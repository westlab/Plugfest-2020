/*
 *  Wind Speed Direction Sensor (SGLab)
 * 
 *  Signal Level 3.3V
 *  CN-IP 1-Pin C1 +5V/+3.3V
 *        3-Pin C2 R(270) NodeMCU TxD GPIO13 RXD2
 *        4-Pin C3        NodeMCU RxD GPIO15 TXD2
 *        8-Pin C4 GND
 *   Serial Communication
 *   - Use HardwareSerial (its conflicts with serial monitor.
 *         You cannot use serial monitor window for debugging)
 *   - Baudrate 38400 / 9600 (Switch according to the sensor MODEL)
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
const char* ssid = "TP-Link_102B";
const char* password = "32204353";
const char* mqtt_server = "131.113.98.77";
//const char* mqtt_server = "iot.eclipse.org";
bool stchk = true;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(100);
  // We start by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {

} //end callback

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    //if you MQTT broker has clientID,username and password
    //please change following line to    if (client.connect(clientId,userName,passWord))
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      //once connected to MQTT broker, subscribe command if any
      //      client.subscribe("OsoyooCommand");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
} //end reconnect()

void setup() {
  Serial.begin(38400);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  Serial.swap();
  delay(100);
}

void loop() {
  String buf;
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  Serial.println("<RM,>??");
  delay(1);
  if (Serial.available() > 0) {
    buf = Serial.readStringUntil('\n');
  }
  buf.trim();
  char message[58];
  buf.toCharArray(message, 58);
  client.publish("/TESTData", message);
  delay(1000);
}
