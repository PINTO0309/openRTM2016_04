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
    /*比例ゲイン,積分ゲイン,微分ゲイン*/
    float KP, KI, KD;
    /*左目標速度,右目標速度*/
    float VL, VR;//[pt/s]
    /*左実測速度,右実測速度*/
    float RL, RR;//[pt/s]
    /*左速度差累計,右速度差累計*/
    float sL, sR;
    /*左速度差,右速度差*/
    float pL, pR;
    unsigned long LastT;
    /*モータ*/
    Zumo32U4Motors mtr;
    /*エンコーダ*/
    Zumo32U4Encoders enc;

  public:
    Motor() ;
    /**
       左目標速度設定
       引数   : L :目標速度[pt/s]
       返り値 : 無し
    */
    void SetSpeedL(float L) {
      VL = L;
    }
    /**
       右目標速度設定
       引数   : R :目標速度[pt/s]
       返り値 : 無し
    */
    void SetSpeedR( float R) {
      VR = R;
    }

    void SendSpeed(SerialPort port);
    void SetSpeed();
    /**
       比例ゲイン設定
       引数   : v :設定値
       返り値 : 無し
    */
    void SetKP(float v) {
      KP = v;
    }
    /**
       積分ゲイン設定
       引数   : v :設定値
       返り値 : 無し
    */
    void SetKI(float v) {
      KI = v;
    }
    /**
       微分ゲイン設定
       引数   : v :設定値
       返り値 : 無し
    */
    void SetKD(float v) {
      KD = v;
    }
};

#endif
