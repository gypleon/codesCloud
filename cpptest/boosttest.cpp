#include <iostream>
#include <boost/lexical_cast.hpp>

int main(){
    using boost::lexical_cast;
    int a = lexical_cast<int>("123");
    double b = lexical_cast<double>("123.12");
    std::cout<<a<<std::endl;
    std::cout<<b<<std::endl;
    return 0;
}
