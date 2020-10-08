gpp = g++ -std=c++17 -O3 -I /usr/include/boost

all: convert parse_only json_parser

convert: main.o sniff.o parser.o reverse_poland.o my_utilities.o
	$(gpp) -o convert_full.out main.o sniff.o parser.o reverse_poland.o my_utilities.o -l pcap

parse_only: convert_only.o parser.o reverse_poland.o my_utilities.o
	$(gpp) -o convert_part.out convert_only.o parser.o reverse_poland.o my_utilities.o -l pcap

json_parser: parse_json.o my_utilities.o
	$(gpp) -o json_parser.out parse_json.o my_utilities.o

main.o: main.cpp
	$(gpp) -c main.cpp -l pcap

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
