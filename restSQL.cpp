//#include "TRestSql.h"

#include <TFile.h>
#include <TKey.h>
#include <TRestG4Metadata.h>
#include <TRestMetadata.h>

#include <assert.h>
#include <boost/filesystem.hpp>
#include <iostream>

int main() {

  string root_file_path(
      "/home/lobis/Desktop/gifna-gitlab/restsql/"
      "Run_simulation_1e6-5keV_NeutronsFromGas_TestCalib_Neon_Version_2.root");

  root_file_path = boost::filesystem::canonical(root_file_path).string();
  // above step checks if file exists and also normalizes the format, for
  // example removes double "//"

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