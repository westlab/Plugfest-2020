#!/usr/bin/env python

# Test whether message parameters are passed to the plugin acl check function.

from mosq_test_helper import *

def write_config(filename, port):
    with open(filename, 'w') as f:
        f.write("port %d\n" % (port))
        f.write("auth_plugin c/auth_plugin_msg_params.so\n")
        f.write("allow_anonymous true\n")

port = mosq_test.get_port()
conf_file = os.path.basename(__file__).replace('.py', '.conf')
write_config(conf_file, port)

rc = 1
keepalive = 10
connect_packet = mosq_test.gen_connect("msg-param-test", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

mid = 2
subscribe_packet = mosq_test.gen_subscribe(mid, "param/topic", 1)
suback_packet = mosq_test.gen_suback(mid, 1)

mid = 3
publish_packet = mosq_test.gen_publish(topic="param/topic", qos=1, payload="payload contents", retain=1, mid=mid)
puback_packet = mosq_test.gen_puback(mid)

mid = 1
publish_packet_recv = mosq_test.gen_publish(topic="param/topic", qos=1, payload="payload contents", retain=0, mid=mid)


broker = mosq_test.start_broker(filename=os.path.basename(__file__), use_conf=True, port=port)

try:
    sock = mosq_test.do_client_connect(connect_packet, connack_packet, timeout=20, port=port)
    mosq_test.do_send_receive(sock, subscribe_packet, suback_packet, "suback")
    mosq_test.do_send_receive(sock, publish_packet, puback_packet, "puback")

    if mosq_test.expect_packet(sock, "publish receive", publish_packet_recv):
        rc = 0

    sock.close()
finally:
    os.remove(conf_file)
    broker.terminate()
    broker.wait()
    (stdo, stde) = broker.communicate()
    if rc:
        print(stde)


exit(rc)

