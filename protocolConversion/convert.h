#ifndef CONVERT_H
#define CONVERT_H
#include <string>
bool convert(int convert_type,const std::string read_file_name,const unsigned char* data={},
    const int packet_length=0,std::string srcip="",std::string dstip="",std::string srcport="",std::string dstport="", void *middle=NULL);
#endif //CONVERT_H