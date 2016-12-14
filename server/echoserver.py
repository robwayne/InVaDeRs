import socket
import random

host = ''
port = 5000
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

while True:
    x = random.randrange(640)
    message = str(x)
    print(message)

    client, address =  s.accept()
    client.send(bytes(message, "utf_8"))
    client.close()
