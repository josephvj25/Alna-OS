#!/usr/bin/env python

# example spinbutton.py

import gobject
import gtk
import os
import requests
import urllib
import zipfile

gobject.threads_init()

winAppC = gtk.Window()
winAppC.fullscreen()
scrAppC = gtk.ScrolledWindow()
scrAppC.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
vbxAppC = gtk.VBox()
url = "http://localhost/appc/"
user = "as"
path = os.path.dirname(os.path.realpath(__file__))
path +="/users/"+user+"/apps/"
def downloadApp(object,appid, user,win):
    print "downloading"
    print url+"zip/"+str(appid)+".zip"
    
    urllib.urlretrieve(url+"zip/"+str(appid)+".zip", "app.zip")
    zfile = zipfile.ZipFile("app.zip")
    path = os.path.dirname(os.path.realpath(__file__))
    
    path +="/users/"+user+"/apps/"
    print path
    os.mkdir(path+str(appid))
    zfile.extractall(path+"/"+str(appid))
    os.system("rm app.zip")
    win.destroy()
def deleteApp(object,appid, user,win):
    print "delete "+str(appid)+" of "+user
    path = os.path.dirname(os.path.realpath(__file__))
    
    path +="/users/"+user+"/apps/"
    os.system("rm -r "+path+"/"+str(appid))
    win.destroy()

def close(object,win):
    win.destroy()
    
if requests.get(url).status_code == 200 :
    
    num = int(requests.get(url+"appId").content) + 1
    while num :
        hbxAppItem = gtk.HBox()

        
        
        loader=gtk.gdk.PixbufLoader()
        loader.write(requests.get(url+"/icon/"+str(num-1)+".png").content)
        loader.close()
        ico = gtk.Image()
        ico.set_from_pixbuf(loader.get_pixbuf())
        hbxAppItem.pack_start(ico,False)
        hbxAppItem.pack_start(gtk.Label(requests.get(url+"/name/"+str(num-1)).content),True)
        
        installed = False
        for i in os.listdir(path):
            if int(i) == num-1 :
                installed = True
        
        if installed :
            btn = gtk.Button("Remove")
            btn.connect("clicked",deleteApp,num-1,user,winAppC)
        else :
            btn = gtk.Button("  Install ")
            btn.connect("clicked",downloadApp,num-1,user,winAppC)
        
        hbxAppItem.pack_start(btn,False, True)
        

        vbxAppC.pack_start(hbxAppItem,False,False)
        #downloadApp(num-1,"kt")
        
        num -=1
        
else :
    print "serverdown"

btnC = gtk.Button("Close")
btnC.connect("clicked",close,winAppC)

vbxAppC.pack_start(btnC,True,False)
scrAppC.add_with_viewport(vbxAppC)
winAppC.add(scrAppC)
winAppC.show_all()
gtk.main()