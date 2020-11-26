# procotol conversion called from C

## はじめに
プロトコル変換をC言語の実装から呼び出し、変換後のデータを構造体で返す拡張です。

`c_main.c`がサンプルコードです。

## 使い方
呼び出し元において`#include "middle.h"`でインクルードします。

`middle.h`で定義されている。関数は次の通りです。

* `void *get_middle()` Middle構造体を生成し、ポインタを返します。
* `void delete_middle(void *mid)` Middle構造体ポインタを解放します。
* `void add_data(void *mid, const char* key, const char* value)` Middleにあるmapにデータを追加します
* `int get_data(void *mid, const char** dst, const char* key)` Middleにあるmapからデータを取得します。値がある場合は`GET_DATA_SUCCESS`を、ない場合は`GET_DATA_FAIL`を返します。
* `void *convert_fromC(const unsigned char* l7data, int packet_length, const char* srcprotocol, const char* targetprotocol)` 変換を行い、Middleのポインタを返します。変換されなかった場合は`NULL`を返します。

## ビルド
`Makefile`から抜粋。

```
gpp = g++ -std=c++17 -O3 -I /usr/include/boost
cflag = -mmacos-version-min=10.16

extern_c: c_main.o middle.o convert_fromC.o parser.o reverse_poland.o my_utilities.o
	$(gpp) -o a.out c_main.o middle.o convert_fromC.o parser.o reverse_poland.o my_utilities.o

c_main.o: c_main.c
	gcc $(cflag) -c c_main.c

convert_fromC.o: convert_fromC.cpp
	$(gpp) -c convert_fromC.cpp

middle.o: middle.cpp
	$(gpp) -c middle.cpp

parser.o: parser.cpp
	$(gpp) -c parser.cpp 

reverse_poland.o: reverse_poland.cpp
	$(gpp) -c reverse_poland.cpp

my_utilities.o: my_utilities.cpp
	$(gpp) -c my_utilities.cpp
```

## 注意点
Macでビルドした時は、コンパイルとリンクでバージョンが違ったことでリンクが正常にできなかったため、`-mmacos-version-min=10.16`をつけました。

環境によってはバージョンの指定を行う必要があるかもしれません。
