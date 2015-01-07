import httplib
import urllib
import json

"""
XBMC = httplib.HTTPConnection("127.0.0.1", 8080)

req = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "limits": { "start" : 0 }, "properties": ["artist"] }, "id": "retrieveSongs"}'
req2 = '{"jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": {"title":"Hey!", "message":"Doing something !"}, "id": "doSomething"}'
req3 = '{"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 0 }, "id": 1}'

XBMC.request('GET', '/jsonrpc?request=' + urllib.quote(req3, ''))


response = XBMC.getresponse()
if response.status == httplib.OK:
	print response.read()

XBMC.close()
"""


class XBMCManager:

	#CONSTRUCTOR METHOD
	def __init__(self, ip):

		#DEBUG
		print '__init__() - ' + ip + ':8080'

		self.connection = httplib.HTTPConnection(ip, 8080)

	#SWITCH USED DEVICE TO THE ONE WITH THE IP ADRESS GIVEN
	def switchDevice(self, ip):

		#DEBUG
		print 'switchDevice(ip) - ' + ip

		self.connection.close()
		self.connection = httplib.HTTPConnection(ip, 8080)

	#EXECUTE JSON-RPC REQUEST PASSED AS PARAMETER
	def executeJSONRPC(self, request):

		#DEBUG
		print 'executeJSONRPC(request) - ' + request

		self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			return True
		return False

	#SHOW NOTIFICATION
	def doSomething(self):

		#DEBUG
		print 'doSomething()'

		request = '{"jsonrpc": "2.0", "method": "GUI.ShowNotification", "params": {"title":"Hey!", "message":"Doing something !"}, "id": "doSomething"}'
		self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			return True
		return False

	#PLAY/PAUSE CURRENT PLAYER
	def playPause(self):

		#DEBUG
		print 'playPause()'

		request = '{"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": 0 }, "id": "playPause"}'
		self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			return True
		return False


	#RETRIEVE ALL AUDIO CONTENT
	def getAudio(self):

		#DEBUG
		print 'getAudio()'

		request = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "limits": { "start" : 0 }, "properties": ["artist"] }, "id": "retrieveSongs"}'

		self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

		response = self.connection.getresponse()
		if response.status == httplib.OK:

			result = '{"audio":['
			json_data = json.loads(response.read())

			first = True
			for song in json_data['result']['songs']:

				if first:
					first = False
					result += '{"title":"' + song['label'] + '", '
					result += '"artist":"' + song['artist'][0] + '", '
					result += '"id":"' + str(song['songid']) + '"}'
				else:
					result += ', '
					result += '{"title":"' + song['label'] + '", '
					result += '"artist":"' + song['artist'][0] + '", '
					result += '"id":' + str(song['songid']) + '}'

			result += ']}'

			return result

	#RETRIEVE ALL VIDEO CONTENT
	def getVideo(self):

		#DEBUG
		print 'getVideo()'

		#request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "limits": { "start" : 0 }, "properties": ["originaltitle"] }, "id": "retrieveMovies"}'
		request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": {"field": "playcount", "operator": "is", "value": "0"}, "limits": { "start" : 0, "end": 75 }, "properties" : ["art", "rating", "thumbnail", "playcount", "file"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}'

		self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

		response = self.connection.getresponse()
		if response.status == httplib.OK:

			"""result = '{"video":['
			json_data = json.loads(response.read())

			first = True
			for song in json_data['result']['songs']:

				if first:
					first = False
					result += '{"title":"' + song['label'] + '", '
					result += '"artist":"' + song['artist'][0] + '", '
					result += '"id":"' + str(song['songid']) + '"}'
				else:
					result += ', '
					result += '{"title":"' + song['label'] + '", '
					result += '"artist":"' + song['artist'][0] + '", '
					result += '"id":' + str(song['songid']) + '}'

			result += ']}'

			return result
			"""




###

#xbmc = XBMCManager("127.0.0.1")
#print xbmc.getVideo()


