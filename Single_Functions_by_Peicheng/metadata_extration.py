import os
import docx
import olefile
import csv

def get_docx_info(file_path):
    """
    Extract metadata from docx file
    """
    consistant: bool = False  # If author and last modifier are the same
    doc = docx.Document(file_path)  # Open docx file
    filename = os.path.basename(file_path)
    filename_no_ext = os.path.splitext(filename)[0]  # Get file name without extension
    # Get metadata
    author = doc.core_properties.author
    created_time = doc.core_properties.created
    last_modifier = doc.core_properties.last_modified_by
    last_modified_time = doc.core_properties.modified
    # Check if author and last modifier are the same
    if author.casefold() == last_modifier.casefold():
        consistant = True  # Author and last modifier are the same
    return filename_no_ext, author, created_time, last_modifier, last_modified_time, consistant

def get_doc_info(file_path):
    """
    Extract metadata from doc file
    """
    consistant: bool = False  # If author and last modifier are the same
    ole = olefile.OleFileIO(file_path)  # Open doc file
    filename = os.path.basename(file_path)  
    filename_no_ext = os.path.splitext(filename)[0]  # Get file name without extension
    metadata = ole.get_metadata()  # Get metadata

    author = metadata.author
    if author is not None and author != '':
        author = author.decode("utf-8")
    created_time = metadata.create_time
    last_modifier = metadata.last_saved_by
    if last_modifier is not None and last_modifier != '':
        last_modifier = last_modifier.decode("utf-8")
    last_modified_time = metadata.last_saved_time
    # Check if author and last modifier are the same
    if author.casefold() == last_modifier.casefold():
        consistant = True # Author and last modifier are the same
    return filename_no_ext, author, created_time, last_modifier, last_modified_time, consistant
    

def get_file_info(file_path):
    """
    Extract metadata from file
    """
    # Support only docx and doc files
    if file_path.endswith('.docx'):
        return get_docx_info(file_path)
    elif file_path.endswith('.doc'):
        return get_doc_info(file_path)
    else: # Not docx or doc file 
        return None

def get_file_list(dir_path):
    """
    Get all files in the directory and its subdirectories
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def write_to_csv(file_path):
    """
    Write First Row to csv file
    """
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['File Name', 'Author', 'Created Time', 'Last Modifier', 'Last Modified Time', 'Consistant'])

def add_to_csv(file_path, file_info):
    """
    Add metadata to csv file
    """
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(file_info)

def main():
    """
    Main function
    """
    dir_path = 'Single_Functions_by_Peicheng\Asset'
    file_list = get_file_list(dir_path)
    write_to_csv('Single_Functions_by_Peicheng\metadata.csv')
    for file_path in file_list:
        file_info = get_file_info(file_path)
        if file_info:
            add_to_csv('Single_Functions_by_Peicheng\metadata.csv', file_info)
            print(file_info)

if __name__ == '__main__':
    main()