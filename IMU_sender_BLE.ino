// Sends IMU data to another device via BLE
// Reference: https://docs.arduino.cc/tutorials/nano-33-iot/bluetooth

#include <ArduinoBLE.h>
#include <Arduino_LSM6DS3.h>

long previousMillis = 0;
int interval = 0;
int ledState = LOW;
unsigned int SIZE = 24;

BLEService mluService("IMU"); // BLE LED Service

BLECharacteristic mluCharacteristic("2A57", BLERead, SIZE, true);

void writeFloat(float value, byte buffer[], unsigned int offset){
  for (int i = 0; i < 4; ++i){
    buffer[offset + i] = ((uint8_t*)&value)[i];
  }
}

void setup() {
  // set built in LED pin to output mode
  pinMode(LED_BUILTIN, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting Bluetooth® Low Energy failed!");

    while (1);
  }
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("kexin2's arduino nano 33");
  BLE.setDeviceName("kexin2's arduino");
  BLE.setAdvertisedService(mluService);

  // add the characteristic to the service
  mluService.addCharacteristic(mluCharacteristic);

  // add service
  BLE.addService(mluService);

  // start advertising
  BLE.advertise();
}

void loop() {
  // create buffer to store mlu values
  byte buffer[SIZE];
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    digitalWrite(LED_BUILTIN, HIGH);

    // while the central is still connected to peripheral:
    while (central.connected()) {
      if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        float imuData[3];
        // read acceleration data and store into buffer
        IMU.readAcceleration(imuData[0], imuData[1], imuData[2]);
        for (int i = 0; i < 3; ++i){
          writeFloat(imuData[i], buffer, i * 4);
        }
        // read gyroscope data and store into buffer
        IMU.readGyroscope(imuData[0], imuData[1], imuData[2]);
        for (int i = 0; i < 3; ++i){
          writeFloat(imuData[i], buffer, (i + 3) * 4);
        }
        // send data via BLE
        mluCharacteristic.writeValue(buffer, SIZE);
      } 
    }

    // when the central disconnects, print it out:
    digitalWrite(LED_BUILTIN, LOW);
  }
}