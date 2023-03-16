import os
import sqlite3
import docx
import time

def get_docx_info(file_path):
    """
    Extract metadata from docx file
    """
    doc = docx.Document(file_path)
    author = doc.core_properties.author
    created_time = doc.core_properties.created
    last_modifier = doc.core_properties.last_modified_by
    last_modified_time = doc.core_properties.modified
    return author, created_time, last_modifier, last_modified_time

def get_doc_info(file_path):
    """
    Extract metadata from doc file
    """
    pass

def get_file_info(file_path):
    """
    Extract metadata from file
    """
    if file_path.endswith('.docx'):
        return get_docx_info(file_path)
    elif file_path.endswith('.doc'):
        return get_doc_info(file_path)
    else:
        return None

def get_file_list(dir_path):
    """
    Get all files in the directory
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def create_table(cursor):
    """
    Create table in database
    """
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_info
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT NOT NULL,
        author TEXT,
        created_time TEXT,
        last_modifier TEXT,
        last_modified_time TEXT);''')

def insert_data(cursor, file_path, author, created_time, last_modifier, last_modified_time):
    """
    Insert data into database
    """
    cursor.execute('''INSERT INTO file_info (file_path, author, created_time, last_modifier, last_modified_time)
        VALUES (?, ?, ?, ?, ?)''', (file_path, author, created_time, last_modifier, last_modified_time))

def main():
    """
    Main function
    """
    dir_path = 'Single_Functions\Asset'
    file_list = get_file_list(dir_path)
    conn = sqlite3.connect('file_info.db')
    cursor = conn.cursor()
    create_table(cursor)
    for file_path in file_list:
        file_info = get_file_info(file_path)
        if file_info:
            insert_data(cursor, file_path, *file_info)
            print(file_info)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()