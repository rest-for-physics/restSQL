#include "TRestSql.h"

#include <TFile.h>
#include <TKey.h>
#include <TRestG4Metadata.h>
#include <TRestMetadata.h>

#include <getopt.h>
#include <iostream>

string input_root_file;

void PrintHelp() {
    std::cout <<
              "--file <your_file.root>: Input ROOT file\n"
              "--help:      Print this help message\n";
    exit(1);
}

void ProcessArguments(int argc, char **argv) {
    const char *const short_opts = "f:h";
    const option long_opts[] = {
            {"file",  required_argument, nullptr, 'f'},
            {"help",  no_argument,       nullptr, 'h'},
            {nullptr, no_argument,       nullptr, 0}
    };

    while (true) {
        const auto opt = getopt_long(argc, argv, short_opts, long_opts, nullptr);

        if (-1 == opt)
            break;

        switch (opt) {
            case 'f':
                input_root_file = std::string(optarg);
                std::cout << "reading from root file: " << input_root_file << std::endl;
                break;
            case 'h':
                PrintHelp();
                break;
            case '?':
            default:
                PrintHelp();
                break;
        }
    }
}

int main(int argc, char *argv[]) {

    ProcessArguments(argc, argv);

    TRestTools::LoadRESTLibrary(true);

    TFile *f = new TFile((TString) input_root_file);

    for (const auto &obj : *f->GetListOfKeys()) {
        TKey *key = (TKey *) obj;
        string key_class_name = key->GetClassName();

        if (key_class_name == "TRestG4Metadata") {
            TRestMetadata *key_metadata = (TRestMetadata *) f->Get(key->GetName());
            assert(key_metadata->InheritsFrom("TRestMetadata"));
            cout << "REST version used: " << key_metadata->GetVersion() << std::endl;
        }
        cout << key_class_name << " - " << key->GetName() << std::endl;
    }

    f->Close();

    return 0;
}
