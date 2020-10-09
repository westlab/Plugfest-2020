# Protocol Conversion

## 使用ライブラリ
boost 1.73.0
libpcap (バイト列を入力とする場合は入力不要)

## ディレクトリ・ファイル構成
```
.
├ rule_json/  //jsonの変換ルール記述ファイル
├ commands/  //rule_jsonのファイルを変換したもの
├ ref //変換時の参照ファイル
├ sample/  //中間ファイルの例
├ update.sh  //rule_jsonのファイルからcommandを生成する
```

## 実行ファイル生成
`make all`で生成

* convert_full.out ... lo0インターフェイスをキャプチャリングしてXMPPのpubsubからMQTT, CoAP, SMTPに変換する。
* convert_part.out ... `./parse_only.out 1 sample/mqtt_src.json`の形式で実行。数字はgeneralへの変換が`1`,generalからの変換が`2`
* json_parser.out ... `./json_parser.out <json file name> <text file name>`の形式で実行。update.shで使用

## 使用方法
jsonのルール記述ファイルの書き方はすでにあるファイルや、論文等を参考してください。整理ができたら追記します。

`./update.sh`でコマンドファイルを生成します。JSONを更新したら、実行してください。

## Plugfestでの実行方法
### プロトコル変換処理の起動
NIC（デフォルトはwlp2s0）を通るパケットをキャプチャして変換する処理を起動する。MQTTブローカと同じマシンで動かす。
```bash
$ make
$ protocolconversion/convert_full.out
```
### XMPPサーバの起動
xmppserver(ejabberd)を起動（停止）する場合、
```bash
$ sudo /opt/ejabberd-20.07/bin/ejabberdctl start(stop)
```

xmppserver(ejabberd)を起動してログをリアルタイムで表示させる場合、
```bash
$ sudo /opt/ejabberd-20.07/bin/ejabberdctl live
```
ctrl+Cで止めても、サーバは動き続けることに注意

※起動中は `http://192.168.0.40:5280/admin/` で管理画面に入れる。管理者アカウントはIDが`admin`、パスワードはドク系

### XMPPクライアントの実行
予めsubscribeするnodeを登録しておく。
```bash
$ /home/demo/slixmpp/examples/pubsub_client.py pubsub.192.168.0.40 subscribe Plugfest/keio/sensor/1/TEMP -j client@192.168.0.40 -p clientpass
```
listenして、subscribeしているノードにパブリッシュされたら受け取って表示する。
```bash
$ /home/demo/slixmpp/examples/pubsub_events.py -j client@192.168.0.40 -p clientpass
```

## TO DO?
conversion(const unsigned char *data, const string srcProtocol, const vector\<string\> &dstProtocol)で変換して、送るライブラリを作る？

