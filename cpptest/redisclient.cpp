#include <iostream>
#include <string>
#include <sys/time.h>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <cstring>

#include "hiredis.h"

#define redisCmd(context, ...) static_cast<redisReply*>(redisCommand(context, __VA_ARGS__))

int main(){
    redisContext *c;
    redisReply *reply;
    const char *hostname = "192.168.50.7";
    int port = 6379;
    struct timeval timeout = { 1, 500000};
    c = redisConnectWithTimeout(hostname, port, timeout);
    reply = redisCmd(c, "CLUSTER NODES");
    // parse reply string into lines
    std::istringstream rep_lines(reply->str);
    freeReplyObject(reply);
    char line_buf[256] = "";
    while(rep_lines.getline(line_buf, sizeof(line_buf))){
        // std::cout << line_buf << std::endl;
        // parse reply line into information
        std::istringstream line(line_buf);
        std::vector<std::string> split_info;
        // <id> <ip:ports> <flags> <master> <ping-sent> <pong-recv> <config-epoch> <link-state> <slot> <slot> ... <slot>
        while(line){
            std::string field;
            line >> field;
            if("" != field)
                split_info.push_back(field);
        }
        // for(std::string info:split_info)
        //     std::cout << info << ' ';
        // std::cout << std::endl;
        // std::cout << "TEST " << split_info.back() << std::endl;
        /* PARSE SLOTS
        * if ( 0 == strcmp("-", split_info[3].c_str()))
        *     std::cout << split_info[8] << std::endl;
        */
        // PARSE IP:PORT
        // std::istringstream ip_port(split_info[1]);
        // ip_port.getline(line_buf, sizeof(line_buf), ':');
        // std::string ip(line_buf);
        // ip_port.getline(line_buf, sizeof(line_buf), ':');
        // std::istringstream ports(line_buf);
        // std::istringstream ports(line_buf);
        // ports.getline(line_buf, sizeof(line_buf), '@');
        // int port = atoi(line_buf);
        // 2nd METHOD
        // std::string ip_port(split_info[1]);
        // int pos_delim = ip_port.find(":");
        // std::string ip = ip_port.substr(0, pos_delim - 1);
        // int pos_delim_bak = pos_delim;
        // pos_delim = ip_port.find("@", pos_delim);
        // int port = 0;
        // if (std::string::npos == pos_delim){
        //     port = atoi(ip_port.substr(pos_delim_bak + 1, std::string::npos).c_str());
        // }else{
        //     port = atoi(ip_port.substr(pos_delim_bak + 1, pos_delim-pos_delim_bak).c_str());
        // }
        // std::cout << ip << ' ' << port << std::endl;
        
    }
    int cursor = 0;
    int amount = 1;
    do{
        reply = redisCmd(c, "SCAN %d COUNT %d", cursor, amount);
        // std::cout << reply->element[0]->str << std::endl;
        cursor = atoi(reply->element[0]->str);
        for ( int i=0; i<reply->element[1]->elements; i++){
            //std::cout << reply->element[1]->element[i]->str << " " << reply->element[1]->element[i]->type << std::endl;
            redisReply * rep = redisCmd(c, "TYPE %s", reply->element[1]->element[i]->str);
            if (!strcmp(rep->str, "string")){
                rep = redisCmd(c, "GET %s", reply->element[1]->element[i]->str);
                std::cout << reply->element[1]->element[i]->str << " " << rep->str << std::endl;
            }else if (!strcmp(rep->str, "list")){
                // rep = redisCmd(c, "LRANGE %s 0 -1", reply->element[1]->element[i]->str);
                // for (int j=0; j<rep->elements; j++){
                //     std::cout << reply->element[1]->element[i]->str << " " << rep->element[j]->str << std::endl;
                // }
                rep = redisCmd(c, "LLEN %s", reply->element[1]->element[i]->str);
                int llen = rep->integer;
                for (int j=0; j<llen; j++){
                    rep = redisCmd(c, "LINDEX %s %d", reply->element[1]->element[i]->str, j);
                    std::string value(rep->str);
                    std::cout << value << std::endl;
                }
            }else if (!strcmp(rep->str, "hash")){
                rep = redisCmd(c, "HGETALL %s", reply->element[1]->element[i]->str);
                for (int j=0; j<rep->elements; j++){
                    std::cout << reply->element[1]->element[i]->str << " " << rep->element[j]->str << std::endl;
                }
            }
        }
    }while(cursor);
    // reply = redisCmd(c, "LRANGE %s %d %d", key.c_str(), 0, 6);
    //std::istringstream rep_lines(reply->str);
    // for(int i=0; i<reply->elements; i++)
    //    std::cout << reply->element[i]->str << std::endl;
    freeReplyObject(reply);
    redisFree(c);

    return 0;
}
