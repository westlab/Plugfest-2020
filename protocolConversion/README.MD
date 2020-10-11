# Protocol Conversion

## Required Libraries
boost 1.73.0
libpcap (only when directly capture network interfaces to get protocols)

## Directory and files structure
```
.
├ rule_json/  //Description files for conversion in json
├ commands/  //Translated files from rule_json
├ ref // Referenced files when translating
├ sample/  //Samples of middle files
├ update.sh  // generating commands according to rule_json
```

## Making executables
`make all` for making all

* convert_full.out ... Capture lo0 interface and translate XMPP pubsub to MQTT, CoAP, and SMTP
* convert_part.out ... Execute as `./parse_only.out 1 sample/mqtt_src.json` where the digit means 1 to convert general form. and 2 to convert from general form.
* json_parser.out ... Execute as `./json_parser.out <json file name> <text file name>`; used in update.sh

## How to use
Refer the syntax rules in the paper to write json rules.

To generate command files, execute `./update.sh`. This is required whenever you update json files.

## Demo for Plugfest
### How to run demo of protocol conversion
It captures all network traffic of NIC(default is wlp2s0) and transfer MQTT protocol to XMPP protocol for decicated topics.
It is required to execute on MQTT brokder server to captuer all MQTT protocols.
```bash
$ make
$ protocolconversion/convert_full.out
```
### XMPP server
Execute/terminate xmppserver(ejabberd) as follows:
```bash
$ sudo /opt/ejabberd-20.07/bin/ejabberdctl start(stop)
```

To get realtime message from xmppserver(ejabberd)
```bash
$ sudo /opt/ejabberd-20.07/bin/ejabberdctl live
```
Note that it cannot be terminated by pressing `ctrl+C`

Administrator menu is avairable on `http://192.168.0.40:5280/admin/` with admin/demo account.

### Execute XMPP client
Register subscribing nodes as a preperation. Firstly, it is required for subscribing data.
```bash
$ /home/demo/slixmpp/examples/pubsub_client.py pubsub.192.168.0.40 subscribe Plugfest/keio/sensor/1/TEMP -j client@192.168.0.40 -p clientpass
```
Show messages when published to subscribing nodes by using `listen`
```bash
$ /home/demo/slixmpp/examples/pubsub_events.py -j client@192.168.0.40 -p clientpass
```

## TO DO?
Convert by using conversion(const unsigned char *data, const string srcProtocol, const vector\<string\> &dstProtocol), and create transfering library

