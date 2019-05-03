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
  string input_file_hash;

  void SetMetadataMap();
  string SetInputFileHash() {
    string input_file_as_string;
    // TODO: implement file hash, if possible without reading the file again
    // temporary BAD implementation
    // we should be able to convert the file contents in bytes to a string and
    // compute hash
    input_file_as_string = fInputFileName;
    input_file_hash = sha1(input_file_as_string);
  }

 protected:
 public:
  void PrintMetadataMap();
  // TODO: write ReadRestRunFile in src instead
  void ReadRestRunFile(string filename, bool print_metadata_map_keys = false) {
    OpenInputFile((TString)filename);
    SetMetadataMap();
    if (print_metadata_map_keys) {
      PrintMetadataMap();
    }
    // we compute the hash afterwards to make sure file is exists and readable
    SetInputFileHash();
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
