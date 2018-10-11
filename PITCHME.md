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


Design Policy
TEDS is only needed when required.
Namely, TEDS request from application to TIM is required.
After that, TIM send appropriate TEDS according to Topic of the request.
When sensor becomes unavailable, application should recognize the unavailability.

This sequence should be designed on MQTT transactions.


---

