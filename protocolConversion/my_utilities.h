#ifndef MY_UTILITIES_H
#define MY_UTILITIES_H
#include <vector>
#include <string>
std::vector<std::string> space_split(const std::string& src,const bool ignore_quote=true,const char dlim=' ');
std::vector<std::string> space_split_regex(const std::string& src,const bool ignore_quote=true,const char dlim=' ');
std::vector<std::string> split_statement(const std::string&);
std::string merge_string(std::vector<std::string> strs,int start=0,int end=INT32_MAX);
int bit_extraction(const unsigned char byte,int start=0,int end=8);
std::vector<std::string> sub_vector(std::vector<std::string> src,int start=0,int end=INT32_MAX);
std::string str_replace(std::string,std::string,std::string);
#endif