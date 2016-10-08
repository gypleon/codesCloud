#include <json/json.cpp>
#include <iostream>
#include <ifstream>
#include <ofstream>
#include <thread>

using namespace std;

typedef class User{
public:
    User(){}
    ~User(){}
public:
    const int id;
    const set<int> *like;
    const set<int> *unlike;
}USER;

typedef class Data{
public:
    Data(){}
    ~Data(){}
    loadJSON()
public:
    const vector<USER> userlist;
}SRCDATA;

float jaccardCompute(const User& user1, const User& user2){
    float js = 0;

    return js;
}

reducer(){

}

int main(){
    // load json data

    // construct user pairs and tasks

    // distribute tasks, multithread

    // aggragate results

    // output results

    return 0;
}
