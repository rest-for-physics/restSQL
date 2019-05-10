//
// Created by lobis on 4/24/19.
//

#include "TRestSql.h"

#include <TRestMetadata.h>

#include <getopt.h>
#include <iostream>

string input_root_file;
string sqlite_file;

void PrintHelp() {
    std::cout << "--file <your_file.root>: [REQUIRED] Input ROOT file\n"
                 "--directory <dir>:       [NOT IMPLEMENTED] look for ROOT files "
                 "inside this directory\n"
                 "--sqlite_file:           [OPTIONAL] sqlite database file to "
                 "use, if not specified it will use default file, if it doesn't "
                 "exists it will try to create one"
                 "--help:                  Print this help message\n";
    exit(1);
}
void ProcessArguments(int argc, char** argv) {
    const char* const short_opts = "f:s:h:d";
    const option long_opts[] = {{"file", required_argument, nullptr, 'f'},
                                {"directory", required_argument, nullptr, 'd'},
                                {"sqlite_file", required_argument, nullptr, 's'},
                                {"help", no_argument, nullptr, 'h'},
                                {nullptr, no_argument, nullptr, 0}};
    // used to check that we called the required arguments
    std::set<char> used_argument_flags;
    const std::set<char> required_arguments_configurations[] = {
        {'f'},  // file
    };

    while (true) {
        const auto opt = getopt_long(argc, argv, short_opts, long_opts, nullptr);

        if (-1 == opt) {
            // we sort vector for easier comparison
            break;
        } else {
            // add argument to used arguments container for latter comparison
            used_argument_flags.insert((char)opt);
        }

        switch (opt) {
            case 'f':
                input_root_file = std::string(optarg);
                std::cout << "reading from root file: " << input_root_file << std::endl;
                break;
            case 'd':
                // TODO: implement reading all files in directory
                break;
            case 'h':
                PrintHelp();
                break;
            case 's':
                // TODO: implement checking file exists
                sqlite_file = std::string(optarg);
                std::cout << "sqlite database file provided: " << sqlite_file << std::endl;
                break;
            case '?':
            default:
                PrintHelp();
                break;
        }
    }
    // verify that we called all the required arguments and finish processing
    for (auto required_arguments : required_arguments_configurations) {
        bool required_arguments_ok = true;
        for (auto flag : required_arguments) {
            if (not used_argument_flags.count(flag)) {
                required_arguments_ok = false;
                break;
            }
        }
        if (required_arguments_ok) {
            return;
        }
    }
    // if we get here it means we miss required arguments
    PrintHelp();
}

int main(int argc, char* argv[]) {
    ProcessArguments(argc, argv);

    TRestTools::LoadRESTLibrary(true);

    TRestSQL* rest_sql = new TRestSQL();
    if (not(sqlite_file == "")) {
        // sqlite_file has been provided as an option
        rest_sql->SetSqliteFile(sqlite_file);
    }

    rest_sql->ReadRestRunFile(input_root_file, true);

    rest_sql->CreateTables();
    rest_sql->InsertIntoFiles(true);
    return 0;
}
