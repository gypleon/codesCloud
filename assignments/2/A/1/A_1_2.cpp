#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

using namespace std;

#define WINDSIZE 1000

// transaction
typedef class Tran{
public:
    Tran() = default;
    ~Tran() = default;
public:
    int price_;
    int timestamp_;
}TRAN;

// bucket
typedef class Buck{
public:
    Buck(const TRAN& tran):size_(1), avg_(tran.price_), lastts_(tran.timestamp_){}
    ~Buck() = default;
    Buck& operator+=(const Buck& toadd){
        this->size_ += toadd.size_;
        this->avg_ = (this->avg_ + toadd.avg_) >> 1;
        this->lastts_ = toadd.lastts_;
        return *this;
    }
public:
    int avg_;
    int size_;
    int lastts_;
}BUCK;

// recent buckets
class Bucks{
public:
    Bucks() = default;
    ~Bucks() = default;
    void inputTran(const TRAN& tran){
        Buck buck(tran);
        bucks_.push_back(buck);
        vector<int> toberemoved;
        for(unsigned i=0; i<bucks_.size(); i++){
            if(bucks_[i].lastts_ < tran.timestamp_-WINDSIZE){
                toberemoved.push_back(i);
            }
        }
        for(auto i:toberemoved){
            bucks_.erase(bucks_.begin()+i);
        }
    }
    void mergeBucks(){
        int cur_size = 1;
        int cur_num = 0;
        int nxt_num = 0;
        vector<int> toberemoved;
        for(int i=bucks_.size()-1; i>=0; i--){
            if(bucks_[i].size_ == cur_size){
                cur_num++;
                if(cur_num>2){
                    bucks_[i] += bucks_[i+1];
                    toberemoved.push_back(i+1);
                    nxt_num++;
                }
            }else{
                cur_size <<= 1;
                cur_num = nxt_num + 1;
                nxt_num = 0;
            }
        }
        for(auto i:toberemoved){
            bucks_.erase(bucks_.begin()+i);
        }
        // displayBucks();
    }
    int estimateSold(){
        int soldcount = 0;
        int soldsum = 0;
        for(BUCK buck:bucks_){
            soldcount += buck.size_;
            soldsum += buck.avg_ * buck.size_;
        }
        soldcount -= bucks_.front().size_ >> 1;
        soldsum -= (bucks_.front().size_ * bucks_.front().avg_) >> 1;
        return soldsum / soldcount;
    }
    void displayBucks(){
        cout << "Buckets in Sliding Window:" << endl;
        cout << "SIZE" << ' ' << "AVERAGE_PRICE" << endl;
        for(auto& buck:bucks_){
            cout << setw(4) << buck.size_ << ' ' << setw(13) << buck.avg_ << endl;
        }
    }
private:
    vector<BUCK> bucks_;
};

int main(int argc, char* argv[]){
    Bucks recentBucks;
    char curchar;
    string curTran("");
    Tran tran;
    int tr_iter = 0;
    ifstream rawdata("engg5108_stream_data2.txt");
    if (rawdata.is_open()){
        while(rawdata.get(curchar)){
            if(' ' != curchar){
                curTran.push_back(curchar);
            }else{
                tran.price_ = stoi(curTran);
                tran.timestamp_ = tr_iter;
                recentBucks.inputTran(tran);
                recentBucks.mergeBucks();
                tr_iter += 1;
                curTran = "";
            }
        }
        rawdata.close();
    }
    recentBucks.displayBucks();
    cout << "Estimated Average Price: " << recentBucks.estimateSold() << endl;
    return 0;
}
