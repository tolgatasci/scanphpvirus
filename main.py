import argparse

from helper.Global import *
from colorama import Fore, Style


def main() -> None:
    global data
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
        data = zip_run(args, data)
    if args.directory:
        data = directory_run(args, data)
    last_run()


def last_run() -> None:
    total_files = 0
    found_danger = 0
    for item in data.directory:

        for file_ in item.files:
            total_files += 1
            if file_.results:
                found_danger += 1
                print(Fore.GREEN + "File: " + Style.RESET_ALL + item.name + "/" + file_.name)
                for rulex in file_.results:
                    print(
                        Fore.RED + "Rule: " + Style.RESET_ALL + rulex.name + Fore.RED + " found: " + Style.RESET_ALL + rulex.found + Fore.RED + " on line: " + Style.RESET_ALL + str(
                            rulex.line))
    print(Fore.GREEN + "Total files: " + Style.RESET_ALL + str(total_files))
    print(Fore.RED + "Total found risk: " + Style.RESET_ALL + str(found_danger))


if __name__ == "__main__":
    main()
