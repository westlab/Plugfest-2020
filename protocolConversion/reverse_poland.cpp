#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include <stack>
#include <math.h>
#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string/split.hpp>

bool string2int(std::string str,int &i){
    int tmp;
    try{
      tmp=std::stoi(str);
    }catch (const std::invalid_argument& e) {
        return 0;
    }
    i=tmp;
    return 1;
}

bool is_num(std::string str){
    try{
      std::stoi(str);
    }catch (const std::invalid_argument& e) {
        return 0;
    }
    return 1;
}

int operate(std::stack<std::string> &st,std::string ope){
    int num;
    if(string2int(ope,num)){ //数値に変換できるか
        st.push(ope);
    }else{ //記号の場合
        if(st.size()<2) return 1;
        std::string a,b;
        a=st.top(); st.pop();
        b=st.top(); st.pop();
        int ai,bi;
        if(string2int(a,ai)&&string2int(b,bi)){
          int ans;
          if(ope=="+"){
            ans=bi+ai;
          }else if(ope=="-"){
            ans=bi-ai;
          }else if(ope=="*"){
            ans=bi*ai;
          }else if(ope=="/"){
            ans=bi/ai;
          }else if(ope=="**"){
            ans=pow(bi,ai);
          }else return 1;
          st.push(std::to_string(ans));
        }else return 1;
    }
    return 0;
}

int reverse_poland(std::vector<std::string> operand,int &ans){
    std::stack<std::string> st;
    for(std::string ope:operand){
        if(operate(st,ope)) return 1;
    }
    if(st.size()!=1) return 1;
    int tmp;
    if(!string2int(st.top(),tmp)) return 1;
    ans=tmp;
    return 0;
}

int reverse_poland(std::string statement,int &ans){ //stringで来たらvectorに分解して渡す
    std::vector<std::string> operand,tmp;
    boost::algorithm::split(tmp,statement,boost::is_any_of(" "));
    for(std::string s:tmp) if(s!="") operand.push_back(s);
    return  reverse_poland(operand,ans);
}

int rank(std::string ope){
    if(ope=="**") return 5;
    else if(ope=="*"||ope=="/") return 10;
    else if(ope=="+"||ope=="-") return 20;
    else return 99;
}

int to_rev_poland(std::vector<std::string> operand,std::vector<std::string>& ans){
    std::stack<std::string> st;
    for(std::string s:operand){
      if(s=="") continue;
      int num;
      if(is_num(s)){
          ans.push_back(s);
      }else if(s==")"){
          if(st.empty()) return 1;
          while(st.top()!="("){
              ans.push_back(st.top());
              st.pop();
              if(st.empty()) return 1;
          }
          st.pop();
      }else if(s=="("){
          st.push("(");
      }else{
          while(true){
              if(st.empty()){
                  st.push(s);
                  break;
              }
              if(rank(s)<=rank(st.top())){
                  st.push(s);
                  break;
              }
              ans.push_back(st.top());
              st.pop();
          }
      }
    }

    while(!st.empty()){
        ans.push_back(st.top());
        st.pop();
    }
    return 0;
}

int to_rev_poland(std::string statement,std::vector<std::string>& ans){
    std::vector<std::string> operand;
    std::stack<std::string> st;
    boost::algorithm::split(operand,statement,boost::is_any_of(" "));
    return to_rev_poland(operand,ans);
}

int calc (std::vector<std::string> args,int& ans){
    std::vector<std::string> tmp;
    if(to_rev_poland(args,tmp)){
        std::cerr<<"invalid syntax"<<std::endl;
        return 1;
    }
    return reverse_poland(tmp,ans);
}

int calc(std::string input,int& ans){
    std::vector<std::string> args;
    std::string tmp;
    for(char s:input) {
        if(s==' ') continue;
        if(s>='0'&&s<='9') tmp.push_back(s); //数字の場合
        else{
            if(!tmp.empty()) {
              args.push_back(tmp);
              tmp.clear();
            }
            std::string tmp{s};
            args.push_back(tmp);
        }
    }
    if(!tmp.empty()) {
        args.push_back(tmp);
        tmp.clear();
    }
    if(args[0]=="-"){ //最初が"-5"などの場合の処理
      args[0]+=args[1];
      args.erase(args.begin()+1);
    }
    //for(std::string str:args) std::cout<<str<<std::endl;
    calc(args,ans);
    return 0;
}

//#define DEBUG
#ifdef DEBUG
int main(){
    std::string S;
    getline(std::cin,S);
    int ansa;
    calc(S,ansa);
    std::cout<<ansa<<std::endl;
    return 0;
}
#endif