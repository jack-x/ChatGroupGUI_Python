import tkinter as tk
import threading
from tkinter import scrolledtext
import requests



#Network Connectivity here
import socket
import pickle
import random

s = socket.socket()

HOST = '127.0.0.1'
PORT = 1234

s.connect((HOST, PORT))

idString = ''
for x in range(1,11):
    idString += random.choice('abcdefghijklmnopqrstuvwxyz')

idHash = hash(idString) #this is now the client ID
messageOwnerList = []
messageList = []
userNameDict = []


response = requests.get('https://randomuser.me/api/')
userData = response.json()
userName = userData["results"][0]["name"]["first"]
s.send(pickle.dumps((userName,idHash)))




#https://randomuser.me/api/






#Setting up the GUI below

HEIGHT = 500
WIDTH = 500

root = tk.Tk()


canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()


upper_frame = tk.Frame(root, bg='black', bd = 10)
upper_frame.place(relx=0.5,rely=0.1,relwidth=0.75, relheight = 0.8, anchor='n')

text_area = tk.scrolledtext.ScrolledText(upper_frame, wrap = tk.WORD, width = 40,height = 10,font = ('Courier',10))
text_area.place(relwidth=1,relheight=0.9)
text_area.configure(state ='disabled')


##txt = tk.Text(upper_frame,bg='white',font = ('Courier',10),yscrollcommand = scroll.set)
##txt.place(relwidth=1,relheight=0.9)
##scroll.config(command=txt.yview)
#(relx=0.9,relwidth=0.1,relheight=0.9)


frame = tk.Frame(root, bg='blue', bd = 5)
frame.place(relx=0.5,rely=0.8,relwidth=0.75,relheight=0.1,anchor='n')
entry = tk.Entry(frame,font=40)
entry.place(relwidth=0.65,relheight=1)
button=tk.Button(frame,text='Send Message',font = 40,command = lambda: sendMessage(entry))
button.place(relx=0.7,relwidth=0.3,relheight=1)


def sendMessage(entry):
    messageOwnerList.append(idHash)
    messageList.append(entry.get())
    entry.delete(0,tk.END)
    dataCouple = (messageOwnerList,messageList)
    p = pickle.dumps(dataCouple)
    s.send(p)

def updateMessages():
    dataCouple = pickle.loads(s.recv(10000))
    global messageOwnerList,messageList
    messageOwnerList = dataCouple[0]
    messageList = dataCouple[1]
    userDict = dataCouple[2]

    text_area.configure(state='normal')
    text_area.delete('1.0',tk.END)
    text_area.configure(state='disabled')
    for x in range(0, len(messageOwnerList)):
        if messageOwnerList[x] == idHash:
            updateMessageFrame("You Said: {} \n".format(messageList[x]))
        else:
            updateMessageFrame(" {} says: {} \n".format(userDict[messageOwnerList[x]],messageList[x]))

    t1 = threading.Thread(target=updateMessages)
    t1.start()


t1 = threading.Thread(target=updateMessages)
t1.start()


def updateMessageFrame(message):
    text_area.configure(state='normal')
    text_area.insert(tk.INSERT,message)
    text_area.configure(state='disabled')


##root.after(1000,updateMessages)
root.mainloop()

#GUI setup complete
