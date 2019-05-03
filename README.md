# restSQL

restSQL is a program that will be able to access a directory and create/populate a SQL database with the information found inside the metadata structures of REST files in that directory.

## How it works

restSQL can be run on a single file `restSQL -f rest_run.root` or on a directory `restSQL -d directory` which will process all files inside the directory.

restSQL will read the ROOT file and create an entry in the *FILES* table with the file name and other identifying information including the file hash which will be unique to the file (e.g. any modification to the file will change the hash). The file hash will be the unique identifier and serve as primary key.

The information contained in each metadata object of the file will also be read on a case by case basis and stored on a different table for each kind of metadata structure (e.g. *TRESTGAS* table where entries would be the output of different getters such as `GetPressure` or `GetTemperature`). These tables would be linked to the main *FILES* table via the file unique identifier.

Sample of metadata objects contained in a file (simulation run + analysis): 

```
TRestPhysicsLists - default
TRestGas - Argon-Isobutane 2Pct 10-10E3Vcm
TRestReadout - TREXDM_v1
TRestRun - Background Model
TRestElectronDiffusionProcess - Ar-electronDiffusion-1kVcm-10atm
TRestHitsToSignalProcess - hitsToSignal-Template
TRestFastHitsToTrackProcess - fastHitsToTrack-Template
TRestGeant4AnalysisProcess - g4Ana
TRestTriggerAnalysisProcess - trigger
TRestHitsAnalysisProcess - hitsAna
TRestG4toHitsProcess - g4ToHits
TRestProcessRunner - TemplateEventProcess
TRestG4Metadata - restG4 Simulation run
TRestTrackAnalysisProcess - tckAna
TRestTrackReconnectionProcess - trackReconnection-Template
TRestSignalToHitsProcess - signalToHits
```
