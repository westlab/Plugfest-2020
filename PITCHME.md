### PlugFest Demo
### MQTT+Bluetooth+IoT
Keio University
Tokyo Denki University

---

### Interop 1451 Plugfest/Demo System Configuration

---

### How to use Bluetooth?

- BNEP encapsulation (Bluetooth Network Encapsulation Protocol)
  - To use bnep0 network device
  - Working on L2CAP (Logical Link Control and Adaption Protocol)
  - REFCOMM runs on BNEP

- BLE (Bluetooth Low Energy)
  - Currently, out-of-scope for IEEE1451-1?
  - Popular protocol for tiny sensor nodes

---

### Bluetooth Sensor – Raspberry Pi 3 connection

- ALPS IoT Sensor (BLE)
  - Power: 2.35-3.30V 7mA(Peak)
  - Communication: Bluetooth 4.1
  - Sensors:
    - 6D Acceleration Sensor (-2G – 2G extendable)
    - Presser Sensor (300-1100hPa, 0.013hPa/LSB)
    - Temperature (-20 - +85 C, 0.02 C/LSB)
    - Humidity (0 – 100%, 0.016%/LSB)
    - UV (0 - 20.48mW/cm2)
    - Illuminance (0 – 81900Lx, 20Lx/LSB)
- Raspberry Pi 3 B/B+
  - NOOBS + bluepy + alps_extension

---

### Design Map

---

### System Configuration

---

### How to communicate via MQTT?

- Sensor Data Transmission over MQTT
- TEDS Transmission over MQTT

- Sensor Data
  - Sequential Mode
    - Data come periodically
  - TIM becomes Publisher with the Topic of
  /plugfest/NodeName/SensorName/[data] (for demo)  
  Generally  
  /Manufacturer/Model/Version/SerialNumber[/Field]  
  OR  
  /Country/Region/City/Area/Street/Building/Apartment/Sensor[/Field]
 - Application
Becomes Subscriber to read the sensor data by using same Topic

---

### How to send TEDS?

- Design Policy
  - TEDS is only needed when required.  
  Namely, TEDS request from application to TIM is required.
  - After that, TIM send appropriate TEDS according to Topic of the request.
  - When sensor becomes unavailable, application should recognize the unavailability.

- This sequence should be designed on MQTT transactions.

---

### Retain and WILL mechanism

- Retain
  - Publisher can send a message with retain bit.
  - The message with retain bit will be kept in MQTT broker.
    - When subscribed, “the last message with the retain bit” will return.
  - MQTT brokers does not guarantee storing all messages with retain bit.
  - Some MQTT brokers does not implement retain mechanism.
- WILL
  - When subscribers becomes unavailable, WILL message returns to all subscribers of the sensor’s topics.
    - WILL message may observe HTTP status code (RFC7231)
  - Keep Alive Timer function with PINGREQ/PINGRESP message will be used for checking availability of sensors.

---

### Implementation status of retain and WILL

|Broker(version)|Language|Supported version|QoS level|Retain|Will|
|:---|:---|:---|:---|:---|:---|
|Mosquitto(1.5.3)|C|3.1/3.1.1|0,1,2|Yes|Yes|
|Apollo(1.7.1)|Java|3.1|0,1,2|Yes|Yes|
|RabbitMQ(3.7.8)|Erlang|3.1|0,1|Yes|Yes|
|Mosca(2.8.3)|Node.js|3.1|0,1|Yes|Yes|
|eMQTTD(0.8.6-beta)|Erlang|3.1/3.1.1|0,1,2|Yes|Yes|
|VerneMQ(0.9.4)|Erlang|3.1/3.1.1|0,1,2|Yes|Yes|
|HIVEMQ(3.4.0)|Java|3.1/3.1.1|0,1,2|Yes|Yes|
|MQTTnet(2.8.2)|C#|3.1/3.1.1|0,1,2|Yes|Yes|
|RabbitMQ(3.5.3)|Erlang|3.1|0,1|No|Yes|
|Mosca(0.29.0)|Node.js|3.1|0,1|No|Yes|

---

### You don’t like MQTT?

- Almost all problems are solved by using MQTT 5.0
- Encryption / Authorization supported
  - Negotiation can be supported by client ID and key/value properties
  - Injection can be prevented (It was supported, but standardized in 5.0)
- Scalability is improved
  - Support connection-less communication = No limitation in the number of connection
- Expression flexibility is improved
 - User Property was given and error codes are improved
- End-to-end message acceptance confirmation is supported
- MQTT v3 defined little about broker, and MQTT extend the definition. However, MQTT broker design had flexibility. MQTT v5 defines many broker design rules.

---

### MQTT 5.0 Support

- We can support MQTT 5.0 by using Python gmqtt and flespi MQTT broker.
  - All MQTT 5.0 functions are not supported
    It depends on flespi MQTT broker design and update

- These set is not a major implementation

---

### TEDS acquisition sequence (Option A = preferable)

- Sensor Node
  - Publish TEDS *with retain flag*  
  /plugfest/ModeName/SensorName/TEDS  
  /plugfest/ModeName/SensorName/METATEDS
  - Use Keep-Alive-Timer (PINGREQ/PINGRESQ Message) [Opt-A]  
  (We need to check MQTT behavior when Timer expires and retain-flagged message is lost or remains. This is case WILL is helpful.)  
  OR
  - Subscribe PING topic with similar way of Option B [Opt-A’ not good idea]  
  plugfest/ModeName/SensorName/ALIVE
- Application
  - Subscribe TEDS by [A]
  - Check availability of sensor by TEDS availability, [A]+WILL, or [A’]

---

### TEDS acquisition sequence (Option B)

- MQTT Broker can keep TEDS by retain flag
  - Publisher publishes TEDS message with retain bit firstly.
  - After that sensor data is sent to the same topic without retain bit.
- Then, all application can subscribe TEDS in the beginning.
- Clients can get TEDS again by reconnecting.

---

### TEDS acquisition sequence (Option C)

- Sensor Node
  - Subscribe predefined Topic to receive TEDS request  
  /plugfest/ModeName/SensorName/TEDS/TEDSREQ [A]  
  /plugfest/ModeName/SensorName/METATEDS/TEDSREQ
- Application
  - Generate UniqID (according to MAC address and current time)
  - Subscribe (wait) TEDS by using the topic of  
  /plugfest/Node name/TEDS/TEDSRECV/[UniqID]
  - Publish UniqID to /plugfest/NodeName/SensorName/TEDS/TEDSREQ [A]
- Sensor Node
  - Receive ID by [A]
  - Publish TEDS to given Topic  
  /plugfest/Node name/TEDSRECV/[UniqID] [B]
  - Close the Port of the Topic
Retain flag may simplify this process. However, this option implies no retain and will implementation on the server as well as incompatible implementation.

---

### TEDS update sequence (option)

Simply, TEDS will be updated when a certain topic in the initialization process was published.

Dynamic update?
Sensor has to subscribe the topic periodically.

---

### Other useful information

- Raspberry Pi Image file Reader/Writer  
http://sourceforge.jp/projects/sfnet_win32diskimager/

- Our design on Git  
https://github.com/westlab/PlugFest

- Presentation Magerials  
https://github.com/westlab/PlugFest

---

### TEDS

- We used DeweTEDSEditor to generate TEDS information
  - It outputs TEDS binary data (HEX text) only
- XML-based TEDS was also defined according to the input data to the editor (self-typed)
  - Currently using Meta-identification TEDS
  - It will be extended to XEP-0323  
  (http://www.sensei-iot.org/PDF/Transforming_TEDS.pdf)
  
---

### Creating TEDS

- ALPS Electric Co.Ltd. Smart IoT Sensor Module

### TEDS example (Temperature Sensor)

- TEDS  
    40002004320000AA0107A1C0E00485953A3D0A660B928246586A56F3722DF93E124  
    CCA0183933228A60000803F010040830100548500EA540773C1642FE654081C00
- METATEDS (XML)  
```
<?xml version="1.0" encoding="UTF-8"?>  
<MetaIdentificationTEDSDataBlock>  
  <manufacturer>Unknown</manufacturer>  
  <manufacturerId>109</manufacturerId>  
  <ModelNo>1A1</ModelNo>  
  <SerialNo>50</SerialNo>  
  <UserManufacturer>ALPS ELE</UserManufacturer>  
  <UserModelNo>IOT SMART MDL</UserModelNo>  
  <UserSerialNo>SUFOYUEYWO</UserSerialNo>  
  <UserPhysicalMeasurand>TEMPARATURE</UserPhysicalMeasurand>  
  <UnitScale>DEG C/DECIM/TXT</UnitScale>  
  <UnitConvertionFactor>1</UnitConvertionFactor>  
  <UserSensorLimits>Yes</UserSensorLimits>  
  <PhysicalSensorMin>-20</PhysicalSensorMin>  
  <PhysicalSensorMax>85</PhysicalSensorMax>  
  <UserDataValue>S:0.02/LSB</UserDataValue>  
</MetaIdentificationTEDSDataBlock>
```

---

### Sensor BLE Format

- Command
 - Write command

|Event Code|Length|Data (Single/LSB,MSB)|
|:---|:---|:---|

  - Read command

|Event Code + 0x80|Length|Data (Single/LSB,MSB)|
|:---|:---|:---|

- Event Code  
0x20 (Measurement control)  
0x21 (Bluetooth configuration)  
0x23 (Disable data transfer)  
0x2D (Communication parameter)  
0x2E (Status / Data request)  
0x30 (Internal Clock adjustment)

---

### TIM Operation

- Get sensor data from BLE sensor
- Load TEDS format from file system
  - Network update sub command is also available
- TEDS ID is defined by the filename
  - TEDS files are generated by unified TEDS definition file, and the filenames are also automatically given according to the definition file.
- Data format (json is used for elasticsearch+kibana)  
{DATETIME:{},PRESSURE:{.3f},HUMID:{.3f},TEMP:{.3f},ILLUMI:{.3f},UV:{.3f},GEOMAG:{.3f},ACCEL:{.3f}}
  - Currently, only X axis is transferred for GEOMAG and ACCEL
  - DATETIME format is YYYY-MM-DD HH:MM:SS.mmm

### Command line options (TIM : alps.py)

```
usage: Receive BLE sensor data and send to NCAP with TEDS and METATEDS
optional arguments:
  -h, --help            show this help message and exit
  --version             verbose operation (output sensor data)
  -v, --verbose         verbose operation (output sensor data)
  -q, --quiet           quiet (does not output data messages)
  -P, --pseudo_sensor   generate random sensor values without ALPS module
  -m [ALPSMODULE], --alpsmodule [ALPSMODULE]
                        specify ALPS Smart IoT Module Bluetooth address
  -d [DESTINATION_ADDRESS], --destination_address [DESTINATION_ADDRESS]
                        specify destination Bluetooth address
  -E, --elasticsearch   prepare elasticsearch/kibana data and push
  -e [ELASTICSEARCH_ADDRESS], --elasticsearch_address [ELASTICSEARCH_ADDRESS]
                        specify destination Bluetooth address
```

### Command line options (NCAP : rfcommserver.py)

```
usage: Receive BLE sensor data and send to NCAP with TEDS and METATEDS
optional arguments:
  -h, --help            show this help message and exit
  --version             verbose operation (output sensor data)
  -v, --verbose         verbose operation (output sensor data)
  -q, --quiet           quiet (does not output data messages)
  -c [{0,1,2,3} [{0,1,2,3} ...]], --connect [{0,1,2,3} [{0,1,2,3} ...]]
                        connect to MQTT server (mode ID can be specified [0:No TEDS 1:Dual topics 2:Single topic 3:Callback Multiple designation is available)
  -P, --pseudo_sensor   generate random sensor values without ALPS module
  -s MQTT_SERVER, --mqtt_server MQTT_SERVER
                        specify MQTT server IP address
  -p MQTT_PORT, --mqtt_port MQTT_PORT
                        specify MQTT server port
  -k MQTT_KEEPALIVE, --mqtt_keepalive MQTT_KEEPALIVE
                        specify MQTT keepalive timer (default is 15)
  -t TOPIC, --topic TOPIC
                        specify topic to publish (suffix is automatically added)

```

### Testing Environment


---

### Plugfest Demo Image


---

### Operation Demo

https://www.youtube.com/watch?v=fLECv2HtAZ4

---
