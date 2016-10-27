#ifndef __INC_BUTTON
#define __INC_BUTTON

#include <Zumo32U4.h>
#include "SerialPort.h"

class Button {
  private:
    /*各ボタン*/
    Zumo32U4ButtonA btnA;
    Zumo32U4ButtonB btnB;
    Zumo32U4ButtonC btnC;
    /*最後にボタンの状態を確認したときの値*/
    bool btnAL;
    bool btnBL;
    bool btnCL;

  public:
  /*情報を送信*/
    void SendStatus(SerialPort port);
};

#endif
