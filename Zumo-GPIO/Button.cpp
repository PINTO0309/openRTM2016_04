#include "Button.h"

/**
 * ボタンの情報を送信
 * 変化があったときだけ送信を実行
 * 引数   : port : シリアルポートインスタンス
 * 返り値 : 無し
 */
void Button::SendStatus(SerialPort port) {
  bool A = btnA.isPressed ();
  bool B = btnB.isPressed ();
  bool C = btnC.isPressed ();
  if (A != btnAL) {
    port.Send(0x08, A);
    btnAL = A;
  }
  if (B != btnBL) {
    port.Send(0x09, B);
    btnBL = B;
  }
  if (C != btnCL) {
    port.Send(0x0A, C);
    btnCL = C;
  }
}
