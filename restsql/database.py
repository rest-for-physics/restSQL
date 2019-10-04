import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_files_table(conn):
    sql = """
CREATE TABLE IF NOT EXISTS FILES (
id text PRIMARY KEY,
name text NOT NULL UNIQUE,
owner text,
'created date' date,
'last modified date' date,
'size (MB)' float,
'insert date' date
);
"""
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
        print(e)


def insert_files_data(conn, file_info):
    sql = f"""
INSERT INTO FILES(
id, name, owner, 'created date', 'last modified date', 'size (MB)', 'insert date') VALUES(
'{file_info['id']}', 
'{file_info['name']}', '{file_info['owner']}', '{file_info['created date']}', '{file_info['last modified date']}', 
'{file_info['size (MB)']}', '{file_info['insert date']}');
"""

    create_files_table(conn)
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
        print(e)
        return False

    return True


def create_metadata_table(conn, class_name, metadata_fields):
    fields = [f"'{field}' text" for field in metadata_fields]
    fields = ",\n".join(fields)
    sql = f""" 
CREATE TABLE IF NOT EXISTS {class_name} (
id integer PRIMARY KEY,
file_id text NOT NULL,
name text,
{fields},
FOREIGN KEY (file_id) REFERENCES files (id)
);
"""
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
        print(e)


def insert_metadata(conn, class_name, metadata_name, file_id, data):
    fields = ', '.join([f"'{key}'" for key in data.keys()])
    values = ', '.join([f"'{str(value)}'" for value in data.values()])

    sql = f"""
INSERT INTO {class_name} (file_id, name, {fields}) VALUES(
'{file_id}',
'{metadata_name}',
{values}
);
"""

    create_metadata_table(conn, class_name, data.keys())
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
        print(e)

    return cur.lastrowid

def get_files(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM FILES")

    rows = cur.fetchall()

    return [row[0] for row in rows]