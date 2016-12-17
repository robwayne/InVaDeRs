import socket
import random
import threading
import _thread
import time

clientlist = []
lis = []
msglist = []
scoreboard = []
for i in range(1000):
    lis.append(str(random.randrange(640)))

def newClient(clientsocket):
    global lis
    global clientlist
    global msglist
    global scoreboard
    while True:
        i = 0
        c = 0
        data = clientsocket.recv(8).decode('utf_8')
        if data == 'ready':
            msglist.append(data)
        while True:
            if len(msglist)>1:
                clientsocket.send(bytes('start', 'utf_8'))
                break
            else:
                clientsocket.send(bytes('waiting', 'utf_8'))
                time.sleep(0.4)
        while (len(msglist)>1):
            client = clientsocket
            status = clientsocket.recv(4).decode('utf_8')
            if status == 'dead':
                msglist.append('dead')
                break
            i+=1
            if i==1000:
                i = 0
            try:
                client.send(bytes(lis[i], 'utf_8'))
                time.sleep(0.03)
            except:
                continue
            c+=1
        while True:
            if msglist.count('dead')==len(clientlist):
                client.send(bytes('yes', 'utf_8'))
                break
            else:
                client.send(bytes('no', 'utf_8'))
                time.sleep(0.4)

        while True:
            p2Score = client.recv(64).decode("utf_8")
            p2Score = p2Score.split(',')
            scoreboard.append([p2Score[0].replace("(", "").replace("'", "").replace("'", ""), p2Score[2]])
            break
        while True:
            if len(scoreboard)==len(clientlist):
                client.send(bytes(str(scoreboard), 'utf_8'))
                break

        data = client.recv(3).decode('utf_8')
        if data == 'fin':
            msglist.append('fin')
        while True:
            if msglist.count('fin')==len(clientlist):
                scoreboard = []
                msglist = []
                break
            elif msglist == []:
                break

host = ''
port = 5000
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)
spn = 0
addlist = []
while True:
    new = False
    c, addr = s.accept()
    clientInfo = [c, addr]
    if addlist == []:
        addlist.append(clientInfo[0].getsockname())
        clientlist.append(clientInfo[0])
        new = True
    else:
        if clientInfo[0].getsockname() not in addlist:
            addlist.append(clientInfo[0].getsockname)
            clientlist.append(clientInfo[0])
            new = True
    if new:
        print('thread started with client: '+clientInfo[0].getsockname()[0])
        _thread.start_new_thread(newClient, (clientlist[-1],))
