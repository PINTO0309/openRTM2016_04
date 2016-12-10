#ifndef __INC_SPORT
#define __INC_SPORT

#include <Zumo32U4.h>

#ifndef SPort
/*シリアルポート*/
/* Windows (from USB Port): Serial */
/* GPIO: Serial1 */
#define SPort Serial
#endif

/*CRCの除数,データ長(bit)*/
#define CRC_BASE 0b1011ULL
#define DATA_SIZE 39
/*送受信するデータの長さ[byte],1バイトあたりの長さ[bit]*/
#define DATA_BYTE 6
#define DATA_BIT  7

class SerialPort {
  private:
    /*バッファのメモリ*/
    unsigned long long BufBase;
    /*バッファの中で、データが始まる所のポインタ*/
    byte *DataPoint;

  public:

    SerialPort();
    /*データの送信*/
    void Send(byte ID, unsigned long *value);
    /**
       データの送信(符号なし整数値用)
       引数   : ID    : 送信値のID
              : value : 送信値
       返り値 : 無し
    */
    void Send(byte ID, unsigned long value) {
      Send(ID, &value);
    }
    /**
       データの送信(符号あり整数値用)
       引数   : ID    : 送信値のID
              : value : 送信値
       返り値 : 無し
    */
    void Send(byte ID, signed long value) {
      Send(ID, (unsigned long *)&value);
    }
    /**
       データの送信(浮動小数点値用)
       引数   : ID    : 送信値のID
              : value : 送信値
       返り値 : 無し
    */
    void Send(byte ID, float value) {
      Send(ID, (unsigned long *)&value);
    }
    /**
       データの送信(ブール値用)
       引数   : ID    : 送信値のID
              : value : 送信値
       返り値 : 無し
    */
    void Send(byte ID, bool value) {
      if (value) {
        Send(ID, 1L);
      } else {
        Send(ID, 0L);
      }
    }
    /*データの確認*/
    int CheckData();
    /**
       受信したデータを読み込み(浮動小数点値用)
       引数   : 無し
       返り値 : 受信値
    */
    float GetFloat() {
      return *((float *)DataPoint);
    }
    /**
       受信したデータを読み込み(符号なし整数値用)
       引数   : 無し
       返り値 : 受信値
    */
    unsigned long GetULong() {
      return *((unsigned long *)DataPoint);
    }
    /**
       受信したデータを読み込み(符号あり整数値用)
       引数   : 無し
       返り値 : 受信値
    */
    signed long GetSLong() {
      return *((signed long *)DataPoint);
    }
    /**
       受信したデータを読み込み(ブール値用)
       引数   : 無し
       返り値 : 受信値
    */
    bool GetBool() {
      return GetULong() == 1;
    }
};
/*CRCの計算*/
byte CalcCRC(unsigned long long value);

#endif
