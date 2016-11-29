#include <utility>
#include <iostream>
#include <vector>

using namespace std;

int main(){
        vector<pair<int, int> > vec;
        for (int i=0; i<100; i++){
                vec.push_back(make_pair(i, i*i));
        }
        for ( auto& v : vec){
                cout << v.first << " " << v.second << endl;
        }
        return 0;
}

