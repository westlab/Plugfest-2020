//
//
#include <iostream>
#include <string>
#include <cstring>
#include <netinet/ip.h>
#include <netinet/ip6.h>
#include <netinet/udp.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

//multi thread
#include <chrono>

#include "convert.h"

#ifndef __FAVOR_BSD
# define __FAVOR_BSD
#endif

using namespace std;


void ipv4_process(char *p,string& srcip,string& dstip,int& len,int& tp){
    struct ip *ip;

    ip = (struct ip *)p;
    srcip=inet_ntoa(ip->ip_src);
    dstip=inet_ntoa(ip->ip_dst);
    len=ip->ip_hl*4;
    tp=ip->ip_p;
}

void ipv6_process(char *p,string& srcip,string& dstip,int& iplength){ //諦め
    struct ip6_hdr *ip;
    char str_buffer[INET6_ADDRSTRLEN];
    ip = (struct ip6_hdr *)p;
    inet_ntop(AF_INET6,&(ip->ip6_src),str_buffer, sizeof(ip->ip6_src));

    //dstip=ip->ip6_dst;
}

void tcp_process(char *p, int& srcport, int& dstport, int& len){
    struct tcphdr *tcp;
    tcp=(struct tcphdr*)p;

    srcport=ntohs(tcp->th_sport);
    dstport=ntohs(tcp->th_dport);
    //len=ntohs(tcp->th_off);
    len=tcp->th_off*4;
    //printf("tcplen:%d\n",len);

}

void udp_process(char *p, int& srcport, int& dstport, int& len){
    struct udphdr *udp;
    udp=(struct udphdr*)p;

    srcport=ntohs(udp->uh_sport);
    dstport=ntohs(udp->uh_dport);
    len=ntohs(udp->uh_ulen);
}

unsigned char* sub_packet(const unsigned char *data_buffer,const unsigned int length, int start){ //使わない
    //unsigned char* ret=data_buffer.sub;
    int N=length-start;
    cout<<length<<"-"<<start<<" = "<<length-start<<endl;
    unsigned char d[length-start+1]={0};
    for(int i=0;i<length-start;++i){
        d[i]=*(data_buffer+start+i);
    }
    //printf("%x\n",d[N]);
    unsigned char* ret=(unsigned char*)d;
    //cout<<ret<<endl;
    printf("1stbyte: %x\n",ret[0]);
    //printf("%d:%x %x\n",N,ret[0],ret[N-1]);
    return ret;
}

void convert_after_general(string protocol){
    chrono::system_clock::time_point start, end; //timing
    string from_general="commands/"+protocol+"_from_general.txt";
    string send="commands/"+protocol+"_send.txt";
    start = chrono::system_clock::now();
    bool is_convert=convert(2,from_general);
    if(is_convert) {
        //mt.unlock();
        //this_thread::sleep_for(chrono::microseconds(10000));
        //convert(3,send);
        string command="./parse_only 3 "+send;
        system(command.c_str());
        
        end = chrono::system_clock::now();
        double time=static_cast<double>(chrono::duration_cast<chrono::microseconds>(end - start).count() / 1000.0); //経過時間
        printf("%s : %.3f ms\n",protocol.c_str(),time);
    }else{
        //mt.unlock();
    }
    
}

void dump(const unsigned char *data_buffer, const unsigned int length,const char *device) {
    int start=0;

    //ethernet layer
    if(!strcmp(device,"lo0")){
        start+=4;
    }else{
        start+=14;
    }

    //IP layer
    int iplength,tptype;
    string srcip,dstip;
    if(data_buffer[start]>>4==4){ //ipv4
        ipv4_process((char *)(data_buffer+start),srcip,dstip,iplength,tptype);
    }else{ //ipv6
        iplength = 40;
        tptype = (int)data_buffer[start+6];
        srcip="::1"; dstip="::1"; //手抜き
    }

    start+=iplength;

    //trance port layer
    int srcp,dstp,tplength;
    if(tptype==IPPROTO_TCP){ //TCP
        tcp_process((char *)(data_buffer+start),srcp,dstp,tplength);
        //tplength=(int)(data_buffer[start+12]>>4)*4;
    }else if(tptype==IPPROTO_UDP){ //UDP
        //cout<<"called"<<endl;
        udp_process((char *)(data_buffer+start),srcp,dstp,tplength);
        tplength=8;
    }else{
        return;
    }
    string srcport=to_string(srcp),dstport=to_string(dstp);

    start+=tplength;

    //application
    if(dstport=="1883"){ //MQTT
        if(convert(0,"commands/mqtt_parse.txt",data_buffer+start,length-start,srcip,dstip,srcport,dstport)&&convert(1,"commands/mqtt_to_general.txt")){
            if(convert(2,"commands/xmpp_from_general.txt")){
	        convert(3,"commands/xmpp_send.txt");
	    }
        }
    }

}
