#!/usr/bin/python3
import socket
from time import sleep
from threading import Thread
import sys
import shutil

TCP_IP = 'localhost'
TCP_PORT = 80
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sIP = TCP_IP
sP = TCP_PORT
try:
	sIP = sys.argv[1]
	try:
		sP = sys.argv[2]
	except:
		sP = int(input("You forgot the port: "))
except:
	sIP = input("What's the IP then?: ")
	sP = int(input("Oi, and the port?: "))
s.connect((sIP, int(sP)))
print("Who's you?")
nick = input()

s.sendto(nick.encode('utf-8'), (TCP_IP,TCP_PORT))

height = shutil.get_terminal_size().lines - 1
stdout_write_bytes = sys.stdout.buffer.write
CSI = b'\x1b['
CLEAR = CSI + b'2J'
CLEAR_LINE = CSI + b'2K'
SAVE_CURSOR = CSI + b's'
UNSAVE_CURSOR = CSI + b'u'

GOTO_INPUT = CSI + b'%d;0H' % (height + 1)

def emit(*args):
    stdout_write_bytes(b''.join(args))

def set_scroll(n):
    return CSI + b'0;%dr' % n

emit(CLEAR, set_scroll(height))

def getData(sock):
    timecounter = 0

    while True:
        data_raw = s.recv(BUFFER_SIZE)
        data = data_raw.decode('utf-8')
        if not data:
            break
        if (data.endswith("\r\n")):
            lines = data.split("\r\n")
            for line in lines:
                print (line)
        else:
            print(data)
        timecounter += 1
        if((timecounter % 20) == 0):
            sock.send(('ping').encode('utf-8'))
            sleep(0.25)
            try:
                response = sock.recv(1024).decode('utf-8')
            except:
                if(not response):
                    print("Connection DED :c. Attempting reconnect...")
                    try:
                        s.connect((sIP,sP))
                    except:
                        print("unable to recover connection to " + TCP_IP + " quitting....")
                else:
                    print("Unknown error occured.... dumping $response\n" + response)


t = Thread(target=getData, args=(s,))
t.daemon = True
t.start()


try:
    while True:
        emit(SAVE_CURSOR, GOTO_INPUT, CLEAR_LINE)
        try:
            data = input()
            if(data == "/quit"):
                emit(UNSAVE_CURSOR)
                break
            s.sendto(data.encode('utf-8'), (TCP_IP,TCP_PORT))
        except:
            continue
        finally:
            emit(UNSAVE_CURSOR)

except KeyboardInterrupt:
    #Disable scrolling, but leave cursor below the input row
    emit(set_scroll(0), GOTO_INPUT, b'\n')
