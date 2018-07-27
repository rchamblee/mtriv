from guizero import App, TextBox, Window, PushButton, Text
import socket
from time import sleep
from threading import Thread

BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
sIP = 0
sP = 0
app = App(bg="lightblue1",title="Multitriv Client",layout="grid",width=875,height=600)
ippWindow = Window(app, title = "Server details")
inputLn = TextBox(app,grid=[0,0],width=50)
chatHist = TextBox(app,grid=[0,1], height=29,width=110, multiline=True)
ipBox = TextBox(app,grid=[0,2],width = 10, text="IP Address")
portBox = TextBox(app,grid=[0,3],width = 10,text="Port")

chatHist.text_color = "maroon"
inputLn.text_color = "maroon"
chatHist.bg = "LightSteelBlue3"
inputLn.bg = "LightSteelBlue3"
ipBox.bg = "LightSteelBlue3"
portBox.bg = "LightSteelBlue3"
def sendMsg(args):
	#if(event_data.key == "<Return>"):
	msgContents = inputLn.value
	inputLn.clear()
	s.send(msgContents.encode('utf-8'))
nick = "Aloura"
def conn():
	sIP = ipBox.value
	sP = portBox.value
	try:
		
		s.connect((sIP,int(sP)))
		s.settimeout(0.01)
		s.send(nick.encode('utf-8'))
		chatHist.repeat(150,getData)
	except:
		errWin = Window(app, title="Unable to connect.",width=200,height=50)
		Text(errWin, text="Unable to connect to " + str(sIP) + " on port " + str(sP))
		PushButton(errWin, text="Ok", command=errWin.hide)
ConnButton = PushButton(app,grid=[0,4],text="Connect",command=conn)

#def openW():
#	ippWindow.show()
#open_button = PushButton(app,text="set server/ip",command=openW())
def getData():
    timecounter = 0
    try:
        data_raw = s.recv(BUFFER_SIZE)
    except socket.timeout:
        return 0
    data = data_raw.decode('utf-8')
    if not data_raw:
        return 0
    else:
        chatHist.tk.insert(1.0,data + "\n")
        #schatHist.tk.xview()
    timecounter += 1
        #if((timecounter % 20) == 0):
        #    sock.send(('ping').encode('utf-8'))
        #    sleep(0.25)
        #    try:
        #      response = sock.recv(1024).decode('utf-8')
        #    except:
        #        if(not response):
        #            print("Connection DED :c. Attempting reconnect...")
        #            try:
        #                s.connect((sIP,sP))
        #            except:
        #                print("unable to recover connection to " + sIP + " quitting....")
        #        else:
        #            print("Unknown error occured.... dumping $response\n" + response)

def close():
	#ipDisplay = Text(app, text="IP: " + str(sIP),grid=[0,1])
	#portDisplay = Text(app, text="Port: " + str(sP),grid=[1,1])
	ippWindow.hide()

inputLn.tk.bind('<Return>',sendMsg)
	
#chatHist = TextBox(app,grid=[0,2], height=20,width=(60),multiline=True)
#try:
	#s.connect((sIP,sP))
	
close_button = PushButton(ippWindow, text="help me fuck off", command=close)
app.display()