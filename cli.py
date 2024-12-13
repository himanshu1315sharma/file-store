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


def delete_file(filename):
    response = requests.delete(f"{SERVER_URL}/{filename}")
    print(response.json())


def update_file(filename):
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist locally.")
        return

    with open(filename, "rb") as f:
        files_payload = {"file": f}
        response = requests.put(f"{SERVER_URL}/{filename}", files=files_payload)
        print(response.json())


def word_count():
    response = requests.get(f"{SERVER_URL}/wordcount")
    print(response.json())


def frequent_words(limit, order):
    params = {"limit": limit, "order": order}
    response = requests.get(f"{SERVER_URL}/frequent", params=params)
    print(response.json())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Store CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add files
    parser_add = subparsers.add_parser("add", help="Add files to the store")
    parser_add.add_argument("files", nargs="+", help="Files to add")

    # List files
    parser_list = subparsers.add_parser("ls", help="List files in the store")

    # Remove file
    parser_remove = subparsers.add_parser("rm", help="Remove a file from the store")
    parser_remove.add_argument("filename", help="File to remove")

    # Update file
    parser_update = subparsers.add_parser("update", help="Update a file in the store")
    parser_update.add_argument("filename", help="File to update")

    # Word count
    parser_wc = subparsers.add_parser("wc", help="Get word count of all files")

    # Frequent words
    parser_freq = subparsers.add_parser("freq-words", help="Get frequent words")
    parser_freq.add_argument("--limit", "-n", type=int, default=10, help="Number of frequent words")
    parser_freq.add_argument("--order", choices=["asc", "desc"], default="desc", help="Order of words")

    args = parser.parse_args()

    if args.command == "add":
        add_files(args.files)
    elif args.command == "ls":
        list_files()
    elif args.command == "rm":
        delete_file(args.filename)
    elif args.command == "update":
        update_file(args.filename)
    elif args.command == "wc":
        word_count()
    elif args.command == "freq-words":
        frequent_words(args.limit, args.order)
    else:
        parser.print_help()
