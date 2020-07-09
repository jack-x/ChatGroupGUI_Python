import socket
import threading
import pickle
import os
import sys


s = socket.socket()

HOST = '127.0.0.1'
PORT = 1234


ClientSocketList = []
messageOwnerList =[]
messageList = []
userNamedict = dict()
s.bind((HOST,PORT))

s.listen(100)


def ClientHandling(clientSocket):
    global messageList, messageOwnerList, userNamedict

    print("I am in CLientHandling")
    data = pickle.loads(clientSocket.recv(100000))

    messageList = data[1]
    messageOwnerList = data[0]
    print("data received")
    for x in ClientSocketList:
        x.send(pickle.dumps((messageOwnerList,messageList,userNamedict)))
    ClientReceivingThread = threading.Thread(target=lambda: ClientHandling(clientSocket))
    ClientReceivingThread.start()



while True:
    print("Waiting for new client")
    c, addr = s.accept()
    userInfo = c.recv(1000)
    userInfo = pickle.loads(userInfo)

    userNamedict[userInfo[1]] = userInfo[0]
    print("I am here")
    ClientSocketList.append(c)
    dataCouple = (messageOwnerList,messageList,userNamedict)
    c.send(pickle.dumps(dataCouple))
    ClientReceivingThread = threading.Thread(target=lambda: ClientHandling(c))
    ClientReceivingThread.start()



