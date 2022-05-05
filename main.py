import argparse
import re
import tempfile
from helper.Global import *
from colorama import Fore, Style
from models.DModel import DModel, File, Directory, Result


def directory_run(args) -> None:
    global data
    def content_get(key,val) -> []:
        with open(args.directory+key+"/"+val, "r") as f:
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


def zip_run(args) -> None:
    global data
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
def last_run() -> None:
    total_files = 0
    found_danger = 0
    for item in data.directory:

        for file_ in item.files:
            total_files += 1
            if file_.results:
                found_danger += 1
                print(Fore.GREEN + "File: " + Style.RESET_ALL + item.name + "/" +file_.name)
                for rulex in file_.results:
                    print(Fore.RED + "Rule: " + Style.RESET_ALL + rulex.name + Fore.RED + " found: "  + Style.RESET_ALL+ rulex.found  + Fore.RED+ " on line: " + Style.RESET_ALL + str(rulex.line))
    print(Fore.GREEN + "Total files: " + Style.RESET_ALL + str(total_files))
    print(Fore.RED + "Total found risk: " + Style.RESET_ALL + str(found_danger))

def main() -> None:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--zip', '-z', type=str, help='Zip file', required=False)
    parser.add_argument('--directory', '-d', type=str, help='Directory', required=False)
    parser.add_argument('--wordpress', '-w', type=bool, help='Wordpress', required=False)
    args = parser.parse_args()
    if not args.zip and not args.directory:
        print(Fore.RED + "Please specify a zip file or a directory" + Style.RESET_ALL)
        print(Fore.GREEN + "usage: main.py [-h] [-z ZIP] [-d DIRECTORY]" + Style.RESET_ALL)
        exit(1)


    if args.zip:
        zip_run(args)
    if args.directory:
        directory_run(args)
    last_run()
data = None
if __name__ == "__main__":
    main()
