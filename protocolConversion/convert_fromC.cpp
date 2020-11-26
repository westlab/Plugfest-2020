#include "convert.h"
#include "middle.h"
#include <iostream>
#include <string>
using namespace std;


void *convert_fromC(const unsigned char* l7data, int packet_length, const char* srcprotocol, const char* targetprotocol){
    void* ret = get_middle();
    //to general
    string srcpstr = srcprotocol, tarpstr = targetprotocol;
    string parse_name = "commands/"+srcpstr+"_parse.txt";
    string to_general_name = "commands/"+srcpstr+"_to_general.txt";
    string form_general_name = "commands/"+tarpstr+"_from_general.txt";

    if(convert(0,parse_name,l7data, packet_length,"","","","")&&convert(1,to_general_name)){
      if(convert(2,form_general_name,{},0,"","","","",ret)) return ret;
    }
    return NULL;
}
