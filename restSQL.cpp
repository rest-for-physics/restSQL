#include "TRestSql.h"

#include <TKey.h>
#include <TFile.h>
#include <iostream>

int main() {
  TRestSQL *restSql = new TRestSQL();

  std::cout << "test variable: " << restSql->x << std::endl;

  TString rootFile(
      "/home/lobis/Desktop/gifna-gitlab/restsql/"
      "Run_simulation_1e6-5keV_NeutronsFromGas_TestCalib_Neon_Version_2.root");

  TFile *f = new TFile(rootFile);

  for(const auto& obj: *f->GetListOfKeys())
  {
    TKey* key = (TKey*)obj;
    cout << key->GetClassName() << std::endl;
  }

  f->Close();

  restSql->PrintMetadata();

  return 0;
}