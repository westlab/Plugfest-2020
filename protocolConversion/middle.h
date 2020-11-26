#ifndef MIDDLE_H
#define MIDDLE_H

#ifdef __cplusplus

#include<unordered_map>
#include<string>
using namespace std;

struct Middle{
    unordered_map<string, string> p;
};

extern "C" {
#endif //__cplusplus



const int GET_DATA_SUCCESS = 1;
const int GET_DATA_FAIL = 0;

void *get_middle();
void delete_middle(void*);

void add_data(void*, const char*, const char*);
int get_data(void*,const char**, const char*);

void *convert_fromC(const unsigned char*, int, const char*, const char*);

#ifdef __cplusplus
}
#endif //__cplusplus


#endif //MIDDLE_H
