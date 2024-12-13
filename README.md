#File Store Project

##Steps to Run The Project

###Without Using DockerFile(In Local Machine)
1) pip install -r requirements.txt
2) python server.py
3) Open another terminal and use the CLI to interact with the server:
   Commands Example
   python cli.py add file1.txt file2.txt
   python cli.py ls
   python cli.py rm file1.txt
   python cli.py update file2.txt
   python cli.py wc
   python cli.py freq-words --limit 5 --order asc

###With Using Docker File
1) docker build -t file-store .
2) docker run -p 5000:5000 -v /d/file-system/file_storage:/app/files file-store
   Commands Example
   python cli.py add file1.txt file2.txt
   python cli.py ls
   python cli.py rm file1.txt
   python cli.py update file2.txt
   python cli.py wc
   python cli.py freq-words --limit 5 --order asc

