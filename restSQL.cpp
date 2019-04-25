//#include "TRestSql.h"

#include <TFile.h>
#include <TKey.h>
#include <TRestG4Metadata.h>
#include <TRestMetadata.h>

#include <assert.h>
#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>
#include <iostream>

namespace po = boost::program_options;

int main(int argc, const char *argv[]) {
  string root_file_path;
  // using boost/program_options to perform argument parsing
  try {
    po::options_description desc{"Options"};
    desc.add_options()("help,h", "Help screen")(
        "file,f", po::value<string>(&root_file_path),
        "Input ROOT file (REQUIRED)");

    po::variables_map vm;
    store(parse_command_line(argc, argv, desc), vm);
    notify(vm);

    if (vm.count("help") || (argc <= 1)) {
      std::cout << desc << '\n';
      return 0;
    } else if (vm.count("file")) {
      // we continue with normal execution
      root_file_path = vm["file"].as<string>();
    } else {
      std::cout << desc << '\n';
      return 0;
    }

  } catch (const po::error &ex) {
    std::cerr << ex.what() << '\n';
    return 0;
  }

  root_file_path = boost::filesystem::canonical(root_file_path).string();
  // above step checks if file exists and returns the absolute path normalized,
  // for example removes double "//" if present

  cout << root_file_path << std::endl;

  TRestTools::LoadRESTLibrary();

  TFile *f = new TFile((TString)root_file_path);

  for (const auto &obj : *f->GetListOfKeys()) {
    TKey *key = (TKey *)obj;
    string key_class_name = key->GetClassName();

    if (key_class_name == "TRestG4Metadata") {
      TRestMetadata *key_metadata = (TRestMetadata *)f->Get(key->GetName());
      assert(key_metadata->InheritsFrom("TRestMetadata"));
      cout << "REST version used: " << key_metadata->GetVersion() << std::endl;
    }
    cout << key_class_name << " - " << key->GetName() << std::endl;
  }

  f->Close();

  return 0;
}