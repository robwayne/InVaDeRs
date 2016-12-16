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
    i = 0
    data = clientsocket.recv(8).decode('utf_8')
    print(data)
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
        print(status)
        if status == 'dead':
            msglist.append('dead')
        if 'dead' in msglist:
            client.send(bytes('dead', 'utf_8'))
            break
        i+=1
        if i==1000:
            i = 0
        try:
            client.send(bytes(lis[i], 'utf_8'))
            time.sleep(0.03)
        except:
            continue


    while True:
        global scoreboard
        p2Score = client.recv(64).decode("utf_8")
        print("Player2 score: ",p2Score)
        p2Score = p2Score.split(',')
        address = (p2Score[0]+","+p2Score[1])
        print("Address: ",address)
        print(client.getsockname())
        scoreboard.append([p2Score[0].replace("(", "").replace("'", "").replace("'", ""), p2Score[2]])
        for score in scoreboard:
            if score[0] != client.getsockname()[0]:
                print("address0: ",score[0], " clientsockname[0]: ", client.getsockname()[0])
                print("p2score: ",score[1])
                client.send(bytes(score[1], 'utf_8'))

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
        clientlist.append(clientInfo)
        new = True
    else:
        if clientInfo[0].getsockname() not in addlist:
            addlist.append(clientInfo[0].getsockname)
            clientlist.append(clientInfo)
            new = True
    if new:
        print('thread started')
        _thread.start_new_thread(newClient, (clientlist[-1][0],))
