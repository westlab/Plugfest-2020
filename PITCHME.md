
## Interop 1451
## PlugFest Demo
## MQTT+Bluetooth+IoT
Keio University
Tokyo Denki University

To make a presentation of this document, please access:

https://gitpitch.com/westlab/PlugFest/

---

### PlugFest Demo System Configuration

<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/PlugFest.png" alt="PlugFest">

---

### How to use Bluetooth?

- BNEP encapsulation (Bluetooth Network Encapsulation Protocol)
  - To use bnep0 network device
  - Working on L2CAP (Logical Link Control and Adaption Protocol)
  - REFCOMM runs on BNEP

- BLE (Bluetooth Low Energy)
  - Currently, out-of-scope for IEEE1451-1?
  - Popular protocol for tiny sensor nodes

+++

### Bluetooth Sensor

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

@snap[east]
<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/alps.png" alt="BLE Sensor" width="50%">
@snapend

+++

### Sensor BLE Format

- Command
 - Write command
  - Event Code + Length + Data (Single/LSB,MSB)
 - Read command
  - Event Code + 0x80 + Length + Data (Single/LSB,MSB)
  
- Event Code  
  - 0x20 (Measurement control)  
  - 0x21 (Bluetooth configuration)  
  - 0x23 (Disable data transfer)  
  - 0x2D (Communication parameter)  
  - 0x2E (Status / Data request)  
  - 0x30 (Internal Clock adjustment)

+++

### Raspberry Pi 3

- Raspberry Pi 3 B/B+　　　　　　　　　　　　　　　　　　　　
  - NOOBS + bluepy + alps_extension
- Rasberry Pi 2 or earlier needs bluetooth and  
  WiFi dongles.
- Heat Sink is preferable to use.
- Raspberry Pi 3 B+ has PoE function and is  
  convenient to build Raspberry Pi Cluster  
  environment.
- Raspberry Pi 3 and Heat Sink may need appropriate  
  case for preventing interference between the heat  
  sink and the case.

@snap[east]
<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/RP3.png" alt="Raspberry Pi 3" width="50%">
@snapend

---

### Design Map

![Design Map](https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/ConfigMap.png)

---

### System Configuration

![System Configuration](https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/SystemStructure.png)

---

### How to communicate via MQTT?

- Both Sensor and TEDS Data Transmission over MQTT
- Sensor Data
  - Sequential Mode
    - Data come periodically
  - TIM becomes Publisher with the Topic of  
  /plugfest/NodeName/SensorName/[data] (for demo)  
  Generally, it will be  
  /Manufacturer/Model/Version/SerialNumber[/Field]  
  OR  
  /Country/Region/City/Area/Street/Building/Apartment/Sensor[/Field]
 - Application becomes subscriber to read the sensor data by using same Topic.

---

### Why we desined our own MQTT broker?

- MQTT v3 does not define the function of MQTT broker clearly.
- THere are many local rules in the implementation of MQTT blokers.
- We wanted to check and adopt the differences of MQTT brokers.
  - mosquitto becomes a defact standard of MQTT broker.
- MQTTnet is a C# based MQTT broker implementation, and is very flexible.

---

### How to send TEDS?

- Design Policy
  - TEDS is only needed when required.  
  Namely, TEDS request to TIM/NCAP is required from an application.
  - After that, TIM/NCAP send appropriate TEDS according to Topic of the request.
  - When sensor becomes unavailable, application should recognize the unavailability.

- This sequence should be designed on MQTT transactions.

+++

### Retain and WILL mechanism

- Retain
  - Publisher can send a message with retain bit.
  - The message with retain bit will be kept in MQTT broker.
    - When subscribed, “the last message with the retain bit” will return.
  - MQTT brokers does not guarantee storing all messages with retain bit.
  - Some MQTT brokers does not implement retain mechanism.
- WILL
  - When publisher becomes unavailable, WILL message returns to all subscribers of the publisher's topics.
    - WILL message may observe HTTP status code (RFC7231)
    - MQTT v5.0 has extension in this status code. However, it does not give any guideline of WILL message contents.
  - Keep Alive Timer function with PINGREQ/PINGRESP message will be used for checking availability of sensors.

+++

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
|RabbitMQ(3.5.3)|Erlang|3.1|0,1|*No*|Yes|
|Mosca(0.29.0)|Node.js|3.1|0,1|*No*|Yes|

+++

### You don’t like MQTT?

- Almost all problems are solved in MQTT 5.0.
- Encryption / Authorization support
  - Negotiation can be supported by client ID and key/value properties.
  - Injection can be prevented (It has already solved, but standardized in 5.0).
- Scalability improvement
  - Support connection-less communication. = No limitation in the number of connection
  - Connection-less communication degrades functionalities.
- Expression flexibility improvement
 - User Property was given and error codes are improved.
- End-to-end message acceptance confirmation is supported.
- MQTT v3 did not give enough definition to broker design. It cause a multiple interpretation in designing MQTT broker. HQTT v5 gives many definitions for broker design.

+++

### MQTT 5.0 Support

- We can support MQTT 5.0 by using Python gmqtt and flespi MQTT broker.
  - Even if using flspi MQTT broker, all MQTT 5.0 functions are not supported.

- These set is not a major implementation

---

### TEDS acquisition sequence (Option A = preferable)

- Sensor Node　　　　　　　　　　　　　　　　　　　　　　　　　　　　
  - Publish TEDS *with retain flag*  
  /plugfest/NodeName/SensorName/TEDS  
  /plugfest/NodeName/SensorName/TXTTEDS  
  [Option-A]  Use Keep-Alive-Timer  
    (PINGREQ/PINGRESQ Message)  
  We need to check whether the timer expires.  
  In this case, WILL is helpful.  
  OR  
  [Option-A’] Subscribe PING topic  
  with similar way of next Option B  
  plugfest/NodeName/SensorName/ALIVE
- Application
  - Subscribe TEDS by method [Option-A]
  - Check availability of sensors by cheking TEDS accessibility using method [Option-A]+WILL or [Option-A’]

@snap[east]
<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/DualTopic.png" alt="Dual" width="40%">
@snapend

+++

### TEDS acquisition sequence (Option B)

- MQTT Broker can keep TEDS by retain flag　　　　　　　　　　　　　　　　　　　
  - Publisher publishes TEDS message with retain bit.
  - Publisher has to publish the TES message first.
  - After the TEDS, the publisher sends sensor data  
  to the *same topic without retain bit*.
- Then, all application can subscribe TEDS in the beginning.
- Clients can get TEDS again by reconnecting.

- Redundant TEDS connumication will be achived.
- If application do not care the first TEDS in its  
implementation, it may cause a serious system failure.
- This is simple and can maximize the benefit of using MQTT,  
especially managing distribution tree.

@snap[east]
<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/SingleTopic.png" alt="Single" width="40%">
@snapend

+++

### TEDS acquisition sequence (Option C)

- Sensor Node　　　　　　　　　　　　　　　　　　　　　　　　　　　　
  - Subscribe predefined Topic to receive TEDS request  
  /plugfest/ModeName/SensorName/TEDS/TEDSREQ  
  OR  
  .../TXTTEDS/TEDSREQ
- Application
  - Generate UniqID  
  (according to MAC address and time)
  - Subscribe (and wait) TEDS by checking the topic of  
  /plugfest/Node name/TEDS/TEDSRECV/[UniqID]
  - Publish UniqID to  
   /plugfest/NodeName/SensorName/TEDS/TEDSREQ
- Sensor Node
  - Receive ID from TEDSREQ and publish TEDS to  
  the given Topic  
  /plugfest/Node name/TEDSRECV/[UniqID]
  - Close the Topic
  Retain flag may simplify this process. However, this option implies the target broker does not have any retain and will implementation.

@snap[east]
<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/Callback.png" alt="Callback" width="40%">
@snapend


+++

### TEDS update sequence (option)

- Simply, TEDS will be updated when a certain topic in the initialization process was published.

- Dynamic update?  
Sensor has to subscribe the topic periodically.

---

### Other useful information

- Raspberry Pi Image file Reader/Writer  
http://sourceforge.jp/projects/sfnet_win32diskimager/

- Our design on Git  
https://github.com/westlab/PlugFest

- Installation document  
https://github.com/westlab/PlugFest

- Presentation Magerials  
https://gitpitchcom/westlab/PlugFest

---

### Creating TEDS

Specification of Smart IoT Sensor Module, ALPS Electric Co.Ltd.

@snap[bottom]
<img src="https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/Spec.png" alt="Specification" width="60%">
@snapend

+++

### TEDS editor and TXTTEDS

- We used DeweTEDSEditor to generate TEDS information
  - It outputs TEDS binary data (HEX text) only
- XML-based TEDS was also defined according to the input data to the editor (self-typed)
  - Currently using Tranducer Channel TEDS
  - It will be extended to XEP-0323  
  (http://www.sensei-iot.org/PDF/Transforming_TEDS.pdf)
  
+++

### TEDS example (Temperature Sensor)

- TEDS  
```
    40002004320000AA0107A1C0E00485953A3D0A660B928246586A56F3722DF93E124  
    CCA0183933228A60000803F010040830100548500EA540773C1642FE654081C00
```
- TXTTEDS (XML)  
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

### IEEE1451.0 Implementation

- Use Block Method (5.9)
- Use Continuous Sampling Mode and Immediate Operation (5.10.1.6, 7)
- Partially Supports HTTP API (Table 106)
- YAML is used for the expression of commands
  - All command and TEDS will be replaced into YAML for simplifing implementation.
---

### TIM Operation

- Get sensor data from BLE sensor
- Load TEDS format from file system
  - Network update sub command is also available.
- TEDS ID is defined by the filename
  - TEDS files are generated by unified TEDS definition file, and the filenames are also automatically given according to the definition file.
- Data format (json is used for elasticsearch+kibana)  
```
{DATETIME:{},PRESSURE:{.3f},HUMID:{.3f},TEMP:{.3f},ILLUMI:{.3f},UV:{.3f},GEOMAG:{.3f},ACCEL:{.3f}}
```
  - Currently, only X axis is transferred for GEOMAG and ACCEL.
  - DATETIME format is YYYY-MM-DD HH:MM:SS.mmm

+++

### Command line options (TIM)

- alps.py
```
usage: Receive BLE sensor data and send to NCAP with TEDS and TXTTEDS
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

---

### NCAP operation

- Receive sensor data and TEDS data from TIM
- TEDS cache management
- Forward sensor data and TEDS to application via MQTT
- Manages multiple TIMs
- Works as a server

+++

### Command line options (NCAP)

- rfcommserver.py

```
usage: Receive BLE sensor data and send to NCAP with TEDS and TXTTEDS
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

---

### Testing Environment

![Testing Environment](https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/TestEnv.png)

+++

### Plugfest Demo Image

![Developgment Environment](https://raw.githubusercontent.com/wiki/westewest/PlugFest/images/DevEnv.png)

+++

### Operation Demo

![Video](https://www.youtube.com/embed/fLECv2HtAZ4)

---

# Thank you
