#include<pcap.h>
#include<string>
#include "sniff.h"
using namespace std;

int main(int argc, char *argv[]) {
    char *device;
    if(argc==1){
        device="wlp2s0";
    }else{
        device=argv[1];
    }

    struct pcap_pkthdr header;
    const u_char *packet;
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *pcap_handle;

    if (device == NULL) {
        printf("error1\n");
        return 1;
    }
    printf("device = %s\n", device);

    pcap_handle = pcap_open_live(device, 4096, 1, 10, errbuf);
    if (pcap_handle == NULL) {
        printf("error2\n");
        return 1;
    }

    for (int i = 0; i > -1;) {
        packet = pcap_next(pcap_handle, &header);
        if(header.len>30000||!packet) continue;
        dump(packet, header.len, device);
        ++i;
    }

    pcap_close(pcap_handle);

    return 0;
}
