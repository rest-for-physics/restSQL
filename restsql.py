import os
import time
import argparse

from restsql import rest_utils, database

db_file = "/tmp/restsql.db"


def process_file(root_file):
    class_map, class_names, file_info = rest_utils.get_file_info(root_file)

    conn = database.create_connection(db_file)
    with conn:
        inserted = database.insert_files_data(conn, file_info)
        if not inserted:
            # row already inserted
            return

        for name, metadata in class_map.items():
            data = rest_utils.get_class_data(metadata)
            database.insert_metadata(conn, class_names[name], name, file_info["id"], data)


def get_files(path):
    root_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if '.root' in file:
                root_files.append(os.path.abspath(os.path.join(root, file)))
    return root_files


def find_deleted_files():
    conn = database.create_connection(db_file)
    with conn:
        files = database.get_files(conn)

    deleted_files = []
    for file in files:
        if not os.path.isfile(file):
            deleted_files.append(file)

    return deleted_files


def get_database_files():
    conn = database.create_connection(db_file)
    with conn:
        return database.get_files(conn)


def clean_files():
    deleted_files = find_deleted_files()
    conn = database.create_connection(db_file)
    with conn:
        database.delete_files(conn, deleted_files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root_files", help="root files path or single root file")
    parser.add_argument("-d", "--database", help="database path")
    args = parser.parse_args()

    if args.database:
        db_file = os.path.abspath(args.database)

    path = os.path.abspath(args.root_files)

    rest_utils.load_rest_libs()

    while 1:
        files_processed = 0
        files = get_files(path)
        try:
            clean_files()
            database_files = get_database_files()
        except Exception as e:
            # database may not exist here
            database_files = []
        for i, file in enumerate(files):

            if file in database_files:
                continue
            print(f"{i + 1}/{len(files)} - {file}")
            process_file(file)
            files_processed += 1

        print(f"processed {files_processed} files")
        time.sleep(5)
