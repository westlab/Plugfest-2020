#include<unordered_map>
#include<iostream>
#include<string>
#include"middle.h"
using namespace std;

//export to C

void *get_middle(){
    Middle *ret = new (nothrow) Middle();
    if(ret==NULL) {
        printf("middle struct allocation failed\n");
        exit(1);
    }

    return (void*)ret;
}

void delete_middle(void *mid){
    free(mid);
    mid = NULL;
}

void add_data(void *mid, const char* key, const char* value) {
    Middle *m = (Middle*)mid;
    m->p[key]=value;
}


int get_data(void *mid, const char** dst, const char* key){
    Middle *m = (Middle*)mid;
    auto itr = m->p.find(key);
    if(itr == m->p.end()) return GET_DATA_FAIL;
    *dst = itr->second.c_str();
    return GET_DATA_SUCCESS;
}



