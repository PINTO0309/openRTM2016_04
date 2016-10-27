#include "Motor.h"

Motor::Motor() {
  VL = 0;
  VR = 0;
  KP = 0.1;
  KI = 0.2;
  KD = 0.05;
  sL = 0;
  sR = 0;
  pL = 0;
  pR = 0;
  LastT = 0;
}

void Motor::SendSpeed(SerialPort port) {
  port.Send(0x02, RL);
  port.Send(0x03, RR);
}

void Motor::SetSpeed() {

  /*モータの制御値を設定*/

  int16_t Lc = enc.getCountsAndResetLeft();
  int16_t Rc = enc.getCountsAndResetRight();
  
  unsigned long T = micros(); //[us]
  long dT;//[us]
  if (T > LastT) {
    dT = T - LastT;
  } else {
    dT = T + (~LastT);
    /* ULMaxをunsigned longの最大値とする

      T - (LastT - ULMax)
      = ULMax + T - LastT
      = ULMax + T + (-LastT)
      = ULMax + T + (~LastT + 1)
      = ULMax + T + ~LastT + 1
      = ULMax + 1 + T + ~LastT
      = 0 + T + ~LastT
      (なぜなら、符号なし整数の最大値はすべてのビットが"1"で、
      そこに1を加算するとオーバーフローして0になるから）
      = T + ~LastT
    */
  }
  RL = Lc * (float)US_S / dT;//Lc/(dT/US_S)
  RR = Rc * (float)US_S / dT;//Rc/(dT/US_S)
  float L = VL - RL;
  float R = VR - RR;
  float dL = L - pL;
  float dR = R - pR;
  sL += L;
  sR += R;

  float LP = KP * L + KI * sL + KD * dL;
  float RP = KP * R + KI * sR + KD * dR;

  mtr.setSpeeds(MTR_VAL(LP), MTR_VAL(RP));

  pL = L; pR = R; LastT = T;
}
