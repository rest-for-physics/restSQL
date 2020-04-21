#!~/anaconda3/bin/python

import os
import time
import argparse
import datetime

from restsql import database
from restsql import rest_utils


def myprint(s):
    print(f"{datetime.datetime.now().strftime('%d.%b %Y %H:%M:%S')} - {s}", flush=True)

def get_root_files(path):
    myprint(f"scanning {path} for root files")
    root_files = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if '.root' in file:
                    root_files.append(os.path.abspath(os.path.join(root, file)))
    elif os.path.isfile(path):
        root_files = [os.path.abspath(path)]
    
    myprint(f"there are {len(root_files)} in {path}")
    return root_files

# process a root file, extracting metadata and inserting into database
def process_file(root_file):
    class_map, class_names, file_info = rest_utils.get_file_info(root_file)

    database.insert_files_data(file_info)

    for name, metadata in class_map.items():
        data = rest_utils.get_class_data(metadata)
        database.insert_metadata(class_names[name], name, file_info["id"], file_info["name"], data)

def remove_unavailable_entries():
    database_files = database.get_files()

    deleted_files = []
    for file in database_files:
        if not os.path.isfile(file):
            deleted_files.append(file)

    if deleted_files:
        print(f"found {len(deleted_files)} deleted/moved files, removing them from database - {deleted_files}")
        database.delete_files(deleted_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root_files_dir_or_single_file", help="root files path or single root file")
    args = parser.parse_args()
    path = os.path.abspath(args.root_files_dir_or_single_file)

    if os.path.isdir(path):
        myprint(f"directory to scan recursively: {path}")
    if os.path.isfile(path):
        myprint(f"working on file: {path}")
    
    # load REST libraries
    rest_utils.load_rest_libs()
    # create FILES table
    # database.clear_database()
    database.create_files_table()

    while 1:
        root_files = get_root_files(path)
        for file in root_files:
            #remove_unavailable_entries()
            database_files = database.get_files()
            if file not in database_files:
                process_file(file)
            else:
                pass
                #myprint(f"{file} already in database, skipping...")

        myprint("tick...")
        time.sleep(5)
