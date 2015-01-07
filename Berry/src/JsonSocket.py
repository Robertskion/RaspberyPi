#!usr/bin/env python
'''
Created on 6 janv. 2015

@author: Remi
'''

import SocketServer
import json

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
    	try:      
        	data = json.loads(self.request.recv(1024).strip())
        	print json.dumps(data)
        	# process the data, i.e. print it:
        	print data
        	# send some 'ok' back
        	self.request.sendall(json.dumps({'return':'ok'}))
      	except Exception, e:
		print "Exception while reveiving message: ", e 
            
      

server = MyTCPServer(('192.168.137.13', 50420), MyTCPServerHandler)
server.serve_forever()