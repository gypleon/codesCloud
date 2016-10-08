#include <json-glib/json-glib.h>
#include <ifstream>
#include <iostream>
#include <set>

using namespace std;

int main(){
    ifstream fin("../hadoop/hadoop-2.5.2/usrlist.test", ios::in);
    char line[10240] = {0}
    JsonParser *parser;
    JsonNode *node;
    JsonReader *reader;
    // Json::Reader reader;
    // Json::Value value;
    g_type_init();
    parser = json_parser_new();
    set<string> like;
    set<string> unlike;
    while( fin.getline(line, sizeof(line))){
        json_parser_load_from_data(parser, line, NULL);
        node = json_parser_get_root(parser);
        if( reader = json_reader_new(node)){
        // if( reader.parse(line, value)){
            // Json::Value ja_unlike = value["u"];
            // Json::Value ja_like = value["l"];
            // for (int i=0; i<ja_like.size(); i++){
            //     like.insert(ja_like[i].asString());
            // }
            json_reader_read_member(reader,"l");
            count = json_reader_count_elements(reader);
            for (int i=0; i<count; i++){
                json_reader_read_element(reader,i);
                printf("%s\n", json_reader_get_string_value(reader));
                json_reader_end_element(reader);
                // unlike.insert(ja_unlike[i].asString());
            }
            json_reader_end_member(reader);
            // for (set<string>::iterator i=set::begin(); i!=set.end(); i++){
            //     cout << *iterator;
            // }
        }

    }
    fin.clear();
    fin.close();
    return 0;
}
