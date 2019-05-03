//
// Created by lobis on 4/24/19.
//

#include "TRestSql.h"

// SetMetadataMap only needs to be called once per file read
void TRestSQL::SetMetadataMap() {
  metadata_map.clear();

  for (const auto& obj : *fInputFile->GetListOfKeys()) {
    TKey* key = (TKey*)obj;
    string key_class_name = key->GetClassName();
    TRestMetadata* metadata = (TRestMetadata*)fInputFile->Get(key->GetName());
    // we only want metadata (we do not want event tree, analysis tree, ...)
    if (!metadata->InheritsFrom("TRestMetadata")) {
      // cout << "skipped " << key_class_name << std::endl;
      continue;
    }
    // cout << "added " << key_class_name << std::endl;
    metadata_map[key_class_name] = metadata;
  }
}

void TRestSQL::PrintMetadataMap() {
  cout << "metadata_map has " << metadata_map.size() << " elements"
       << std::endl;
  for (const auto& pair : metadata_map) {
    string class_name = pair.first;
    string object_name = pair.second->GetName();
    cout << class_name << " - " << object_name << std::endl;
  }
}
