#!/usr/bin/python3
import socket
from threading import Thread
import time
from time import sleep
import random

TCP_IP = 'localhost'
TCP_PORT =  80
BUFFER_SIZE = 1024

new_data = ''
new_data_src = ''
scorePairs=[]
qaPairs = []
class Question:
    def __init__(self,prompt,answer):
        self.prompt = prompt
        self.answer = answer.upper()
        self.solved = False

class ClientThread(Thread):
    def __init__(self,ip,port,sock,nick):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        self.handled = False
        self.data = ''
        self.nick = nick
        self.score = 0
        print ("New thread for: " + ip + ":" + str(port))
        msgClients("New user connected: " + self.nick)
        
    def run(self):
        global new_data, new_data_src,scorePairs
        newPair = (self.nick,self.score)
        scorePairs.append(newPair)
        while True:
            rawdata = self.sock.recv(BUFFER_SIZE)
            curtime = time.strftime ("%H:%M")
            self.data = rawdata.decode('utf-8')
            if (not (self.data and self.data.strip())):
                break
            if(self.data == "ping"):
                print("Received ping from " + self.ip)
                response = "pong"
                self.sock.send(response.encode('utf-8'))
            elif(self.data == "!startq"):
                qThread = Thread(target=beginQuestion,args=())
                qThread.start()
            elif(self.data == "!stopq"):
                qThread.stop()
            elif(self.data == "!scores" or self.data == "!score"):
                msgClients("Scores----------")
                for pair in scorePairs:
                    msgClients(pair[0] + ": " + str(pair[1]))
                    sleep(0.2)
            else:
                new_data = self.data
                new_data_src = self.nick
                for thread in threads:
                    try:
                        thread.sock.send(("["+curtime+"]" + self.nick + ': ' + self.data).encode('utf-8'))
                    except:
                        print("Closing thread for " + ip + ": Connection broken")
                        return 1

def msgClients(message):
    for thread in threads:
        thread.sock.send(("["+time.strftime("%H:%M")+"][Multitriv]: " + message).encode('utf-8'))


            
        
def solveCheck(Question):
    global new_data,scorePairs
    while(not Question.solved):
        if(new_data == Question.answer):
            Question.solved = True
            msgClients("Question has been solved! Solved by: " + new_data_src)
            new_data = ''
            for pair in scorePairs:
                if(pair[0] == new_data_src):
                    scorePairs.insert(0,(pair[0],pair[1] + 1))
                    scorePairs.remove(pair)
                    print(pair[0] + " scored")
            break
        if(new_data == "!skip"):
            new_data = ''
            msgClients("Question skipped.")
            return 1
        sleep(0.5)
    return 1
    
        
def beginQuestion():
    while(True):
        quest = random.choice(qaPairs)
        print("Initiating new question...")
        msgClients(quest.prompt)
        solveCheck(quest)
        msgClients("Next question in 5s....")
        sleep(5)

def loadqDoc(filename):
    import re
    global qaPairs
    try:
        with(open(filename,"r")) as f:
            for line in f.readlines():
                elems = line.split(":")
            for index,item in enumerate(elems):
                newQ = Question('a','b')
                if(re.match(r'^[0-9]*\.',item)):
                      newQ.prompt = item
                      newQ.answer = elems[index + 1]
                      qaPairs.append(newQ)
    finally:
        print("done loading questions from " + filename)

        
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

loadqDoc("qdoc.mtq")

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    conn_Nick = conn.recv(1024).decode('utf-8')
    print ('Got connection from ', (ip,port,conn_Nick))
    newthread = ClientThread(ip,port,conn,conn_Nick)
    newthread.start()
    threads.append(newthread)
    for thread in threads:
        if not thread.isAlive():
            thread.handled = True
    threads = [thread for thread in threads if not thread.handled]
        

for thread in threads:
    thread.join()

