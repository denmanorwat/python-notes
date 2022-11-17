import socket
import pickle
from executer import Executer
from database import DataBase

HOST = ""
PORT = 65432
print("Server started")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    executor = Executer(DataBase())
    s.bind((HOST, PORT))
    print("Socket binded")
    s.listen()
    print("Started listening")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if data == b'':
                    break
                instruction = pickle.loads(data)
                answer = pickle.dumps(executor.execute(instruction))
                conn.sendall(answer)
