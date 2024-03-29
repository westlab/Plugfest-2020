#!/usr/bin/env python

# Test whether a client will is transmitted correctly.

from mosq_test_helper import *

rc = 1
mid = 53
keepalive = 60
connect_packet = mosq_test.gen_connect("will-qos0-test", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

subscribe_packet = mosq_test.gen_subscribe(mid, "will/qos0/test", 0)
suback_packet = mosq_test.gen_suback(mid, 0)

publish_packet = mosq_test.gen_publish("will/qos0/test", qos=0, payload="will-message")

port = mosq_test.get_port()
broker = mosq_test.start_broker(filename=os.path.basename(__file__), port=port)

try:
    sock = mosq_test.do_client_connect(connect_packet, connack_packet, timeout=30, port=port)
    mosq_test.do_send_receive(sock, subscribe_packet, suback_packet, "suback")

    will = subprocess.Popen(['./07-will-qos0-helper.py', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    will.wait()
    (stdo, stde) = will.communicate()

    if mosq_test.expect_packet(sock, "publish", publish_packet):
        rc = 0

    sock.close()
finally:
    broker.terminate()
    broker.wait()
    (stdo, stde) = broker.communicate()
    if rc:
        print(stde)

exit(rc)

