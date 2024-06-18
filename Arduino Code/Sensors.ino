#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

// WiFi credentials
const char* ssid = "Wifi Name";
const char* password = "Password";

// Server details
const char* serverAddress = "192.168.1.100"; // Change to your server IP address
const int serverPort = 5000;
const String endpoint = "/store";

// Define multiplexer pins
#define S0 D3
#define S1 D4
#define S2 D5
#define Z A0

// SDS011 Sensor pins
#define SDS011_RX D1
#define SDS011_TX D2

SoftwareSerial sdsSerial(SDS011_RX, SDS011_TX);

// Function to select multiplexer channel
void selectMuxChannel(byte channel) {
  digitalWrite(S0, bitRead(channel, 0));
  digitalWrite(S1, bitRead(channel, 1));
  digitalWrite(S2, bitRead(channel, 2));
}

void setup() {
  Serial.begin(115200);
  sdsSerial.begin(9600);

  // Initialize multiplexer pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);

  // Set all multiplexer pins to LOW initially
  digitalWrite(S0, LOW);
  digitalWrite(S1, LOW);
  digitalWrite(S2, LOW);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void loop() {
  // Read data from SDS011
  readSDS011();

  // Read data from other sensors through multiplexer
  float sensorValues[7]; // Array to hold sensor values
  for (byte channel = 0; channel < 7; channel++) { // 7 channels for 7 sensors
    selectMuxChannel(channel);
    delay(100); // Allow the channel to stabilize
    int sensorValue = analogRead(Z);
    // Convert analog readings to appropriate units
    switch (channel) {
      case 0: // PM2.5
      case 1: // PM10
        // Convert analog readings to micrograms per cubic meter (ug/m3)
        sensorValues[channel] = sensorValue;
        break;
      case 3: // NOx
        // Convert analog readings to parts per billion (ppb)
        sensorValues[channel] = sensorValue;
        break;

      case 2: // SO2
      case 5: // CO
      case 4: // NH3
      case 6: // O3
        // Convert analog reading to mg/m^3
        sensorValues[channel] = sensorValue * 0.02; // Example conversion factor, adjust as per sensor datasheet
        break;
    }

  }

  // Create POST request payload
  String payload = "PM25=" + String(sensorValues[0]) +
                   "&PM10=" + String(sensorValues[1]) +
                   "&SO2=" + String(sensorValues[2]) +
                   "&NOx=" + String(sensorValues[3]) +
                   "&NH3=" + String(sensorValues[4]) +
                   "&CO=" + String(sensorValues[5]) +
                   "&O3=" + String(sensorValues[6]);

  // Send POST request to server
  sendPOSTRequest(payload);

  delay(5000); // Wait before sending data again
}

void readSDS011() {
  if (sdsSerial.available() >= 10) { // Check if 10 bytes available (frame length for SDS011)
    uint8_t data[10];
    sdsSerial.readBytes(data, 10);
    // Process and print SDS011 data
  }
}

void sendPOSTRequest(String payload) {
  WiFiClient client;
  if (client.connect(serverAddress, serverPort)) {
    client.println("POST " + endpoint + " HTTP/1.1");
    client.println("Host: " + String(serverAddress));
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.println("Connection: close");
    client.print("Content-Length: ");
    client.println(payload.length());
    client.println();
    client.println(payload);
  } else {
    Serial.println("Connection to server failed");
  }
  client.stop();
}
