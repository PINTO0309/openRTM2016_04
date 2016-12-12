README

甲南大学知能情報学部
2016/10/31
2016/12/10 アップデートにあわせて改訂
2016/12/12 作例：ライントレーサーのアップデート，利用マニュアルの改訂，Zumo通信プロトコル解説マニュアルの追加

このフォルダには，RTミドルウェアコンテスト2016に参加している「ZumoとRaspberry Piを用いた教育用ロボット環境」の作品データが保存されています．作品は以下のフォルダ，ファイルから構成されています．

(1) Zumo ロボット用 RT Component群
　　(a) 基本コンポーネント
    (b) ゲームパッド入力コンポーネント
    (c) ゲームパッド速度指令コンポーネント
    (d) Zumo-Raspberry Pi間通信テスト用コンポーネント群
    (e) 作例：ライントレーサー
(2) Zumo ロボット内制御プログラム (Micro USBポート接続版(通常はこちらを使用), GPIO接続版(Raspberry Pi A+用)）
(3) Zumo基板上にRaspberry Piを搭載するためのCADデータ
(4) Zumoロボットの利用マニュアル

(2)のロボット内制御プログラムは，Zumoロボット基板上のMicro USBポート経由でのシリアル通信（通常はこちらを使用）と，Zumoロボット基板上のGPIOシリアル通信を利用の場合（Raspberry Pi A+を想定）の2種類があります．通常はMicro USBポート経由のプログラムを用いますが，ご使用の環境に応じて，プログラムを使い分ける必要があります．

フォルダ，ファイルの一覧は以下のとおりです．

- README.txt		README
- ZumoComponents	Pololu Zumo 32U4 RTコンポーネント群
			- 基本コンポーネント
			- ゲームパッド入力
			- ゲームパッド速度指令コンポーネント
 +- IO_test		Zumo - Rasperry Pi 間の通信テスト用コンポーネント群
 +- sample		作例：ライントレーサー
- Zumo-USB		Zumoロボット内制御プログラム（Micro USBポート経由シリアル通信版，通常はこちらを使用）
- Zumo-GPIO		Zumoロボット内制御プログラム (GPIOシリアル通信版）
- CADData		ZumoロボットへのRaspberry Pi マイクロコントローラ搭載用CADデータ
- Manual.pdf		利用マニュアル
- ZumoCommunicationProtocol_Manual.pdf  Zumo通信プロトコル解説マニュアルの追加
これらの，フォルダ，ファイルを利用して，Zumoロボットのアプリケーションソフトウェアの開発が行えます．

以上