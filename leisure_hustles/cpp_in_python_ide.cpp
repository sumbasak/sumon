############################### Cell 1 ###############################

%%writefile trial2.cpp

#include <iostream>
using namespace std;

void temp_conv(float temp) {
    float celsius = temp;
    float fahrenheit = (9.0 / 5.0) * celsius + 32.0;
    cout << celsius << " degree celsius equals with " << fahrenheit << " degree Fahrenheit.\n";
}

int main() {
    string temperature_str = "8";
    float temperature = stof(temperature_str);
    if (-1000.0 < temperature && temperature < 1000.0){
        temp_conv(temperature);
    }
    else {
        cout << "Please provide a valid input" << endl;
    }
    return 0; // never forget to write this even on virtual machine compilation
}


############################### Cell 2 ###############################
%%bash # for jupyter lab
%%shell # for google colab

g++ trial2.cpp -o output
./output
