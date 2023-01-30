#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {

    string ip_range;
    cout << "Input an ip adress range: ";
    cin >> ip_range;
    cout << "You entered: " << ip_range << "\n"
         << "Scanning network..." << "\n";

    string command = "nmap -O " + ip_range;
    string output_file = "output.txt";

    string command_output = command + " > " + output_file;
    int result = system(command_output.c_str());

    if (result != 0)
        return 1;

    std::ifstream infile(output_file);
    std::string line, ip_address;
    bool found_raspberry_pi = false;

    while (std::getline(infile, line)) {

        std::size_t found = line.find("Raspberry Pi");
        if (found != std::string::npos)
            found_raspberry_pi = true;

        found = line.find("Nmap scan report for");
        if (found != std::string::npos) {
            std::size_t start = found + 21;
            ip_address = line.substr(start);
        }

        if (found_raspberry_pi && !ip_address.empty()) {
            cout << "Raspberry Pi found at " + ip_address << endl;
            cout << "Try connecting..." << endl;
            command = "ssh pi@" + ip_address;
            system(command.c_str());
            break;
        }
    }


    return 0;
}
