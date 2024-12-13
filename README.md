# File Store Project

## Steps to Run the Project

### Without Using DockerFile (On Local Machine)
Install the required dependencies:
```python
pip install -r requirements.txt
```
Start the server:
```python
python server.py
```
### Using DockerFile
- Build the Docker image:
  ```bash
  docker build -t file-store .
- Run the Docker container:
  ```bash
  docker run -p 5000:5000 -v /d/file-system/file_storage:/app/files file-store

### Using Kubernetes
- Build the Docker image:
  ```bash
  docker build -t flask-app:latest .
- Push The Docker Image on DockerHub(Registry):
  ```bash
  docker tag flask-app lokicyberbytes/flask-app:latest
  docker push lokicyberbytes/flask-app:latest

- Start the minikube
  ```bash
  minikube start --driver=docker
- Mount the Volume on the location where you want to store the file
  ```bash
  minikube mount D:\file-store\file-storage:/mnt/local-dir
- Deploy the Flask app by applying your deployment.yaml and service.yaml files:
  ```bash
  kubectl apply -f deployment.yaml
  kubectl apply -f service.yaml
- Use Minikube’s built-in service tunneling:
  ```bash
  minikube service flask-app-service
- port forward the application to your localhost:
  ```bash
  kubectl port-forward service/flask-app-service 5000:80
  
### Use the Following Commands to Check Whether the System is Running
Open another terminal and use the CLI commands listed above to interact with the server.

Here are examples of commands to interact with the system:

- Add files:
  ```bash
  python cli.py add file1.txt file2.txt
- Remove files:
  ```bash
  python cli.py rm file1.txt
- List files:
  ```bash
  python cli.py ls
- Update a file:
  ```bash
  python cli.py update file2.txt
- Word count:
  ```bash
  python cli.py wc
- Frequent words with options:
  ```bash
  python cli.py freq-words --limit 5 --order asc

Thanks
