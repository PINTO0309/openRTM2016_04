README

甲南大学知能情報学部
2016/10/31

このフォルダには，RTミドルウェアコンテスト2016に参加している「ZumoとRaspberry Piを用いた教育用ロボット環境」の作品データが保存されています．作品は以下のフォルダ，ファイルから構成されています．

(1) Zumo ロボット用 RT Component群
　　(a) 基本コンポーネント
    (b) ゲームパッド入力コンポーネント
    (c) ゲームパッド速度指令コンポーネント
    (d) Zumo-Raspberry Pi間通信テスト用コンポーネント群
    (e) 作例：ライントレーサー
(2) Zumo ロボット内制御プログラム (Raspberry Pi (GPIOシリアル通信）版，Windows (USB Microポート接続）版用）
(3) Zumo基板上にRaspberry Piを搭載するためのCADデータ
(4) Zumoロボットの利用マニュアル

(2)のロボット内制御プログラムは，Zumoロボット基板上のGPIOシリアル通信を利用の場合（主にRaspberry Piを想定）と，Zumoロボット基板上のMicro USBポート経由でのシリアル通信（主にWindowsとの通信を想定）の2種類があります．ご使用の環境に応じて，プログラムを使い分ける必要があります．

フォルダ，ファイルの一覧は以下のとおりです．

- README.txt		README
- ZumoComponents	Pololu Zumo 32U4 RTコンポーネント群
			- 基本コンポーネント
			- ゲームパッド入力
			- ゲームパッド速度指令コンポーネント
 +- IO_test		Zumo - Rasperry Pi 間の通信テスト用コンポーネント群
 +- sample		作例：ライントレーサー
- Zumo-rasp		Zumoロボット内制御プログラム (Raspberry Pi版 (GPIOシリアル通信））
- Zumo-win		Zumoロボット内制御プログラム（Windows版（Micro USBポート経由シリアル通信））
- CADData		ZumoロボットへのRaspberry Pi A+ 搭載用CADデータ
- Manual.pdf		利用マニュアル

これらの，フォルダ，ファイルを利用して，Zumoロボットのアプリケーションソフトウェアの開発が行えます．

以上