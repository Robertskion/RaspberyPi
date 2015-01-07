#!/usr/bin/env python
#coding: utf-8

import pyjsonrpc
import json
import app

####
#
#Variable Global
#
####

RASPIP = "192.168.137.13"

####
class RequestHandler(pyjsonrpc.HttpRequestHandler):


	@pyjsonrpc.rpcmethod
	def add(self, a, b):
		return a+b


	@pyjsonrpc.rpcmethod
	def playpause(self):
		xbmc = app.XBMCManager(RASPIP)	
		return xbmc.playPause()
		
#	@pyjsonrpc.rpcmethod
	#def add(self,a,b):
	#	try:
	#		x=1/0
	#	except ZeroDivisionError as detail:
	#		print "Handling error" , detail	


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (RASPIP, 50420),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP/xbmc server ..."

http_server.serve_forever()
