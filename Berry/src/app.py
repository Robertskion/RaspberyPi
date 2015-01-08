import httplib
import urllib
import json



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



	def createJsonrpc(self, method, params, i): 
		return '{"jsonrpc":"2.0", "method":"' + method + '", "params":' + params + ', "id": "' + i + '"}'



	def sendRequest(self, method, params ,i):
		self.connection.request('POST', '/jsonrpc', self.createJsonrpc(method,params,i))



	#SHOW NOTIFICATION
	def doSomething(self):

		print 'doSomething()'
		self.sendRequest('GUI.ShowNotification','{"title":"Hey!", "message":"Doing something !"}', 'doSomething' )        
		response = self.connection.getresponse()

		if response.status == httplib.OK:
			return True
		elif response.status == httplib.BAD_REQUEST:
			return False
		return False



	#PLAY/PAUSE CURRENT PLAYER
	def playPause(self):

		#DEBUG
		print 'playPause()'

		player_id = self._getActivePlayer()

		self.sendRequest('Player.PlayPause', '{"playerid": 0}', 'playPause')    
		response = self.connection.getresponse()
        
		if response.status == httplib.OK:
			return True
		elif response.status == httplib.BAD_REQUEST:
			return False
		return False

	def _getActivePlayer(self):

		#DEBUG
		print 'getActivePlayer()'

		request = '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'
	
		self.connection.request('POST', '/jsonrpc', request)

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			data = json.loads(response.read())
			#conn.close()
			if data['result']:
				player_id = data['result'][0]["playerid"]

				return player_id



	#RETRIEVE ALL AUDIO CONTENT
	#def getAudio(self):

		#DEBUG
	#	print 'getAudio()'
 	#	request = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "id": "retrieveSongs", "params": { "limits": { "start" : 0 }, "properties": ["artist"] }}'

         #       self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

	#	self.sendRequest('AudioLibrary.GetSongs', '{ "limits": { "start" : 0 }, "properties": ["artist", "file"] }', 'retrieveSongs')
	#	response = self.connection.getresponse()

	#	if response.status == httplib.OK:

	#		result = '{"audio":['
	#		json_data = json.loads(response.read())
	#		first = True
	#		for song in json_data['result']['songs']:
	#			if song['artist'] == []:
	#				song['artist'].append('Unknown')

	#			if first:
	#				first = False
	#				result += '{"title":"' + song['label'] + '", '
	#				result += '"artist":"' + song['artist'][0] + '", '
	#				result += '"id":' + str(song['songid']) + '}'
	#			else:
	#				result += ', '
	#				result += '{"title":"' + song['label'] + '", '					result += '"artist":"' + song['artist'][0] + '", '
	#				result += '"id":' + str(song['songid']) + '}'
#
#			result += ']}'
#			#print result
#			return result

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
				
				if song['artist'] == []:
					song['artist'].append('Unknown')
				if first:
					first = False
					result += '{"title":"' + song['label'] + '", '
					result += '"artist":"' + song['artist'][0] + '", '
					result += '"id":' + str(song['songid']) + '}'
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
		request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "limits": { "start" : 0, "end": 75 }, "properties" : ["art", "rating", "thumbnail", "playcount", "file"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}'

		self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(request, ''))

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			print response.read()
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

	def play(self, artist, id):

		path = self._findSong(artist, id)
		return self._play(path)

	def _play(self, path):

		#DEBUG
		print 'play() - ' + path

		req1 = '{"jsonrpc": "2.0", "method": "Playlist.Clear", "params":{"playlistid":1}, "id": "clearPlaylist"}'
		req2 = '{"jsonrpc": "2.0", "method": "Playlist.Add", "params":{"playlistid":1, "item" :{ "file" : "' + path + '"}}, "id" : "addToPlaylist"}'
		req3 = '{"jsonrpc": "2.0", "method": "Player.Open", "params":{"item":{"playlistid":1, "position" : 0}}, "id": "openPlaylist"}'
						
		#self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(req1, ''))
		self.connection.request('POST', '/jsonrpc', req1)

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			print response.read()
			
			#self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(req2, ''))
			self.connection.request('POST', '/jsonrpc', req2)

			response = self.connection.getresponse()
			if response.status == httplib.OK:
				print response.read()
				
				#self.connection.request('GET', '/jsonrpc?request=' + urllib.quote(req3, ''))
				self.connection.request('POST', '/jsonrpc', req3)

				response = self.connection.getresponse()
				if response.status == httplib.OK:
					print response.read()
					return True
				return False
			return False
		return False

	def _findSong(self, artist, id):

		#DEBUG
		print 'findSong() - ' + artist + str(id)

		request = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "limits": { "start" : 0 }, "properties": ["artist", "file"], "filter": {"artist": "' + artist + '"}}, "id": "findSong"}'

		self.connection.request('POST', '/jsonrpc', request)

		response = self.connection.getresponse()
		if response.status == httplib.OK:
			data = response.read()
			print data
			
			json_data = json.loads(data)

			for song in json_data['result']['songs']:
				if song['songid'] == id :
					return song['file']
			

###




