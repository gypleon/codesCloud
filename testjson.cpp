#include <json/json.h>
#include <ifstream>
#include <iostream>
#include <set>

using namespace std;

int main(){
    ifstream fin("../hadoop/hadoop-2.5.2/usrlist.test", ios::in);
    char line[10240] = {0}
    Json::Reader reader;
    Json::Value value;
    set<string> like;
    set<string> unlike;
    while( fin.getline(line, sizeof(line))){
        if( reader.parse(line, value)){
            Json::Value ja_unlike = value["u"];
            Json::Value ja_like = value["l"];
            for (int i=0; i<ja_like.size(); i++){
                like.insert(ja_like[i].asString());
            }
            for (int i=0; i<ja_unlike.size(); i++){
                unlike.insert(ja_unlike[i].asString());
            }
            for (set<string>::iterator i=set::begin(); i!=set.end(); i++){
                cout << *iterator;
            }
        }

    }
    fin.clear();
    fin.close();
    return 0;
}
