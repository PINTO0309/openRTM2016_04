#include <Zumo32U4.h>

#include "Motor.h"
#include "SerialPort.h"
#include "Button.h"
#include "LineSensor.h"

Motor motor;
SerialPort Port;
Button button;
LineSensor lsens;
void setup() {
  // put your setup code here, to run once:

}
void loop() {
  static unsigned long LastTime = 0;
  static unsigned long WaitTime = 20; //[ms]
  static bool SendData = true;
  // put your main code here, to run repeatedly:

  /*データの受信*/
  while (true) {
    switch (Port.CheckData()) {
      case 0x00:
        break;
      //0x01
      case 0x02:
        motor.SetSpeedL(Port.GetFloat());
        break;
      case 0x03:
        motor.SetSpeedR(Port.GetFloat());
        break;
      case 0x04:
        ledRed(Port.GetBool());
        break;
      case 0x05:
        ledGreen(Port.GetBool());
        break;
      case 0x06:
        ledYellow(Port.GetBool());
        break;
      //0x07 ... 0x73
      case 0x74:
        motor.SetKP(Port.GetFloat());
        break;
      case 0x75:
        motor.SetKI(Port.GetFloat());
        break;
      case 0x76:
        motor.SetKD(Port.GetFloat());
        break;
      //0x77
      case 0x78:
        SendData = Port.GetBool();
        break;
      case 0x79:
        WaitTime = Port.GetULong();
        break;
      //0x7A .. 0x7F
      default:
        /*受信したデータが無い or 受信に失敗したため、ループを脱出*/
        goto ExitLoop;
    }
  }
ExitLoop:
  /*データの送信*/
  if (millis() - LastTime >= WaitTime) {
    LastTime = millis();

    motor.SetSpeed();

    if (SendData) {
      motor.SendSpeed(Port);
      lsens.SendStatus(Port);
    }
  }
  /*ボダンの情報送信*/
  button.SendStatus(Port);
}
