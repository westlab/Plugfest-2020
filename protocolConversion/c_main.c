#include "middle.h"
#include "stdio.h"

int main () {
    //MQTT publish topic = "test", message = "abc"
    const unsigned char data[]= {0x30, 0x09, 0x00, 0x04, 0x74, 0x65, 0x73, 0x74, 0x61, 0x62, 0x63};
    void* mid = convert_fromC(data,sizeof(data),"mqtt","xmpp");
    if(mid==NULL){
        printf("failed\n");
        return 0;
    }
    const char* value;
    int is_find = get_data(mid, &value, "node");
    if(is_find) printf("%s\n", value); 
    delete_middle(mid);
    return 0;
}
