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

## TO DO?
conversion(const unsigned char *data, const string srcProtocol, const vector\<string\> &dstProtocol)で変換して、送るライブラリを作る？

