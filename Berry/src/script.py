print "haha"

from xbmcjson import XBMC
import time

#time.sleep(10)
	
print "Instansattion of XBMC"
xbmc = XBMC("http://127.0.0.1:8080/jsonrpc")


print "Show notification"
xbmc.GUI.ShowNotification({"title":"Salut", "message":"Hello World !!!"})
	
print "Switch to weather screen"
xbmc.GUI.ActivateWindow({"window":"weather"})


