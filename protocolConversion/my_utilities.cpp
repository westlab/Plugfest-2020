#include <iostream>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <regex>
#include <algorithm>
#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>

using namespace std;

vector<string> space_split(const string& src,const bool ignore_quote,const char dlim) { //空白区切り
    vector<string> ret;
    string tmp;
    string::size_type len = src.length();
    bool inner_quote=false; //" "内では無視しない
    for(int i=0;i<len;++i){
        if(src[i]==' '&&!inner_quote&&i>0&&src[i-1]!='\\'){
            if(!tmp.empty()) ret.push_back(tmp);
            tmp.clear();
        }else if(src[i]=='"'){
            if(!ignore_quote) tmp.push_back(src[i]);
            if(inner_quote){
                if(!tmp.empty()) ret.push_back(tmp);
                tmp.clear();
            }
            inner_quote^=1; //反転
        }else tmp.push_back(src[i]);
    }
    if(!tmp.empty()) ret.push_back(tmp);
    return ret;
}

vector<string> space_split_regex(const string& src,const bool ignore_quote,const char dlim) { //空白区切り
    vector<string> ret;
    string tmp;
    string::size_type len = src.length();
    //bool inner_quote=false; //" "内では無視しない
    for(int i=0;i<len;++i){
        if(src[i]==' '&&i>0&&src[i-1]!='\\'){
            if(!tmp.empty()) ret.push_back(tmp);
            tmp.clear();
        }else tmp.push_back(src[i]);
    }
    if(!tmp.empty()) ret.push_back(tmp);
    return ret;
}

vector<string> split_statement(const string& src){
    vector<string> ret;
    string var,str;
    string::size_type len = src.length();
    bool inner_quotation=false,var_name=false; //""内では無視しない
    for(int i=0;i<len;++i){
        if(src[i]==' '&&!inner_quotation){
            if(!str.empty()) ret.push_back(str);
            str.clear();
        }else if(src[i]=='$'&&!inner_quotation){
            if(!str.empty()) ret.push_back(str);
            str.clear();
            smatch variable;
            string tmp=src.substr(i);
            if(regex_search(tmp,variable,regex(R"(^\$\w+)"))){
                ret.push_back(variable[0].str());
                i+=variable[0].str().size()-1;
            }
        }else if(src[i]=='"'){
            if(inner_quotation){
                if(!str.empty()) ret.push_back(str);
                str.clear();
            }
            inner_quotation^=1;
        }else{ 
           if(inner_quotation) str.push_back(src[i]);
           else{
               if(src[i]=='+'||src[i]=='?'||src[i]==':'||src[i]=='{'||src[i]=='}'||src[i]==','||(src[i]=='>'&&src[i+1]!='=')||(src[i]=='<'&&src[i+1]!='=')||(src[i]=='!'&&src[i+1]!='=')){
                   
                   if(!str.empty()) ret.push_back(str);
                   str.clear();
                   ret.push_back(string{src[i]});
               }else if(src[i]=='#'){ //コメント
                   break;
               }else if(src[i]=='='){
                   if(i>0&&(src[i-1]=='<'||src[i-1]=='>'||src[i-1]=='!')){
                       str.push_back(src[i]); ret.push_back(str); str.clear();
                       continue;
                   }
                   if(!str.empty()) ret.push_back(str);
                   str.clear();
                   if(src[i+1]=='='){
                   ret.push_back(string{"=="});
                   ++i;               
                   }else{
                       ret.push_back(string{src[i]});
                   }
               }else if(src[i]=='-'&&(src[i+1]=='>'||src[i+1]=='e')){
                   if(!str.empty()) ret.push_back(str);
                   str.clear();
                   string tmp{src[i]};
                   tmp.push_back(src[i+1]);
                   ret.push_back(tmp);
                   ++i;
               }else{
                   str.push_back(src[i]);
               }
           }
        }
    }
    if(!str.empty()) ret.push_back(str);
    return ret;
}

string merge_string(vector<string> strs,int start,int end){ //文字列結合
    end=min(end,(int)strs.size());
    string ret;
    for(int i=start;i<end;++i) ret+=strs[i];
    return ret;
}

int bit_extraction(const unsigned char byte,int start,int end){ //bit列を抽出する
    unsigned char mask=0;
    for(int i=0;i<8;++i){
        mask=mask<<1;
        if(i>=start&&i<end) mask+=1;
    }
    return (byte&mask)>>(8-end);
}


vector<string> sub_vector(vector<string> src,int start,int end){
    end=min(end,(int)src.size());
    vector<string> ret;
    for(int i=start;i<end;++i){
        ret.push_back(src[i]);
    }
    return ret;
}

string str_replace(string src,string target,string replacement){
   if(!target.empty()){
        string::size_type pos = 0;
        while((pos=src.find(target,pos))!=string::npos){
            src.replace(pos,target.length(),replacement);
            pos += replacement.length();
        }
   }
   return src;
}

//#define DEBUG
#ifdef DEBUG
int main(){
    string src="$_ = 2";
    src=str_replace(src,"$_","$abc");
    cout<<src<<endl;
}
#endif
