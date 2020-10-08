#include <iostream>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <regex>
#include <algorithm>
#include <chrono>

#include "json.h"
#include "calc.h"
#include "my_utilities.h"
using namespace std;

unordered_map<string,int> int_variable;
unordered_map<string,string> str_variable;
unordered_map<string,string> ref_tags;

bool skip=false;
stack<int> for_stack; //何行目からループが始まっているか
stack<int> if_stack; 
unordered_set<string> comp_opes={"==","!=","<",">","<=",">=","regmatch","-e"};

string get_value(string tag,string json_file_name){
    ptree ref_json;
    read_json(json_file_name,ref_json);
    if(boost::optional<string> tmp =ref_json.get_optional<string>(tag)){
        return tmp.get();
    }else{
        return "";
    }

}

string get_variable_type(string str){
    auto itr_int=int_variable.find(str);
    if(itr_int!=int_variable.end()){
        return "int";
    }
    auto itr_str=str_variable.find(str);
    if(itr_str!=str_variable.end()){
        return "string";
    }
    cout<<"no matching variable"<<endl;
    exit(1);
}

bool find_variable(string str,string& ret){
    int end_packet;
    auto itr_int=int_variable.find(str);
    if(itr_int!=int_variable.end()){
        ret=to_string(itr_int->second);
        return 1;
    }
    auto itr_str=str_variable.find(str);
    if(itr_str!=str_variable.end()){
        ret=itr_str->second;
        return 1;
    }
    return 0;
}

void find_variable(vector<string>& ope,int start=0,int end=INT32_MAX){
    end=min(end,(int)ope.size());
    string tmp;
    for(int i=start;i<end;++i){
        if(ope[i][0]!='$') continue;
        const string key = ope[i].substr(1);
        if(find_variable(key,tmp)) ope[i]=tmp;
    }
}

bool mono_evaluate(vector<string> ope){
    string comp_ope;
    int comp_ope_place;
    bool is_int=true;
    for(int i=0;i<ope.size();++i) {
        if(comp_opes.find(ope[i])!=comp_opes.end()){
            comp_ope=ope[i];
            comp_ope_place=i;
        }
    }

    if(comp_ope=="-e"){
        string waste;
        return find_variable(ope[comp_ope_place+1].substr(1),waste);
    }

    find_variable(ope); //変数を置換
    for(int i=0;i<ope.size();++i) {
        if(i!=comp_ope_place&&!is_num(ope[i])) is_int=false; //手抜き判定
    }
    vector<string> left,right;
    copy(ope.begin(),ope.begin()+comp_ope_place,back_inserter(left));

    copy(ope.begin()+comp_ope_place+1,ope.end(),back_inserter(right));
    
    if(is_int){ //数値評価
        int left_value,right_value;
        calc(left,left_value); calc(right,right_value);
        if(comp_ope=="==") if(left_value==right_value) return true; else return false;
        else if(comp_ope=="!=") if(left_value!=right_value) return true; else return false;
        else if(comp_ope=="<") if(left_value<right_value) return true; else return false;
        else if(comp_ope=="<=") if(left_value<=right_value) return true; else return false;
        else if(comp_ope==">=") if(left_value>=right_value) return true; else return false;
        else if(comp_ope==">") if(left_value>right_value) return true; else return false;
    }
    string left_str="",right_str="";
    for(int i=0;i<left.size();i+=2) left_str+=left[i];
    for(int i=0;i<right.size();i+=2) right_str+=right[i];
    if(comp_ope=="==") if(left_str==right_str) return true; else return false;
    else if(comp_ope=="!=") {
        //cout<<left_str<<":"<<right_str<<endl;
        if(left_str!=right_str) return true; else return false;
    }
    
    else if(comp_ope=="regmatch"){
        regex test(right_str);
        smatch tmp;
        if(regex_search(left_str,tmp,test)) return true;
        else return false;
    }
    return false;
}

bool evaluate(const vector<string> &ope){ //条件判定
    vector<string> tmp,operand;
    vector<bool> bools;
    bool is_not=false;
    for(int i=0;i<ope.size();++i){
        if(ope[i]=="and"||ope[i]=="or"){
            operand.push_back(ope[i]);
            bools.push_back(mono_evaluate(tmp)^is_not);
            tmp.clear();
            is_not=false;
            if(ope[i]=="and"&&!bools.back()) return false;
            if(ope[i]=="or"&&bools.back()) return true;
        }else if(ope[i]=="not"){
            is_not=true;   
        }
        else tmp.push_back(ope[i]);
    }
    bools.push_back(mono_evaluate(tmp)^is_not);
    if(bools.size()==1) return bools[0];
    bool ret;
    if(operand[0]=="and") ret=bools[0]&bools[1];
    else ret=bools[0]|bools[1];
    for(int i=1;i<bools.size()-1;++i){
        if(operand[i]=="and") ret&=bools[i+1];
        else ret|=bools[i+1];
    }
    return ret;
}

bool matching_record(const ptree &record,vector<pair<int,string>> ref_tags,vector<string> condition){
    for(auto tags:ref_tags){
        if(boost::optional<string> tmp=record.get_optional<string>(tags.second)){
            condition[tags.first]=tmp.get();
        }else{
            return false;
        }
    }
    return evaluate(condition);
}

bool reference(const vector<string> &ope,string& ret,string process_type){ //表参照
    //find_variable済
    string ref_file_name=ope[0];
    smatch file_name_results;
    if(regex_match(ref_file_name,file_name_results,regex(R"(([\w|_]*)(.json)?)")))  ref_file_name=file_name_results[1].str()+".json";
    ptree ref_json;
    ifstream ref_file_check(ref_file_name);
    if(ref_file_check.is_open()) read_json(ref_file_name,ref_json);
    else {cerr<<"reference error"<<endl; exit(1);}

    vector<string> conditions;
    string get_title,no_matching_string="";
    vector<pair<int,string>> ref_tags; //参照する必要のあるタグを格納
    int ptr;
    for(ptr=2;ptr<ope.size();++ptr){
        if(ope[ptr]=="?") break;
        conditions.push_back(ope[ptr]);
        auto itr=comp_opes.find(ope[ptr]);
        if (itr!=comp_opes.end()){
            ref_tags.push_back(make_pair(ptr-3,ope[ptr-1]));
        }
    }
    get_title=ope[ptr+1]; //文字列を結合する必要が出てきたら書き換える
    ptree data;
    if(ptr+3<ope.size()) no_matching_string=ope[ptr+3];
    BOOST_FOREACH (const ptree::value_type& child, ref_json.get_child("data")) {
        const ptree& record = child.second;
        if(matching_record(record,ref_tags,conditions)){
            if(process_type=="assign"){
                if (boost::optional<string> target = record.get_optional<string>(get_title)) {
                    ret=target.get(); return true;
                }
            }
        }else{
            if(process_type=="erase"){
                data.push_back(make_pair(child.first,child.second));
            }
        }
    }
    if(process_type=="erase"){
        //cout<<"called"<<endl;
        ref_json.erase("data");
        ref_json.add_child("data",data);
        write_json(ref_file_name,ref_json);
        return true;
    }
    ret=no_matching_string;
    return true;
}

void def_process(const unsigned char* databuffer,vector<string> ope){ //変数定義
    int ope_num=ope.size();
    if(ope_num==1) return;

    const string variable_type = ope[0];
    const string variable_name = ope[1].substr(1); //'$'を取り除く
    if(ope_num<4){ //初期化なし
        if(variable_type=="int"){//int
            int_variable[variable_name]=0;
        }else{ //string
            str_variable[variable_name]="";
        }
        return;
    }
    
    find_variable(ope,3); //変数の置換
    
    if(ope[2]=="="){ //四則演算代入
        if(variable_type=="string"){
            string tmp;
            for(int i=3;i<ope.size();i+=2) tmp+=ope[i];
            str_variable[variable_name]=tmp;
        }else{
            int ans;
            vector<string> tmp;
            for(int i=3;i<ope.size();i++) tmp.push_back(ope[i]);
            calc(tmp,ans);
            int_variable[variable_name]=ans;
        }
    }else if(ope[2]=="->"){ //byte抽出代入
        string formula=merge_string(ope,3);
        regex refer(R"(\[([\w|-|\+|\*|\/|\$]+)\](>([\w|-|\+|\*|\/|\$]+))?(:\[([\w|-|\+|\*|\/|\$]+)\])(>([\w|-|\+|\*|\/|\$]+))?)");
        smatch results;
        if (!regex_match(formula, results, refer)) return;
        string sbyte=results[1].str(),sbit=results[3].str(),ebyte=results[5].str(),ebit=results[7].str();
        int startbyte,startbit=0,endbyte,endbit=8;
        calc(sbyte,startbyte); 
        if(ebyte!="") calc(ebyte,endbyte); else endbyte=startbyte;
        if(sbit!="")calc(sbit,startbit);
        if(ebit!="")calc(ebit,endbit);

        if(variable_type=="string"){
            string tmp;
            for(int i=startbyte;i<endbyte;++i){
                char c=databuffer[i];
                tmp+=c;
            }
            str_variable[variable_name]=tmp;
        }else{
            int tmp;
            if(startbyte==endbyte) tmp=bit_extraction(databuffer[startbyte],startbit,endbit);
            else{
                tmp=bit_extraction(databuffer[startbyte],startbit);
                for(int i=startbyte+1;i<endbyte;++i){
                    tmp=tmp<<8;
                    tmp|=bit_extraction(databuffer[i]);
                }
            }
            int_variable[variable_name]=tmp;
        }
    }else if(ope[2]=="regex"){ //正規表現抽出
        find_variable(ope,4);
        string ref=ope[3]; //検索条件
        string target=ope[4]; //検索対象
        //cout<<ref<<endl;
        string ret="";
        regex condition(ref);
        int rank=0; //代入する文字列は何番目の一致文字列か
        //cout<<ref<<endl;
        //rankの計算
        vector<string> tmp;
        for(int i=5;i<ope.size();i++) tmp.push_back(ope[i]);
        if(!tmp.empty()/*&&variable_type=="int"*/) calc(tmp,rank);

        smatch results;
        regex_search(target,results,condition);
        if(rank<results.size()) ret=results[rank];
        if(variable_type=="int"){
            if(is_num(ret)) int_variable[variable_name]=stoi(ret);
            else exit(1);
        }else{
            str_variable[variable_name]=ret;
        }
    }else if(ope[2]=="ref"){
        string value;
        if(reference(sub_vector(ope,3,ope.size()),value,"assign")){
            if(variable_type=="int"){
                if(is_num(value)) int_variable[variable_name]=stoi(value);
                else exit(1);
            }else{
                str_variable[variable_name]=value;
            } 
        }else{
            if(variable_type=="int"){
                int_variable[variable_name]=0;
            }else{
                str_variable[variable_name]="";
            } 
        }
    }else if(ope[2]=="get"){
        string general_file=str_variable["input_json_name"];
        ifstream general_file_check(general_file);
        if(!general_file_check.is_open()) exit(1);
        ptree ref_json;
        read_json(general_file,ref_json);
        if(boost::optional<string> tmp =ref_json.get_optional<string>(ope[3])){
            if(variable_type=="int"){
                int_variable[variable_name]=stoi(tmp.get());
            }else{
                str_variable[variable_name]=tmp.get();
            }
        }else{
            if(variable_type=="int"){
                if(ope.size()==5) int_variable[variable_name]=stoi(ope[4]);
                else int_variable[variable_name]=0;
            }else{
                if(ope.size()==5) str_variable[variable_name]=ope[4];
                else str_variable[variable_name]="";
            }
        }
    }
}

void update_var(const unsigned char* databuffer,vector<string> ope){
    const string variable_name = ope[0].substr(1);
    const string variable_type = get_variable_type(variable_name);
    ope.insert(ope.begin(),variable_type);
    def_process(databuffer,ope);
}

void add_reference(vector<string> ope){
    find_variable(ope);
    string ref_file_name=ope[0];
    ptree record;
    for(int i=1;i<ope.size();++i){
        if(ope[i]=="}") break;
        if(ope[i]==":"){
            record.put(ope[i-1],ope[i+1]);
        }
    }
    ifstream file_open_check(ref_file_name);
    ptree table;
    if(file_open_check.is_open()) read_json(ref_file_name,table);
    else exit(1);
    ptree &data=table.get_child("data");
    data.push_back(make_pair("",record));
    write_json(ref_file_name,table);
}

string escape_str(string input){
    string ret = "";
    for(auto c:input){
        if(c=='\'') {
	    return ret;
	} else if(c=='!'||c=='$') {
	    return ret;
	} else if(c=='&') {
	    return ret;
	} else if(c=='%'){
	    return ret;
	} else if(c==0) {
	    continue;
	} else {
	    ret+=c;
	}
    }
    return ret;    
}

void os_process(vector<string> ope){ //いろいろ適当なので今後修正予定
    find_variable(ope);
    //cout<<"called"<<endl;
    string command="";
    for(string s:ope) {
        if(regex_match(s,regex(R"(\||<{1,2}|2?>{1,2}(&1)?|&>)"))) command+=s+" ";
        else if(s=="") continue;
        else command+="'"+escape_str(s)+"' ";
    }
    //command+=" > /dev/null";
    //cout<<"process "<<command.c_str()<<endl;
    chrono::system_clock::time_point start, end; //timing
    start = chrono::system_clock::now();
    system(command.c_str());
    end = chrono::system_clock::now();
    double time = static_cast<double>(chrono::duration_cast<chrono::microseconds>(end - start).count() / 1000.0); //経過時間
    printf("%s : %.3f ms\n",command.c_str(),time);
}


void assign_process(vector<string> operation,ptree& payload){
    string tag,message;
    if(operation[0][0]='$'){
        string variable_name=operation[0].substr(1);
        if(find_variable(variable_name,message)) { //変数の値を追加
            if(operation.size()>1){
                tag=operation[2];
            }else tag=variable_name; 
            if(message.length()>0) payload.put(tag,message); //空白ならば送らない
        }
    }else{
            tag=operation[0];
            message=operation[2];
            payload.put(tag,message);
    }
}


void parser(const unsigned char* databuffer,vector<string> operation,int& linecnt,ptree& payload,bool& use){
    if(operation.empty()){
        ++linecnt;
        return;
    }

    if(!for_stack.empty()&&for_stack.top()==-1){
        if(operation[0]=="endwhile") for_stack.pop();
        else if(operation[0]=="while") for_stack.push(-1);
        ++linecnt;
        return;
    }

    if(!if_stack.empty()&&if_stack.top()==0){ //ifがfalseの時
        if(operation[0]=="if") if_stack.push(-1);
        else if(operation[0]=="elif"){
            vector<string> evals;
            copy(operation.begin()+1,operation.end(),back_inserter(evals));
            if(evaluate(evals)) {
                if_stack.pop();
                if_stack.push(1);
            }
        }else if(operation[0]=="else"){
            if_stack.pop();
            if_stack.push(1);
        }else if(operation[0]=="endif") if_stack.pop();
        ++linecnt;
        return;
    }else if(!if_stack.empty()&&if_stack.top()==-1){ //すでに一つ実行されている時
        if(operation[0]=="if") if_stack.push(-1);
        else if(operation[0]=="endif") if_stack.pop();
        ++linecnt;
        return;
    }

    if(operation[0]=="int"||operation[0]=="string"){ //変数宣言
        def_process(databuffer,operation);
    }else if(operation[0][0]=='$'){ //変数再代入
        update_var(databuffer,operation);
    }else if(operation[0]=="print"){ //変数の中身表示用(debug)
        string key=operation[1].substr(1),tmp;
        if(find_variable(key,tmp)) cout<<key<<" : "<<tmp<<endl;
        else {
            cerr<<"no variable"<<endl;
            exit(1);
        }
    }else if(operation[0]=="discard"){ //パケットを無視する
        use=false;
        skip=true;
    }else if(operation[0]=="end"){
        skip=true;
    }else if(operation[0]=="if"){
        vector<string> evals;
        copy(operation.begin()+1,operation.end(),back_inserter(evals));
        if(evaluate(evals)) if_stack.push(1);
        else if_stack.push(0);
    }else if(operation[0]=="elif"){
            if_stack.pop(); if_stack.push(-1);
    }else if(operation[0]=="else"){
        if_stack.pop();
        if_stack.push(-1);
    }else if(operation[0]=="endif"){
        if_stack.pop();
    }else if(operation[0]=="while"){
        vector<string> evals;
        copy(operation.begin()+1,operation.end(),back_inserter(evals));
        if(evaluate(evals)) for_stack.push(linecnt);
        else for_stack.push(-1);
    }else if(operation[0]=="endwhile"){
        if(for_stack.top()==-1){
            for_stack.pop();
        }else{
            linecnt=for_stack.top();
            for_stack.pop();
            return;
        }
    }else if(operation[0]=="add_ref"){
        add_reference(sub_vector(operation,1)); 
    }else if(operation[0]=="erase_ref"){
        string waste;
        reference(sub_vector(operation,1),waste,"erase");
    }else if(operation[0]=="process"){
        os_process(sub_vector(operation,1));
    }else if(operation[0]=="assign"){
        assign_process(sub_vector(operation,1),payload); 
    }else if(operation[0]=="continue"){ //while文のcontinue
        if(for_stack.empty()) return;
        linecnt=for_stack.top();
        for_stack.pop();
        return;
    }else if(operation[0]=="break"){ //while文のbreak
        for_stack.pop();
        for_stack.push(-1);
    }
    ++linecnt;
}
//変換を行ったかを返す
bool convert(int convert_type,const string read_file_name,const unsigned char* data={},const int packet_length=0,string srcip="",string dstip="",string srcport="",string dstport=""){
    chrono::system_clock::time_point start, end; //timing
    start = chrono::system_clock::now();
    ptree output;
    ifstream file_open;
    file_open.open(read_file_name,ios::in);
    if(!file_open.is_open()){
        cerr<<"cannot open convert rule:"<<read_file_name<<endl;
        return false;
    }
    string reading_buffer;
    vector<string> commands;
    string input_file_name,output_file_name;

    bool is_convert_packet=true;
    while(!file_open.eof()){
        getline(file_open,reading_buffer);
        commands.push_back(reading_buffer);
    }
    int read_line=0;
    if(convert_type==0){
        output_file_name=commands[0].substr(12);
        read_line=1;
    }else if(convert_type==1||convert_type==2){ 
        input_file_name=commands[0].substr(11);
        output_file_name=commands[1].substr(12);
        read_line=2;
    }else{
        input_file_name=commands[0].substr(11);
        read_line=1;
        is_convert_packet=false;
    }


    if(convert_type==0){ //パケットからのパースの場合
        //default変数
        int_variable["packet_length"]=packet_length;
        str_variable["all_message"]=string{(char*)data}.substr(0,packet_length); //substrがないとなぜか増えることがある
    }else{
        str_variable["input_json_name"]=input_file_name;
        srcip=get_value("srcip",input_file_name);
        dstip=get_value("dstip",input_file_name);
        srcport=get_value("srcport",input_file_name);
        dstport=get_value("dstport",input_file_name);
    }
    str_variable["srcip"]=srcip;
    str_variable["dstip"]=dstip;
    str_variable["srcport"]=srcport;
    str_variable["dstport"]=dstport;
    output.put("srcip",srcip);
    output.put("dstip",dstip);
    output.put("srcport",srcport);
    output.put("dstport",dstport);
    while(read_line<commands.size()){
        if(skip) break;
        vector<string> operations;
        if(regex_search(commands[read_line],regex(R"(^process\s.*)"))){
            //cout<<"called"<<endl;
            operations=space_split(commands[read_line],false);
        }else if(regex_search(commands[read_line],regex(R"(regex|regmatch)"))){
            operations=space_split_regex(commands[read_line],false);
        }else{
            operations=split_statement(commands[read_line]);
        }
        parser(data,operations,read_line,output,is_convert_packet);
    }
    int_variable.clear();
    str_variable.clear();
    skip=false;
    if(is_convert_packet) write_json(output_file_name,output);
    end = chrono::system_clock::now();
    double time = static_cast<double>(chrono::duration_cast<chrono::microseconds>(end - start).count() / 1000.0); //経過時間
    printf("%s : %.3f ms\n",read_file_name.c_str(),time);
    return is_convert_packet;
}

