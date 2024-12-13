import requests
import argparse
import os

SERVER_URL = "http://127.0.0.1:5000/files"


def add_files(files):
    with requests.Session() as session:
        files_payload = [("files", open(file, "rb")) for file in files]
        response = session.post(SERVER_URL, files=files_payload)
        print(response.json())


def list_files():
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        print("Files in the store:")
        for file in response.json():
            print(f"- {file}")
    else:
        print("Error:", response.json())




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Store CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add files
    parser_add = subparsers.add_parser("add", help="Add files to the store")
    parser_add.add_argument("files", nargs="+", help="Files to add")

    # List files
    parser_list = subparsers.add_parser("ls", help="List files in the store")


    args = parser.parse_args()

    if args.command == "add":
        add_files(args.files)
    elif args.command == "ls":
        list_files()
    else:
        parser.print_help()
