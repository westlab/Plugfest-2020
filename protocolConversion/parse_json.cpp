#include <iostream>
#include <fstream>
#include <vector>
#include <regex>
#include <unordered_map>
#include <boost/foreach.hpp>
#include <boost/optional.hpp>
#include <boost/property_tree/xml_parser.hpp>

#include "my_utilities.h"
#include "json.h"
using namespace std;

string replace_variable(string src,string var_name){
    return str_replace(src,"$_","$"+var_name);
}

void rule_process(const ptree rules,string var_type,string var_name,ofstream& opfile){
    BOOST_FOREACH(const ptree::value_type& child, rules.get_child("")){
        const ptree& rule=child.second;
        if(rule.get_optional<string>("")){
            string command=rule.get_value<string>("");
            if(command.find("$_")==0){
                command=var_type+" "+command;
            }
            command = replace_variable(command,var_name);
            opfile<<command<<endl;
        }
    }
}

void json_parser_test(string json_name,string output_name){
    ptree ref_json;
    ifstream ref_file_check(json_name);
    ofstream opfile(output_name);
    if(ref_file_check.is_open()) read_json(json_name,ref_json);
    else{
        cerr<<"error"<<endl;
        exit(1);
    }
    if(boost::optional<string>input_file=ref_json.get_optional<string>("input_file")){
        opfile<<"input_file:"<<input_file.get()<<endl;
    }
    if(boost::optional<string>output_file=ref_json.get_optional<string>("output_file")){
        opfile<<"output_file:"<<output_file.get()<<endl;
    }
    
    vector<pair<string,string>> register_variables;  //jsonに書き込む変数
    BOOST_FOREACH (const ptree::value_type& child, ref_json.get_child("")) {
        //if(child.first=="input_file"||child.first=="output_file"||child.first=="preprocess"||child.first=="postprocess") continue;
        if(child.first=="input_file"||child.first=="output_file") continue;
        //cout<<child.first<<endl;
        const ptree& info = child.second;
        string var_type;
        string var_name=child.first;
        bool ignore=false,set_if_use=false;
        if(child.first=="preprocess"||child.first=="postprocess") ignore=true;
        // 変数の型
        if (boost::optional<string> type = info.get_optional<string>("type")) {
            var_type=type.get();
        }else var_type="string";

        if (boost::optional<string> ign= info.get_optional<string>("ignore")) {
            ignore=((ign.get()=="true")?true:false);
        }
        
        if (boost::optional<std::string> if_use= info.get_optional<std::string>("if_use")) { //読み込みを行う条件
            set_if_use=true;
            string statement = "if "+if_use.get();
            statement=replace_variable(statement,var_name);
            opfile<<statement<<endl;
        }

        if (boost::optional<std::string> get= info.get_optional<std::string>("get")) { //inputからの読み出し
            if(boost::optional<string> if_none=info.get_optional<string>("if_none"))
                opfile<<var_type<<" $"<<var_name<<" get "<<get.get()<<" "<<if_none.get()<<endl;
            else opfile<<var_type<<" $"<<var_name<<" get "<<get.get()<<endl;
        }

        if (info.get_child_optional("rule")) {
            ptree rules=info.get_child("rule");
            rule_process(rules,var_type,var_name,opfile);
        }

        if (boost::optional<std::string> if_discard= info.get_optional<std::string>("if_discard")) { //変換自体を行うか
            string statement = "if "+if_discard.get()+"\ndiscard\nendif";
            statement=replace_variable(statement,var_name);
            opfile<<statement<<endl;
        }

        if (boost::optional<std::string> if_assign= info.get_optional<std::string>("if_assign")) { //変換自体を行うか
            string statement = if_assign.get();
            statement=replace_variable(statement,var_name);
            //cout<<statement<<endl;
            register_variables.push_back(make_pair(var_name,statement));
            ignore=true; //2度登録されないようにするため
        }
        if(set_if_use) opfile<<"endif"<<endl;

        if(!ignore) register_variables.push_back(make_pair(var_name,""));
    }

    for(auto var:register_variables){
        if(var.first=="") continue;
        if(var.second=="") opfile<<"assign $"<<var.first<<endl;
        else opfile<<"if "<<var.second<<"\nassign $"<<var.first<<"\nendif\n";
    }
}

#define DEBUG
#ifdef DEBUG
int main(int argc,char *argv[]){
    if(argc!=3){
        cerr<<"invalid input"<<endl;
        return 1;
    }
    string json_name=argv[1],command_name=argv[2];
    json_parser_test(json_name,command_name);
    return 0;
}
#endif
