#!/usr/bin/env python
#coding: utf-8

####
#
# Import
#
####
import pyjsonrpc
import json
import app

####
#
# Global Variables
#
####

# ip of the Raspberry Pi Host
# correspond a la clef RASP
RASP_IP = "192.168.43.143" 

# ip of one instance of xbmc
MAIN_IP= "192.168.43.35"

RASP = "Mehdi"
CURRENT_IP = MAIN_IP
Perif_dico = {RASP : RASP_IP,"MAIN" :MAIN_IP,"MacBook de Robin SEICHAIS":"192.168.43.143"}

# Listenned port
SERVER_PORT = "50420"

####
#
# Server class handling Android request
# to control xbmc media center
#
####
class RequestHandler(pyjsonrpc.HttpRequestHandler):

	# Fonction pausing/playing the music
	@pyjsonrpc.rpcmethod
	def playpause(self):
		xbmc = app.XBMCManager(CURRENT_IP)	
		result= xbmc.playPause()
		xbmc.connection.close()
		return result
		
	# Fonction used to get music content on the xbmc library
	@pyjsonrpc.rpcmethod
	def getaudio(self):
		xbmc = app.XBMCManager(CURRENT_IP)	
		result= xbmc.getAudio()
		xbmc.connection.close()
		return result
	
	# Fonction used to start a music
	@pyjsonrpc.rpcmethod
	def play(self, artist, id):
		xbmc = app.XBMCManager(CURRENT_IP)	
		result= xbmc.play(artist, id)
		xbmc.connection.close()
		return result

	# Fonction used to test the connexion between the server 
	# and the remote control 
	@pyjsonrpc.rpcmethod
        def add(self, a, b):
                return a+b
	
	# Fonction used to test an error's case
	@pyjsonrpc.rpcmethod
	def error(self,a,b):
		try:
			x=1/0
		except ZeroDivisionError as detail:
			print "Handling error" , detail	

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(

	# xbmc use port 8080 / Try to use another
	server_address = (RASP_IP, SERVER_PORT),
	RequestHandlerClass = RequestHandler
)



####
#
# MAIN
#
####

try:
	print "Serveur is listenning on ", RASP_IP, " on port ", SERVER_PORT
    	http_server.serve_forever()
except KeyboardInterrupt:
    	http_server.shutdown()
	print "Stopping HTTP server ..."


