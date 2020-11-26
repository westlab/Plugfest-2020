gpp = g++ -std=c++17 -O3 -I /usr/include/boost
cflag = -mmacos-version-min=10.16

all: convert parse_only json_parser

extern_c: c_main.o middle.o convert_fromC.o parser.o reverse_poland.o my_utilities.o
	$(gpp) -o a.out c_main.o middle.o convert_fromC.o parser.o reverse_poland.o my_utilities.o

convert: main.o sniff.o parser.o reverse_poland.o my_utilities.o
	$(gpp) -o convert_full.out main.o sniff.o parser.o reverse_poland.o my_utilities.o -l pcap

parse_only: convert_only.o parser.o reverse_poland.o my_utilities.o
	$(gpp) -o convert_part.out convert_only.o parser.o reverse_poland.o my_utilities.o -l pcap

json_parser: parse_json.o my_utilities.o
	$(gpp) -o json_parser.out parse_json.o my_utilities.o

main.o: main.cpp
	$(gpp) -c main.cpp -l pcap

c_main.o: c_main.c
	gcc $(cflag) -c c_main.c

convert_fromC.o: convert_fromC.cpp
	$(gpp) -c convert_fromC.cpp

middle.o: middle.cpp
	$(gpp) -c middle.cpp

sniff.o: sniff.cpp
	$(gpp) -c sniff.cpp

parser.o: parser.cpp
	$(gpp) -c parser.cpp 

reverse_poland.o: reverse_poland.cpp
	$(gpp) -c reverse_poland.cpp

my_utilities.o: my_utilities.cpp
	$(gpp) -c my_utilities.cpp

convert_only.o: convert_only.cpp
	$(gpp) -c convert_only.cpp

parse_json.o: parse_json.cpp
	$(gpp) -c parse_json.cpp

clean:
	rm *.o
