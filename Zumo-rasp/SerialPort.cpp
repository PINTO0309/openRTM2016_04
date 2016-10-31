#include "SerialPort.h"

/*コンストラクタ*/
SerialPort::SerialPort() {
  SPort.begin(9600);
  DataPoint = ((byte *)(&BufBase));
}
/**
   情報のシリアライズ及び送信
   引数   : ID    : 送信値のID
            value : 送信値のポインタ
   返り値 : 無し
*/
void SerialPort::Send(byte ID, unsigned long *value) {
  unsigned long long SendD = (unsigned long long)(*value);
  SendD |= (unsigned long long)ID << 32;
  byte CRC = CalcCRC(SendD);
  SendD <<= 3;
  SendD |= (unsigned long long)CRC;
  byte Buf[DATA_BYTE] = {0};
  Buf[DATA_BYTE - 1] = 0x80;
  for (int i = 0; i < DATA_BYTE; i++) {
    int Sh = DATA_BIT * (DATA_BYTE - 1 - i);
    Buf[i] |= (SendD & (0x7FULL << Sh)) >> Sh;
  }
  SPort.write(Buf, DATA_BYTE);
}
/**
   通信を受信及びデシリアライズ
   引数   : 無し
   返り値 : 受信情報無し             : -1
            一部受信                 : -1
            エラーのあるデータを受信 : -2
            正常なデータを受信       : データのID
*/
int SerialPort::CheckData() {
  while (SPort.available() > 0) {
    /*受信*/
    int readed = SPort.read();
    if (readed == -1) {/*エラー防止*/
      return -1;
    }
    /*受信値をバッファに追加*/
    BufBase <<= 7;
    BufBase |= (unsigned long long)(readed & 0x7F);
    /*受信値が最終バイトであればデシリアライズ*/
    if ((readed & 0x80) != 0) {
      /*不要部の削除*/
      BufBase &= 0x3FFFFFFFFFFULL;
      /*受信値が持つCRC値を取得*/
      byte CRC_Res = BufBase & 0x7;
      /*受信値からCRCを算出*/
      BufBase >>= 3;
      byte CRC_Cal = CalcCRC(BufBase);
      /*CRCが一致したらIDを返す*/
      if (CRC_Res == CRC_Cal) {
        return (BufBase >> 32) & 0x7FULL;
      }
      /*CRCが一致しなければエラーあり*/
      return -2;
    }
  }
  return -1;
}
/**
 * CRCを計算(3bit)
 * 引数   : value : 計算対象
 * 返り値 : 計算結果
 */
byte CalcCRC(unsigned long long value) {
  unsigned long long MaskCRC = 1ULL     << 38;
  unsigned long long DataCRC = CRC_BASE << 35;
  for (int i = 0; i < 36; i++) {
    if ((value & MaskCRC) != 0) {
      value ^= DataCRC;
    }
    DataCRC >>= 1;
    MaskCRC >>= 1;
  }
  return (byte)(value & 0x7);
}

