#include <iostream>
#include <string>

#include "convert.h"

using namespace std;

int main(int argc, char *argv[]){
    string file_name=argv[2];
    int convert_type=stoi(argv[1]);

    convert(convert_type,file_name);
    return 0;
}