#include "SerialPort.h"

SerialPort::SerialPort() {
  SPort.begin(9600);
  DataPoint = ((byte *)(&BufBase));
}
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
int SerialPort::CheckData() {
  while (SPort.available() > 0) {
    int readed = SPort.read();
    if (readed == -1) {
      return -1;
    }
    BufBase <<= 7;
    BufBase |= (unsigned long long)(readed & 0x7F);
    if ((readed & 0x80) != 0) {
      BufBase &= 0x3FFFFFFFFFFULL;
      byte CRC_Res = BufBase & 0x7;
      BufBase >>= 3;
      byte CRC_Cal = CalcCRC(BufBase);
      if (CRC_Res == CRC_Cal) {
        return (BufBase >> 32) & 0x7FULL;
      }
      return -2;
    }
  }
  return -1;
}
byte CalcCRC(unsigned long long value) {
  unsigned long long MaskCRC = 1ULL     << 38;
  unsigned long long DataCRC = CRC_BASE << 35;
  for (int i=0;i<36;i++) {
    if ((value & MaskCRC) != 0) {
      value ^= DataCRC;
    }
    DataCRC >>= 1;
    MaskCRC >>= 1;
  }
  return (byte)(value & 0x7);
}

