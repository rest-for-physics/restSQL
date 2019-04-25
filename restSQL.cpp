//#include "TRestSql.h"

#include <TFile.h>
#include <TKey.h>
#include <TRestG4Metadata.h>
#include <TRestMetadata.h>

#include <assert.h>
#include <iostream>

int main() {
  TRestTools::LoadRESTLibrary();

  TString root_file(
      "/home/lobis/Desktop/gifna-gitlab/restsql/"
      "Run_simulation_1e6-5keV_NeutronsFromGas_TestCalib_Neon_Version_2.root");

  TFile *f = new TFile(root_file);

  // TRestMetadata *restG4_metadata = restSql->GetTRestG4MetadataFromFile(f);

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