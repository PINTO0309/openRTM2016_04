#ifndef __INC_SPORT
#define __INC_SPORT

#include <Zumo32U4.h>

#ifndef SPort
#define SPort Serial
#endif

#define CRC_BASE 0b1011ULL
#define DATA_SIZE 39
#define DATA_BYTE 6
#define DATA_BIT  7

class SerialPort {
  private:

    unsigned long long BufBase;
    byte *DataPoint;

  public:

    SerialPort();

    void Send(byte ID, unsigned long *value);
    void Send(byte ID, unsigned long value) {
      Send(ID, &value);
    }
    void Send(byte ID, signed long value) {
      Send(ID, (unsigned long *)&value);
    }
    void Send(byte ID, float value) {
      Send(ID, (unsigned long *)&value);
    }
    void Send(byte ID, bool value) {
      if (value) {
        Send(ID, 1L);
      } else {
        Send(ID, 0L);
      }
    }
    int CheckData();
    float GetFloat() {
      return *((float *)DataPoint);
    }
    unsigned long GetULong() {
      return *((unsigned long *)DataPoint);
    }
    signed long GetSLong() {
      return *((signed long *)DataPoint);
    }
    bool GetBool() {
      return GetULong() == 1;
    }
};
byte CalcCRC(unsigned long long value);

#endif
