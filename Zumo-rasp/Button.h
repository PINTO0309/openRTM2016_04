#ifndef __INC_BUTTON
#define __INC_BUTTON

#include <Zumo32U4.h>
#include "SerialPort.h"

class Button {
  private:
    Zumo32U4ButtonA btnA;
    Zumo32U4ButtonB btnB;
    Zumo32U4ButtonC btnC;
    bool btnAL;
    bool btnBL;
    bool btnCL;

  public:
    void SendStatus(SerialPort port);
};

#endif
