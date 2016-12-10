#include "Motor.h"

/*コンストラクタ*/
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

/**
   クローラの現在の速度を送信
   引数   : port : シリアルポートインスタンス
   返り値 : 無し
*/
void Motor::SendSpeed(SerialPort port) {
  port.Send(0x02, RL);
  port.Send(0x03, RR);
}

/**
   設定された速度になるようモータを制御
   引数   : 無し
   返り値 : 無し
*/
void Motor::SetSpeed() {
  /*現在のエンコーダの値*/
  int16_t Lc = enc.getCountsAndResetLeft();
  int16_t Rc = enc.getCountsAndResetRight();
  /*現在の時刻*/
  unsigned long T = micros(); //[us]
  /*前回制御時からの時間差*/
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
  /*現在の実速度の設定*/
  RL = Lc * (float)US_S / dT;// Lc/(dT/US_S)
  RR = Rc * (float)US_S / dT;// Rc/(dT/US_S)
  /*目標速度との差*/
  float L = VL - RL;
  float R = VR - RR;
  /*前回の目標速度との差との差*/
  float dL = L - pL;
  float dR = R - pR;
  /*目標速度との差の累計*/
  sL += L;
  sR += R;
  /*制御地の設定及び送信*/
  float LP = KP * L + KI * sL + KD * dL;
  float RP = KP * R + KI * sR + KD * dR;
  mtr.setSpeeds(MTR_VAL(LP), MTR_VAL(RP));

  pL = L; pR = R; LastT = T;
}
