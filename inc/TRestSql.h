//
// Created by lobis on 4/24/19.
//

#ifndef RESTSQL_TRESTSQL_H
#define RESTSQL_TRESTSQL_H

#include <TFile.h>

#include <TRestDetectorSetup.h>
#include <TRestG4Metadata.h>
#include <TRestMetadata.h>

class TRestSQL {
public:
  TRestMetadata *GetTRestG4MetadataFromFile(TFile *);
};

#endif // RESTSQL_TRESTSQL_H
