/*
Copyright (c) 2010-2018 Roger Light <roger@atchoo.org>

All rights reserved. This program and the accompanying materials
are made available under the terms of the Eclipse Public License v1.0
and Eclipse Distribution License v1.0 which accompany this distribution.
 
The Eclipse Public License is available at
   http://www.eclipse.org/legal/epl-v10.html
and the Eclipse Distribution License is available at
  http://www.eclipse.org/org/documents/edl-v10.php.
 
Contributors:
   Roger Light - initial implementation and documentation.
*/

#include "config.h"

#include <string.h>

#include "mosquitto.h"
#include "mosquitto_internal.h"
#include "logging_mosq.h"
#include "messages_mosq.h"
#include "memory_mosq.h"
#include "packet_mosq.h"
#include "mqtt_protocol.h"
#include "net_mosq.h"
#include "send_mosq.h"
#include "socks_mosq.h"

static int mosquitto__reconnect(struct mosquitto *mosq, bool blocking, const mosquitto_property *properties);
static int mosquitto__connect_init(struct mosquitto *mosq, const char *host, int port, int keepalive, const char *bind_address);


static int mosquitto__connect_init(struct mosquitto *mosq, const char *host, int port, int keepalive, const char *bind_address)
{
	int i;

	if(!mosq) return MOSQ_ERR_INVAL;
	if(!host || port <= 0) return MOSQ_ERR_INVAL;

	if(mosq->id == NULL && (mosq->protocol == mosq_p_mqtt31 || mosq->protocol == mosq_p_mqtt311)){
		mosq->id = (char *)mosquitto__calloc(24, sizeof(char));
		if(!mosq->id){
			return MOSQ_ERR_NOMEM;
		}
		mosq->id[0] = 'm';
		mosq->id[1] = 'o';
		mosq->id[2] = 's';
		mosq->id[3] = 'q';
		mosq->id[4] = '/';

		for(i=5; i<23; i++){
			mosq->id[i] = (random()%73)+48;
		}
	}

	mosquitto__free(mosq->host);
	mosq->host = mosquitto__strdup(host);
	if(!mosq->host) return MOSQ_ERR_NOMEM;
	mosq->port = port;

	mosquitto__free(mosq->bind_address);
	if(bind_address){
		mosq->bind_address = mosquitto__strdup(bind_address);
		if(!mosq->bind_address) return MOSQ_ERR_NOMEM;
	}

	mosq->keepalive = keepalive;
	mosq->receive_quota = mosq->receive_maximum;
	mosq->send_quota = mosq->send_maximum;

	if(mosq->sockpairR != INVALID_SOCKET){
		COMPAT_CLOSE(mosq->sockpairR);
		mosq->sockpairR = INVALID_SOCKET;
	}
	if(mosq->sockpairW != INVALID_SOCKET){
		COMPAT_CLOSE(mosq->sockpairW);
		mosq->sockpairW = INVALID_SOCKET;
	}

	if(net__socketpair(&mosq->sockpairR, &mosq->sockpairW)){
		log__printf(mosq, MOSQ_LOG_WARNING,
				"Warning: Unable to open socket pair, outgoing publish commands may be delayed.");
	}

	return MOSQ_ERR_SUCCESS;
}


int mosquitto_connect(struct mosquitto *mosq, const char *host, int port, int keepalive)
{
	return mosquitto_connect_bind(mosq, host, port, keepalive, NULL);
}


int mosquitto_connect_bind(struct mosquitto *mosq, const char *host, int port, int keepalive, const char *bind_address)
{
	return mosquitto_connect_bind_v5(mosq, host, port, keepalive, bind_address, NULL);
}

int mosquitto_connect_bind_v5(struct mosquitto *mosq, const char *host, int port, int keepalive, const char *bind_address, const mosquitto_property *properties)
{
	int rc;

	if(properties){
		rc = mosquitto_property_check_all(CMD_CONNECT, properties);
		if(rc) return rc;
	}

	rc = mosquitto__connect_init(mosq, host, port, keepalive, bind_address);
	if(rc) return rc;

	pthread_mutex_lock(&mosq->state_mutex);
	mosq->state = mosq_cs_new;
	pthread_mutex_unlock(&mosq->state_mutex);

	return mosquitto__reconnect(mosq, true, properties);
}


int mosquitto_connect_async(struct mosquitto *mosq, const char *host, int port, int keepalive)
{
	return mosquitto_connect_bind_async(mosq, host, port, keepalive, NULL);
}


int mosquitto_connect_bind_async(struct mosquitto *mosq, const char *host, int port, int keepalive, const char *bind_address)
{
	int rc = mosquitto__connect_init(mosq, host, port, keepalive, bind_address);
	if(rc) return rc;

	pthread_mutex_lock(&mosq->state_mutex);
	mosq->state = mosq_cs_connect_async;
	pthread_mutex_unlock(&mosq->state_mutex);

	return mosquitto__reconnect(mosq, false, NULL);
}


int mosquitto_reconnect_async(struct mosquitto *mosq)
{
	return mosquitto__reconnect(mosq, false, NULL);
}


int mosquitto_reconnect(struct mosquitto *mosq)
{
	return mosquitto__reconnect(mosq, true, NULL);
}


static int mosquitto__reconnect(struct mosquitto *mosq, bool blocking, const mosquitto_property *properties)
{
	const mosquitto_property *outgoing_properties = NULL;
	mosquitto_property local_property;
	int rc;
	struct mosquitto__packet *packet;
	if(!mosq) return MOSQ_ERR_INVAL;
	if(!mosq->host || mosq->port <= 0) return MOSQ_ERR_INVAL;
	if(mosq->protocol != mosq_p_mqtt5 && properties) return MOSQ_ERR_NOT_SUPPORTED;

	if(properties){
		if(properties->client_generated){
			outgoing_properties = properties;
		}else{
			memcpy(&local_property, properties, sizeof(mosquitto_property));
			local_property.client_generated = true;
			local_property.next = NULL;
			outgoing_properties = &local_property;
		}
		rc = mosquitto_property_check_all(CMD_CONNECT, outgoing_properties);
		if(rc) return rc;
	}

	pthread_mutex_lock(&mosq->state_mutex);
#ifdef WITH_SOCKS
	if(mosq->socks5_host){
		mosq->state = mosq_cs_socks5_new;
	}else
#endif
	{
		mosq->state = mosq_cs_new;
	}
	pthread_mutex_unlock(&mosq->state_mutex);

	pthread_mutex_lock(&mosq->msgtime_mutex);
	mosq->last_msg_in = mosquitto_time();
	mosq->next_msg_out = mosq->last_msg_in + mosq->keepalive;
	pthread_mutex_unlock(&mosq->msgtime_mutex);

	mosq->ping_t = 0;

	packet__cleanup(&mosq->in_packet);

	pthread_mutex_lock(&mosq->current_out_packet_mutex);
	pthread_mutex_lock(&mosq->out_packet_mutex);

	if(mosq->out_packet && !mosq->current_out_packet){
		mosq->current_out_packet = mosq->out_packet;
		mosq->out_packet = mosq->out_packet->next;
	}

	while(mosq->current_out_packet){
		packet = mosq->current_out_packet;
		/* Free data and reset values */
		mosq->current_out_packet = mosq->out_packet;
		if(mosq->out_packet){
			mosq->out_packet = mosq->out_packet->next;
		}

		packet__cleanup(packet);
		mosquitto__free(packet);
	}
	pthread_mutex_unlock(&mosq->out_packet_mutex);
	pthread_mutex_unlock(&mosq->current_out_packet_mutex);

	message__reconnect_reset(mosq);

	if(mosq->sock != INVALID_SOCKET){
        net__socket_close(mosq); //close socket
    }

#ifdef WITH_SOCKS
	if(mosq->socks5_host){
		rc = net__socket_connect(mosq, mosq->socks5_host, mosq->socks5_port, mosq->bind_address, blocking);
	}else
#endif
	{
		pthread_mutex_lock(&mosq->state_mutex);
		mosq->state = mosq_cs_connecting;
		pthread_mutex_unlock(&mosq->state_mutex);
		rc = net__socket_connect(mosq, mosq->host, mosq->port, mosq->bind_address, blocking);
	}
	if(rc>0){
		return rc;
	}

#ifdef WITH_SOCKS
	if(mosq->socks5_host){
		return socks5__send(mosq);
	}else
#endif
	{
		return send__connect(mosq, mosq->keepalive, mosq->clean_start, outgoing_properties);
	}
}


int mosquitto_disconnect(struct mosquitto *mosq)
{
	return mosquitto_disconnect_v5(mosq, 0, NULL);
}

int mosquitto_disconnect_v5(struct mosquitto *mosq, int reason_code, const mosquitto_property *properties)
{
	const mosquitto_property *outgoing_properties = NULL;
	mosquitto_property local_property;
	int rc;
	if(!mosq) return MOSQ_ERR_INVAL;
	if(mosq->protocol != mosq_p_mqtt5 && properties) return MOSQ_ERR_NOT_SUPPORTED;

	if(properties){
		if(properties->client_generated){
			outgoing_properties = properties;
		}else{
			memcpy(&local_property, properties, sizeof(mosquitto_property));
			local_property.client_generated = true;
			local_property.next = NULL;
			outgoing_properties = &local_property;
		}
		rc = mosquitto_property_check_all(CMD_DISCONNECT, outgoing_properties);
		if(rc) return rc;
	}

	pthread_mutex_lock(&mosq->state_mutex);
	mosq->state = mosq_cs_disconnecting;
	pthread_mutex_unlock(&mosq->state_mutex);

	if(mosq->sock == INVALID_SOCKET) return MOSQ_ERR_NO_CONN;
	return send__disconnect(mosq, reason_code, outgoing_properties);
}


void do_client_disconnect(struct mosquitto *mosq, int reason_code, const mosquitto_property *properties)
{
	pthread_mutex_lock(&mosq->state_mutex);
	mosq->state = mosq_cs_disconnecting;
	pthread_mutex_unlock(&mosq->state_mutex);

	net__socket_close(mosq);

	/* Free data and reset values */
	pthread_mutex_lock(&mosq->out_packet_mutex);
	mosq->current_out_packet = mosq->out_packet;
	if(mosq->out_packet){
		mosq->out_packet = mosq->out_packet->next;
		if(!mosq->out_packet){
			mosq->out_packet_last = NULL;
		}
	}
	pthread_mutex_unlock(&mosq->out_packet_mutex);

	pthread_mutex_lock(&mosq->msgtime_mutex);
	mosq->next_msg_out = mosquitto_time() + mosq->keepalive;
	pthread_mutex_unlock(&mosq->msgtime_mutex);

	pthread_mutex_lock(&mosq->callback_mutex);
	if(mosq->on_disconnect){
		mosq->in_callback = true;
		mosq->on_disconnect(mosq, mosq->userdata, reason_code);
		mosq->in_callback = false;
	}
	if(mosq->on_disconnect_v5){
		mosq->in_callback = true;
		mosq->on_disconnect_v5(mosq, mosq->userdata, reason_code, properties);
		mosq->in_callback = false;
	}
	pthread_mutex_unlock(&mosq->callback_mutex);
	pthread_mutex_unlock(&mosq->current_out_packet_mutex);
}

