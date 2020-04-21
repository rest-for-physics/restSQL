import pymysql
import hashlib

class Mariadb(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

            db_config = {'db': 'restsql', 'host': 'localhost',
                     'password': 'restsql.2020', 'port': 3306, 'user': 'restsql'}
            try:
                print('connecting to MariaDB database...')
                connection = Mariadb._instance.connection = pymysql.connect(**db_config)
                cursor = Mariadb._instance.cursor = connection.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()

            except Exception as error:
                print('Error: connection not established {}'.format(error))
                Mariadb._instance = None

            else:
                print('connection established\n{}'.format(db_version[0]))

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def query(self, query):
        try:
            result = self.cursor.execute(query)
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            self.connection.commit()
            return result

    def __del__(self):
        self.connection.close()
        self.cursor.close()

# specific database methods

def file_unique_id(file_id, path):
    return hashlib.md5((file_id + path).encode()).hexdigest()

def clear_database():
    sql = "DROP TABLE IF EXISTS FILES"
    return Mariadb().query(sql)

#   files table
def create_files_table():
    sql = """
CREATE TABLE IF NOT EXISTS FILES (
name varchar(255) CHARACTER SET utf8 UNIQUE,
primary key(name),
file_id varchar(36) NOT NULL,
owner text,
created_date timestamp,
last_modified_date timestamp,
size_MB float,
insert_date timestamp,
index name_index (name)
);
"""
    return Mariadb().query(sql)

def get_files():
    sql = "SELECT name FROM FILES"

    Mariadb().query(sql)
    
    rows = Mariadb().cursor.fetchall()

    return [row[0] for row in rows]

def delete_files(files):
    if len(files) == 0:
        return
    #print(f"attempting to delete: {files}")
    files_to_delete = ",".join(["'" + file + "'" for file in files])

    sql = f"""
    PRAGMA foreign_keys = ON;
    DELETE FROM FILES WHERE name in ({files_to_delete});
    """
    print(sql)
    return Mariadb().query(sql)

def insert_files_data(file_info):
    sql = f"""
INSERT INTO FILES(
name, file_id, owner, created_date, last_modified_date, size_MB, insert_date) VALUES( 
'{file_info['name']}', '{file_info['id']}', '{file_info['owner']}', '{file_info['created date']}', '{file_info['last modified date']}', 
'{file_info['size (MB)']}', '{file_info['insert date']}');
"""

    create_files_table()
    Mariadb().query(sql)
    return True

#   metadata table

def create_metadata_table(class_name, metadata_fields):
    fields = [f"`{field}` text" for field in metadata_fields]
    fields = ",\n".join(fields)
    sql = f""" 
CREATE TABLE IF NOT EXISTS {class_name} (
file_name varchar(255) CHARACTER SET utf8 NOT NULL,
name VARCHAR(100),
{fields},
PRIMARY KEY (file_name, name),
FOREIGN KEY (file_name) REFERENCES FILES (name) ON DELETE CASCADE
);
"""
    return Mariadb().query(sql)

def insert_metadata(class_name, metadata_name, file_id, root_file, data):
    fields = ', '.join([f"`{key}`" for key in data.keys()])
    values = ', '.join([f"'{str(value)}'" for value in data.values()])

    sql = f"""
INSERT INTO {class_name} (file_name, name, {fields}) VALUES(
'{root_file}',
'{metadata_name}',
{values}
);
"""
    create_metadata_table(class_name, data.keys())
    return Mariadb().query(sql)
