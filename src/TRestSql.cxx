//
// Created by lobis on 4/24/19.
//

#include "TRestSql.h"
#include <TKey.h>
#include <TRestMetadata.h>

TRestMetadata *TRestSQL::GetTRestG4MetadataFromFile(TFile *f) {
  for (const auto &obj : *f->GetListOfKeys()) {
    TKey *key = (TKey *)obj;
    string key_class_name = key->GetClassName();

    if (key_class_name == "TRestG4Metadata") {
      TRestMetadata *key_metadata = (TRestMetadata *)f->Get(key->GetName());
      assert(key_metadata->InheritsFrom("TRestMetadata"));
      return key_metadata;
    }
    cout << key->GetClassName() << " - " << key->GetName() << std::endl;
  }
}