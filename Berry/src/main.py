#!usr/bin/env python
'''
Created on 6 janv. 2015

@author: Remi
'''

import socket

#Ecriture dans un fichier
def commande():
    fichier = open("test.txt","w+")
    fichier.write("Test")
    fichier.close()
    
#Connection au socket
HOST = ''
PORT = 50420
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
print "Listenning"
s.listen(1)
conn,addr = s.accept()

print "connected by" ,addr

while(1):
    data = conn.recv(1024)
    
    if not data:
        break
    else:
        print data
        print "Longeur:",len(data)
        print "Premier:",data
    conn.sendall(data)
conn.close()
    

