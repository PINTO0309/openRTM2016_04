2016/12/12(月曜日)

このスクリプト群はRaspberry Piの起動時にスイッチ一つで各コンポーネントを起動できるようにするためのプログラムです。
このスクリプト群を使うにあたり、各プログラムの配置場所に注意してください。

各プログラムの説明です。
・ActiveComp.py
スイッチの入力を感知すると、Zumo.py、LineTracer.pyを立ち上げRTShellでコンポーネントの接続、コンフィグの変更、コンポーネントのアクティブを行います。場所は/home/pi/においてください。

・DeactiveComp.py
スイッチの入力を感知すると、Zumo.py、LineTracer.pyをexitし、Zumoを止めます。場所は/home/pi/においてください。

・runZumo.sh,stopZumo.sh
それぞれActiveComp.py、DeactiveComp.pyを動かすためのシェルファイルです。場所は/etcにおいてください。

・rc.local
Raspberry Pi の/etc/に存在するファイルです。このスクリプトを置きかえることで起動時に自動でActiveComp.py,DeactiveComp.pyが起動し、スイッチを押すだけでコンポーネントが立ち上がりZumoが動き始めます。

なお、配置場所を変える際には適宜スクリプトファイルを書き換えてください。