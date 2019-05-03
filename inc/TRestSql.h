//
// Created by lobis on 4/24/19.
//

#ifndef RESTSQL_TRESTSQL_H
#define RESTSQL_TRESTSQL_H

#include <unordered_map>

#include <TRestRun.h>

class TRestSQL : public TRestRun {
 private:
  std::unordered_map<string, TRestMetadata*> metadata_map;

  void SetMetadataMap();

 protected:
 public:
  void PrintMetadataMap();

};

#endif  // RESTSQL_TRESTSQL_H
