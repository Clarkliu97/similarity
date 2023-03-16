import os
import docx
import time

def get_file_info(file_path):
    file_info = {}
    file_info['file_name'] = os.path.basename(file_path)
    file_info['file_path'] = file_path
    file_info['file_size'] = os.path.getsize(file_path)
    file_info['file_type'] = os.path.splitext(file_path)[1]
    file_info['file_create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file_path)))
    file_info['file_modify_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file_path)))
    if file_info['file_type'] == '.docx':
        doc = docx.Document(file_path)
        file_info['file_author'] = doc.core_properties.author
        file_info['file_last_modifier'] = doc.core_properties.last_modified_by
    elif file_info['file_type'] == '.doc':
        pass
    return file_info

def get_file_info_list(folder_path):
    file_info_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_info = get_file_info(file_path)
            file_info_list.append(file_info)
    return file_info_list

if __name__ == '__main__':
    folder_path = 'Single_Functions\Asset'
    file_info_list = get_file_info_list(folder_path)
    print(file_info_list)