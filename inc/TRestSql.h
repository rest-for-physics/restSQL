//
// Created by lobis on 4/24/19.
//

#ifndef RESTSQL_TRESTSQL_H
#define RESTSQL_TRESTSQL_H

#include <unordered_map>

#include <TRestGas.h>
#include <TRestRun.h>

#include "sha1.h"

class TRestSQL : public TRestRun {
 private:
  std::unordered_map<string, TRestMetadata*> metadata_map;
  void SetMetadataMap();

 protected:
 public:
  void PrintMetadataMap();
  void ReadRestRunFile(string filename, bool print_metadata_map_keys = false) {
    OpenInputFile((TString)filename);
    SetMetadataMap();
    if (print_metadata_map_keys) {
      PrintMetadataMap();
    }
  }

  TRestGas* GetRestGas() {
    SetMetadataMap();
    PrintMetadataMap();

    TRestGas* gas = (TRestGas*)metadata_map["TRestGas"];
    cout << "Gas Temperature: " << gas->GetTemperature() << std::endl;
    cout << sha1("patata") << std::endl;
    return gas;
  }
};

#endif  // RESTSQL_TRESTSQL_H
