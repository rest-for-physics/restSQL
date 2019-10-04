import os

from restsql import rest_utils, database

root_file = "/home/lobis/gitlab/IAXOD0-REST/analysis_data/cosmic_neutrons/run_cosmic_neutrons_16-September-2019-17h29m47s/analysis_cosmic_neutrons_N100000000_0.root"

db_file = "/home/lobis/example/database.db"


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

def clean():
    deleted_files = find_deleted_files()


if __name__ == '__main__':
    path = "/home/lobis/gitlab/IAXOD0-REST/analysis_data/cosmic_neutrons/run_cosmic_neutrons_16-September-2019-17h29m47s/"
    files = get_files(path)
    find_deleted_files()
    for i, file in enumerate(files):
        print(f"{i + 1}/{len(files)} - {file}")
        process_file(file)
