import os
from models.DModel import DModel, File, Directory, Result
from colorama import Fore, Style
from pyzip import PyZip
import re
import tempfile
data = []
bad_functions = {
        'eval': r'eval\(([\s]*)(.*?)([\s]*)\)',
        'system': r'system\(([\s]*)(.*?)([\s]*)\)',
        'chmod': r'chmod\(([\s]*)(.*?)([\s]*)\)',
        'fileperms': r'fileperms\(([\s]*)(.*?)([\s]*)\)',
        'unlink': r'unlink\(([\s]*)(.*?)([\s]*)\)',
        'mkdir': r'mkdir\(([\s]*)(.*?)([\s]*)\)',
        'assert': r'assert\(([\s]*)(.*?)([\s]*)\)',
        'base64_decode': r'base64_decode\(([\s]*)(.*?)([\s]*)\)',
        'file_get_contents': r'file_get_contents\(([\s]*)(.*?)([\s]*)\)',
        'file_put_contents': r'file_put_contents\(([\s]*)(.*?)([\s]*)\)',
        'curl_exec': r'curl_exec\(([\s]*)(.*?)([\s]*)\)',
        'curl_multi_exec': r'curl_multi_exec\(([\s]*)(.*?)([\s]*)\)',
        'move_uploaded_file': r'move_uploaded_file\(([\s]*)(.*?)([\s]*)\)',
    }
bad_functions_wp = {
        'wp_set_password': r'([\s@;/]*)wp_set_password([\s]*)\(',
        'wp_generate_password': r'([\s@;/]*)wp_generate_password([\s]*)\(',
        'wp_remote_post': r'([\s@;/]*)wp_remote_post([\s]*)\(',
        'wp_remote_get': r'([\s@;/]*)wp_remote_get([\s]*)\(',
        'wp_handle_upload': r'([\s@;/]*)wp_handle_upload([\s]*)\(',

}
sql_injection_regex = {
        'update': r'[\'\"]update(\s+)(.*?)(\s+)set',
        'insert':'insert(\s+)into(\s+)(.*?)(\s+)'
}
def scan_dir(path) -> dict:
    all_df = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            key, value = subdir, file
            if value.endswith(".php"):
                all_df.setdefault(key, []).append(value)
    return all_df
def scan_zip(path) -> dict:
    all_df = {}
    pyzip = PyZip().from_file(path, inflate=False)
    for key, val in pyzip.zip_content.items():
        if os.path.basename(key).endswith(".php"):
            try:
                key, value = os.path.dirname(key), {"filename": os.path.basename(key), "content": val.decode("utf-8")}
                all_df.setdefault(key, []).append(value)
            except Exception as e:
                print(e)
    return all_df


def directory_run(args,data) -> DModel:
    def content_get(key,val) -> []:
        with open(key+"/"+val, "r") as f:
            content = f.read()
        return content
    def content_run(key,val) -> []:
        x = [File(name=file,content=content_get(key,file)) for file in val]

        return x
    all_list = scan_dir(args.directory)
    directory = []
    for key, value in all_list.items():


        directory.append(Directory(name=key, files=content_run(key,value)))

    data = DModel(directory=directory)
    for item in data.directory:

        for file_ in item.files:
            found_rules = []
            file_content = None
            with tempfile.NamedTemporaryFile() as tmp:

                tmp.write(file_.content.encode())
                tmp.seek(0)
                file_content = tmp.readlines()
            for rule, bad_word in bad_functions.items():
                c_bad_word = re.compile(bad_word)
                match = c_bad_word.search(file_.content)

                if match:
                    found_line = match.group(0)

                    index = 1
                    for line in file_content:
                        c_bad_word = re.compile(bad_word)
                        match_2 = c_bad_word.search(line.decode('utf-8'))
                        if match_2:
                            break
                        index += 1
                    found_rules.append(Result(name=rule, found=found_line, line=index))
            for rule, bad_word in sql_injection_regex.items():
                c_bad_word = re.compile(bad_word)
                match = c_bad_word.search(file_.content)
                if match:
                    found_line = match.group(0)

                    index = 1
                    for line in file_content:
                        c_bad_word = re.compile(bad_word)
                        match_2 = c_bad_word.search(line.decode('utf-8'))
                        if match_2:
                            break
                        index += 1

                    found_rules.append(Result(name=rule, found=found_line, line=index))
            if args.wordpress:

                for rule, bad_word in bad_functions_wp.items():
                    c_bad_word = re.compile(bad_word)
                    match = c_bad_word.search(file_.content)
                    if match:
                        found_line = match.group(0)

                        index = 1
                        for line in file_content:
                            c_bad_word = re.compile(bad_word)
                            match_2 = c_bad_word.search(line.decode('utf-8'))
                            if match_2:
                                break
                            index+=1

                        found_rules.append(Result(name=rule, found=found_line, line=index))
            file_.results = found_rules
    return data

def zip_run(args,data) -> DModel:

    all_list = scan_zip(args.zip)

    directory = []
    for key, value in all_list.items():
        directory.append(Directory(name=key, files=[File(name=file['filename'],content=file['content']) for file in value]))

    data = DModel(directory=directory)


    for item  in data.directory:

        for file_ in item.files:
            found_rules = []
            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(file_.content.encode())
                tmp.seek(0)
                file_content = tmp.readlines()
            for rule, bad_word in bad_functions.items():
                c_bad_word = re.compile(bad_word)
                match = c_bad_word.search(file_.content)

                if match:
                    found_line = match.group(0)

                    index = 1
                    for line in file_content:
                        c_bad_word = re.compile(bad_word)
                        match_2 = c_bad_word.search(line.decode('utf-8'))
                        if match_2:
                            break
                        index += 1
                    found_rules.append(Result(name=rule, found=found_line, line=index))
            for rule, bad_word in sql_injection_regex.items():
                c_bad_word = re.compile(bad_word)
                match = c_bad_word.search(file_.content)
                if match:
                    found_line = match.group(0)

                    index = 1
                    for line in file_content:
                        c_bad_word = re.compile(bad_word)
                        match_2 = c_bad_word.search(line.decode('utf-8'))
                        if match_2:
                            break
                        index+=1

                    found_rules.append(Result(name=rule, found=found_line, line=index))
            if args.wordpress:
                for rule, bad_word in bad_functions_wp.items():
                    c_bad_word = re.compile(bad_word)
                    match = c_bad_word.search(file_.content)
                    if match:
                        found_line = match.group(0)

                        index = 1
                        for line in file_content:
                            c_bad_word = re.compile(bad_word)
                            match_2 = c_bad_word.search(line.decode('utf-8'))
                            if match_2:
                                break
                            index += 1

                        found_rules.append(Result(name=rule, found=found_line, line=index))
            file_.results = found_rules
        return data

