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
    for (const auto& pair : metadata_map) {
        string class_name = pair.first;
        string object_name = pair.second->GetName();
        cout << class_name << " - " << object_name << std::endl;
    }
}

static int callback(void* NotUsed, int argc, char** argv, char** azColName) {
    int i;
    for (i = 0; i < argc; i++) {
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

void TRestSQL::CreateDatabase() {
    string sqlite_file_to_use = sqlite_file;
    if (sqlite_file_to_use == "") {
        sqlite_file_to_use = "default.db";
    }
    sqlite3* db;
    char* zErrMsg = nullptr;
    int rc;
    char* sql;

    // open database
    rc = sqlite3_open(sqlite_file_to_use.c_str(), &db);

    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return;
    } else {
        fprintf(stdout, "Opened database successfully\n");
    }

    sql =
        "CREATE TABLE FILES("
        "ID             INT     PRIMARY KEY NOT NULL,"
        "NAME           TEXT                NOT NULL,"
        "REST_VERSION   CHAR(15)"
        ")";

    // execute SQL
    rc = sqlite3_exec(db, sql, callback, nullptr, &zErrMsg);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(stdout, "Table created successfully\n");
    }
    sqlite3_close(db);
}