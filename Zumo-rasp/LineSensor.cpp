#include "LineSensor.h"

LineSensor::LineSensor() {
  lineSensors.initFiveSensors();
}
void LineSensor::SendStatus(SerialPort port) {
  lineSensors.read(lineSensorValues);
  for (int i = 0; i < 5; i++) {
    port.Send(0x10 + i, (unsigned long)lineSensorValues[i]);
  }
}

