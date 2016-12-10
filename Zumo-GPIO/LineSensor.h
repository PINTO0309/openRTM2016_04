#ifndef __INT_LINESENS
#define __INT_LINESENS

#include <Zumo32U4.h>
#include "SerialPort.h"

#define NUM_SENSORS 5

class LineSensor {
  private:
    uint16_t lineSensorValues[NUM_SENSORS];
    Zumo32U4LineSensors lineSensors;

  public:
    LineSensor();
    void SendStatus(SerialPort port);

};

#endif
