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
   
        #waits for client to send ready and adds 'ready' to msglist
        data = clientsocket.recv(8).decode('utf_8')
        if data == 'ready':
            msglist.append(data)
        while True:
            #if both players have added to the msglist, server sends 'start' to each client to start main game loop
            if len(msglist)>1:
                clientsocket.send(bytes('start', 'utf_8'))
                break
            else:
                clientsocket.send(bytes('waiting', 'utf_8'))
                time.sleep(0.4)
        while (len(msglist)>1):
            client = clientsocket
            #receives status from client, if status = 'dead' it adds it to msglist and exits this loop
            status = clientsocket.recv(4).decode('utf_8')
            if status == 'dead':
                msglist.append('dead')
                break
            i+=1
            if i==1000:
                i = 0
            try:
                #send the integer at index i to the client for use as particle position
                client.send(bytes(lis[i], 'utf_8'))
                time.sleep(0.03)
            except:
                continue
            
        while True:
            #if all players have sent 'dead' to the server it sends 'yes' to clients so they can send their scores
            if msglist.count('dead')==len(clientlist):
                client.send(bytes('yes', 'utf_8'))
                break
            else:
                client.send(bytes('no', 'utf_8'))
                time.sleep(0.4)
        #receives the IP, score and nickname of the client and adds them to scoreboard
        while True:
            p2Score = client.recv(80).decode("utf_8")
            p2Score = p2Score.split(',')
            scoreboard.append([p2Score[0].replace("(", "").replace("'", "").replace("'", ""), p2Score[2], p2Score[3]])
            break
        while True:
            #if all players have added to the scoreboard it is sent to the clients
            if len(scoreboard)==len(clientlist):
                client.send(bytes(str(scoreboard), 'utf_8'))
                break
        #if client sends fin then they have successfully received the scores
        data = client.recv(3).decode('utf_8')
        if data == 'fin':
            msglist.append('fin')
        #if all players have sent 'fin' then the scoreboard and msglist are cleared in case players want to play another round
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
    #checks if client trying to connect is already in the list of connected players
    if addlist == []:
        addlist.append(clientInfo[0].getsockname())
        clientlist.append(clientInfo[0])
        new = True
    else:
        if clientInfo[0].getsockname() not in addlist:
            addlist.append(clientInfo[0].getsockname)
            clientlist.append(clientInfo[0])
            new = True
    #if it is a new client a new thread for that client is started
    if new:
        print('thread started with client: '+clientInfo[0].getsockname()[0])
        _thread.start_new_thread(newClient, (clientlist[-1],))
