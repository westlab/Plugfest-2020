#!/usr/bin/env python

# Test whether a connection is denied if it provides just a username when it
# needs a username and password.

from mosq_test_helper import *

def write_config(filename, port):
    with open(filename, 'w') as f:
        f.write("port %d\n" % (port))
        f.write("password_file %s\n" % (filename.replace('.conf', '.pwfile')))
        f.write("allow_anonymous false\n")

port = mosq_test.get_port()
conf_file = os.path.basename(__file__).replace('.py', '.conf')
write_config(conf_file, port)

rc = 1
keepalive = 10
connect_packet = mosq_test.gen_connect("connect-uname-test", keepalive=keepalive, username="user")
connack_packet = mosq_test.gen_connack(rc=5)

broker = mosq_test.start_broker(filename=os.path.basename(__file__), use_conf=True, port=port)

try:
    sock = mosq_test.do_client_connect(connect_packet, connack_packet, port=port)
    sock.close()
    rc = 0
finally:
    os.remove(conf_file)
    broker.terminate()
    broker.wait()
    (stdo, stde) = broker.communicate()
    if rc:
        print(stde)

exit(rc)

