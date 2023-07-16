import re
import os
import hashlib
from shutil import copyfile
from venture.config import Config
from venture.metadata import Metadata
from venture.objects.file_type import FileType


def get_casual_details(metadata:Metadata):
    round_to = 7
    casual_details = f"""Approx total cost since session start: {round(metadata.sum_cost_in_since_start_session+metadata.sum_cost_out_since_start_session,round_to)}$"""
    return Config.CASUAL_DETAILS_TEMPLATE.format(casual_details)


# -------------- [FILES] -------------- #


def get_parsed_files_path():
    return Config.DATA_PATH + Config.PARSED_FILES_PATH

def get_index_path():
    return Config.DATA_PATH + Config.INDEX_PATH

def write_text_to_file(text, path):
    text_file = open(path, "w")
    text_file.write(text)
    text_file.close()

def read_text_from_file(path):
    file = open(path,mode='r')
    all_text = file.read()
    file.close() 
    return all_text

def ensure_folder_created(path):
    if os.path.isdir(path):
        return
    os.makedirs(path)

def file_exists(path):
    return os.path.exists(path)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def copy(from_path, to_path):
    copyfile(from_path, to_path)

def loop_file_names_in_directory(root):
    for dir_path, _, file_names in os.walk(root):
        for file_name in file_names:
            if file_name[0] == '.':
                #IGNORE HIDDEN FILES
                continue
            full_file_path = dir_path + os.sep + file_name
            yield full_file_path

def doc_name_from_file_path(file_path:str):
    supported_file_types = set(ft.value for ft in FileType)
    file_name = (file_path.split('/')[-1]    # TAKE FILE NAME
                        .replace(' ','_')    # AVOID SPACES
                        .replace('.','_'))   # AVOID DOTS

    for suffix in supported_file_types:
        file_name = file_name.replace(f'_{suffix}','')   # REMOVE FILE TYPE
    
    file_name = re.sub('_+', '_', file_name)      # AVOID MULTIPLE UNDERSCORES
    return file_name

def hash_doc(doc:str):
    return hashlib.md5(doc.encode()).hexdigest()

def preprocess_doc(doc_as_string:str):
    cleaned = doc_as_string.strip()
    # REDUCING MULTIPLE LINE DROPS TO SINGLE
    cleaned = re.sub('\n+', '\n', cleaned)
    # COLLAPSING CONSECUTIVE NON-ALPHANUMERIC CHARACTERS ("?????" -> "?")
    cleaned = re.sub(r'([^\w\s])\1*', r'\1', cleaned)
    # FINAL TOUCH
    cleaned = cleaned.strip()
    return cleaned


# -------------- [MISC] -------------- #


def prettify_response(text):
    # DROP LINES AFTER ". ", BUT SKIP FOR NUMBERING ("1. <SOMETHING>")
    text = re.sub(r"([^0-9]\.)\s", "\\1\n", text)
    return text

def suppress_errors(fallback_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                print(ex)
                return fallback_value
        return wrapper
    return decorator

