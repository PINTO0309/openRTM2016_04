#ifndef __INC_MOTOR
#define __INC_MOTOR

#include <Zumo32U4.h>
#include "SerialPort.h"

/*ミリ秒から秒への倍率*/
#define US_S 1000000
/*モータ制御値の最小値・最大値*/
#define MTR_MIN -400
#define MTR_MAX  400
/*モータ制御値に整形*/
#define MTR_VAL(v) ((int16_t)max(min(v,MTR_MAX),MTR_MIN))

class Motor {
  private:
    float KP, KI, KD;
    float VL, VR;
    float RL, RR;
    float sL;
    float sR;
    float pL;
    float pR;
    unsigned long LastT;
    Zumo32U4Motors mtr;
    Zumo32U4Encoders enc;

  public:
    Motor() ;
    void SetSpeedL(float L) {
      VL = L;
    }
    void SetSpeedR( float R) {
      VR = R;
    }

    void SendSpeed(SerialPort port);
    void SetSpeed();
    void SetKP(float v) {
      KP = v;
    }
    void SetKI(float v) {
      KI = v;
    }
    void SetKD(float v) {
      KD = v;
    }
};

#endif
