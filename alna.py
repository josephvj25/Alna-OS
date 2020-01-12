#!/usr/bin/env python
 
import gtk
import webkit
import gobject
import os
import time
import requests
import urllib
import zipfile
 
gobject.threads_init()

rotate=0

def draw_menubg(widget, event,user):
    
    file = open("users/"+user+"/wallpaper","r")
    path = "wall/"+file.readline().strip()
    file.close()
    pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)

def draw_loginbg(widget, event):
    path = 'login-bg.jpg'
    pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)
    
class LoginScreen() :
    
    def __init__(self) :
        
        self.win = gtk.Window()
        self.hbxUname = gtk.HBox(True)
        self.hbxPass = gtk.HBox(True)
        self.vbxLogin = gtk.VBox(True)
        
        self.lblUname = gtk.Label(10)
        self.lblUname.set_text("User Name")
        self.txtUname = gtk.Entry(20)
        self.lblPass = gtk.Label(10)
        self.lblPass.set_text("Password")
        self.txtPass = gtk.Entry(20)
        self.txtPass.set_visibility(False)
        self.imgLogin = gtk.Image()
        self.imgLogin.set_from_file("login.png")
        self.btnLogin = gtk.Button()
        self.btnLogin.add(self.imgLogin)
        self.imgShut = gtk.Image()
        self.imgShut.set_from_file("shutdown.png")
        self.btnShut = gtk.Button()
        self.btnShut.add(self.imgShut)
        self.imgRest = gtk.Image()
        self.imgRest.set_from_file("restart.png")
        self.btnRest = gtk.Button()
        self.btnRest.add(self.imgRest)
        self.imgLogo = gtk.Image()
        self.imgLogo.set_from_file("logo.png")
        self.btnLogo = gtk.Button()
        #self.btnLogo.add(self.imgLogo)
        
        self.map = self.btnLogin.get_colormap() 
        self.color = self.map.alloc_color("black")

        #copy the current style and replace the background
        self.style = self.btnLogin.get_style().copy()
        self.style.bg[gtk.STATE_NORMAL] = self.color
        self.style.bg[gtk.STATE_PRELIGHT] = self.color
        #set the button's style to the one you created
        self.btnLogin.set_style(self.style)
        self.btnRest.set_style(self.style)
        self.btnShut.set_style(self.style)
        self.btnLogo.set_style(self.style)
        
        
        self.hbxUname.pack_start(self.lblUname, fill=True, expand=True)
        self.hbxUname.pack_start(self.txtUname, fill=False, expand=False)
        self.hbxPass.pack_start(self.lblPass, fill=False, expand=True)
        self.hbxPass.pack_start(self.txtPass, fill=False, expand=False)       
                
        self.hbxBtns = gtk.HBox()
        '''
        self.hbxBtns.pack_start(self.btnRest,False,True)
        self.hbxBtns.pack_start(self.btnShut,False,True)
        self.hbxBtns.pack_start(self.btnLogin,False,True)'''
        
        '''self.imgLogo= gtk.Image()
        self.pxbLogo = gtk.gdk.pixbuf_new_from_file('logo.png')
        #self.pxbLogo.add(self.imgLogo)
        self.imgLogo.set_from_pixbuf(self.pxbLogo)#("logo.jpg")
        
        self.hbxBtns.pack_start(self.imgLogo,True,True)
        #self.pxbLogo.set_sensitive(False)
        
        self.vbxLogin.pack_start(self.hbxBtns,True,True)'''
        
        self.vbxLogin.pack_start(self.imgLogo,False,False)
        self.vbxLogin.pack_start(self.hbxUname,True,True)
        self.vbxLogin.pack_start(self.hbxPass,True,True)
        self.vbxLogin.pack_start(self.btnLogin, fill=False, expand=False)
        self.vbxLogin.pack_start(self.btnRest, fill=False, expand=False)
        self.vbxLogin.pack_start(self.btnShut, fill=False, expand=False)
        
        self.btnLogin.connect("clicked", self.loginCheck)
        self.btnRest.connect("clicked", self.restart)
        self.btnShut.connect("clicked", self.shutdown)
        self.vbxLogin.connect('expose-event', draw_loginbg)
        
        self.win.add(self.vbxLogin)
        self.win.show_all()
        self.win.fullscreen()
        
        print "login screen initialized"
        os.system("onboard&")
        
    def restart(self, object) :
        print "restart"
        os.system("shutdown -r now")
    
    def shutdown(self, object):
        print "shutdown"
        os.system("shutdown -P now")
        
    def loginCheck(self, object) :
        
        self.path = os.path.dirname(os.path.realpath(__file__))+"/users/"+self.txtUname.get_text()
        print self.path
        if os.path.isdir(self.path) and os.path.isfile(self.path+"/"+self.txtPass.get_text()) :
            print self.path+"/"+self.txtPass.get_text()
            print "Login Scuccesful"
            self.close(self.txtUname.get_text())
            self.win.destroy()
        else :
            print "Invalid Login Atempt"
            message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK)
            message.set_markup("Invalid User Name/Password.")
            message.run()
            message.destroy()
            
        self.txtPass.set_text("")
        self.txtUname.set_text("")
        self.txtUname.grab_focus()
    
    def close(self,uname) :
        
        print "login screen closed"

        objMenu = Menu(uname)
    
class Menu() :
    def __init__(self,uname) :
        self.uname = uname
        self.win = gtk.Window()
        self.NB = gtk.Notebook()
        self.NB.set_scrollable(True)
        self.NB.set_tab_pos(gtk.POS_BOTTOM)
       ##Settings Area START
        
        self.scMod = gtk.ScrolledWindow()
        self.tblMod = gtk.Table(3,3,True)
        
        self.scMod.set_policy(gtk.POLICY_NEVER,gtk.POLICY_NEVER)
        
        self.btnClock = gtk.Button()
        self.btnRotate = gtk.Button()
        self.btnKeyB = gtk.Button()
        self.btnUsers = gtk.Button()
        self.btnAppC = gtk.Button()
        self.btnWallP = gtk.Button()
        self.btnRst = gtk.Button()
        self.btnShut = gtk.Button()
        self.btnLog = gtk.Button()
        
        self.imgClock = gtk.Image()
        self.imgClock.set_from_file("gif/clock.gif")
        self.imgClock.show()
        self.btnClock.add(self.imgClock)
        
        self.imgUsers = gtk.Image()
        self.imgUsers.set_from_file("gif/users.gif")
        self.imgUsers.show()
        self.btnUsers.add(self.imgUsers)
        
        self.imgKeyB = gtk.Image()
        self.imgKeyB.set_from_file("gif/keyb.gif")
        self.imgKeyB.show()
        self.btnKeyB.add(self.imgKeyB)
        
        self.imgRot = gtk.Image()
        self.imgRot.set_from_file("gif/rotate.gif")
        self.imgRot.show()
        self.btnRotate.add(self.imgRot)
        
        self.imgAppC = gtk.Image()
        self.imgAppC.set_from_file("gif/appc.gif")
        self.imgAppC.show()
        self.btnAppC.add(self.imgAppC)
        
        self.imgWall = gtk.Image()
        self.imgWall.set_from_file("gif/wall.gif")
        self.imgWall.show()
        self.btnWallP.add(self.imgWall)
        
        self.imgRst = gtk.Image()
        self.imgRst.set_from_file("gif/restart.gif")
        self.imgRst.show()
        self.btnRst.add(self.imgRst)
        
        self.imgSht = gtk.Image()
        self.imgSht.set_from_file("gif/shutdown.gif")
        self.imgSht.show()
        self.btnShut.add(self.imgSht)
        
        self.imgLog = gtk.Image()
        self.imgLog.set_from_file("gif/logout.gif")
        self.imgLog.show()
        self.btnLog.add(self.imgLog)
        
        self.map = self.btnUsers.get_colormap() 
        self.color = self.map.alloc_color("black")
        #copy the current style and replace the background
        self.style = self.btnUsers.get_style().copy()
        self.style.bg[gtk.STATE_NORMAL] = self.color
        self.style.bg[gtk.STATE_PRELIGHT] = self.color
        #set the button's style to the one you created
        self.btnUsers.set_style(self.style)
        self.btnClock.set_style(self.style)
        self.btnRotate.set_style(self.style)
        self.btnKeyB.set_style(self.style)
        self.btnAppC.set_style(self.style)
        self.btnWallP.set_style(self.style)
        self.btnRst.set_style(self.style)
        self.btnShut.set_style(self.style)
        self.btnLog.set_style(self.style)
        
        
        self.tblMod.attach(self.btnClock,0,1,0,1)#,True,True,True,True)#
        self.tblMod.attach(self.btnRotate,1,2,0,1)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnKeyB,2,3,0,1)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnUsers,0,1,1,2)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnAppC,1,2,1,2)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnWallP,2,3,1,2)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnRst,0,1,2,3)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnShut,1,2,2,3)#,True,True,True,True)#False,False)
        self.tblMod.attach(self.btnLog,2,3,2,3)#,True,True,True,True)#False,False)
        
        self.btnLog.connect("clicked",self.logout)
        #self.btnAppC.connect("clicked",self.appc,uname,self.scMain) #ee line venda
        self.btnRotate.connect("clicked",self.rotater)
        self.btnClock.connect("clicked",self.clock)
        self.btnUsers.connect("clicked",self.users,uname)
        self.btnRst.connect("clicked",self.restart)
        self.btnShut.connect("clicked",self.shutdown)
        self.btnKeyB.connect("clicked",self.keyB)
        self.btnWallP.connect("clicked",self.wallp,uname)
        
        self.scMod.add_with_viewport(self.tblMod)
        self.scMod.show_all()
        
        imgMod = gtk.Image()
        imgMod.set_from_file("gif/mod.gif")
        hbxModBtn = gtk.HBox()
        lblMod = gtk.Label(time.strftime("%H:%M:%S", time.localtime()))
        hbxModBtn.pack_start(lblMod,False,False)
        hbxModBtn.pack_start(imgMod,False,False)
        def modTime():
            lblMod.set_text(time.strftime("%H:%M:%S", time.localtime()))
            gobject.timeout_add( 1000, modTime)
        modTime()
        hbxModBtn.show_all()
        self.NB.append_page(self.scMod,hbxModBtn)
        ##Setting Area STOP
        
        ##Menu Area START
        def menu_drw():
            scrMenu = gtk.ScrolledWindow()
            mitem_i = 0
            n=0 #no. of apps added counter
            print os.path.dirname(os.path.realpath(__file__))+"/users/"+uname+"/apps"
            print os.listdir(os.path.dirname(os.path.realpath(__file__))+"/users/"+uname+"/apps")
            print len(os.listdir(os.path.dirname(os.path.realpath(__file__))+"/users/"+uname+"/apps"))
            num = len(os.listdir(os.path.dirname(os.path.realpath(__file__))+"/users/"+uname+"/apps"))
            for i in range(0,6):
                if n==num :
                    break
                    print "break"
                for j in range(0,4):
                    mitem = MenuItem(mitem_i,uname)
                    mitem_i = mitem.id+1
                    n+=1
                    mitem.btn.connect("clicked",self.appOpen,mitem)
                    self.tblMenu.attach(mitem.btn,j,j+1,i,i+1,True,True,True,False)
                    if n==num :
                        break
                        print "break"
                    
            scrMenu.add_with_viewport(self.tblMenu)
        
            scrMenu.set_policy(gtk.POLICY_NEVER,gtk.POLICY_NEVER)
            self.tblMenu.connect('expose-event', draw_menubg,uname)
            
    
            self.micon = gtk.Image()
            self.micon.set_from_file("gif/menu.gif")
            self.micon.show()
            return scrMenu
        print "menu starts"
        self.tblMenu = gtk.Table(5,4,True)
        self.scMain = menu_drw()#gtk.ScrolledWindow()
        

        self.map = self.win.get_colormap() 
        self.color = self.map.alloc_color("black")

        #copy the current style and replace the background
        self.style = self.win.get_style().copy()
        self.style.bg[gtk.STATE_NORMAL] = self.color
        self.style.bg[gtk.STATE_SELECTED] = self.color
        #set the button's style to the one you created
        self.win.set_style(self.style)
        

        self.btnAppC.connect("clicked",self.appc,uname,self)
        self.NB.append_page(self.scMain,self.micon)
        self.win.add(self.NB)
        self.win.show_all()
        self.NB.set_current_page(1)
        self.win.fullscreen()
    def re_draw(self):
        self.tblMenu.destroy()
        self.tblMenu = gtk.Table(5,4,True)
        mitem_i = 0
        n=0 #no. of apps added counter
        num = len(os.listdir(os.path.dirname(os.path.realpath(__file__))+"/users/"+self.uname+"/apps"))
        for i in range(0,6):
            if n==num :
                break
                print "break"
            for j in range(0,4):
                mitem = MenuItem(mitem_i,self.uname)
                mitem_i = mitem.id+1
                n+=1
                mitem.btn.connect("clicked",self.appOpen,mitem)
                self.tblMenu.attach(mitem.btn,j,j+1,i,i+1,True,True,True,False)
                if n==num :
                    break
                    print "break"
        
        self.tblMenu.connect('expose-event', draw_menubg,self.uname)
        self.scMain.add_with_viewport(self.tblMenu)
        self.scMain.show_all()
    def appOpen(self, object,item):
        
        self.app = RunApp(item.path)
        self.hbxTitle = gtk.HBox()
        
        self.imgTray = gtk.Image()
        self.imgTray.set_from_file(item.path+"/ticon.png")
        self.imgTray.show()
        
        self.btnTitle = gtk.Button("X")
        self.hbxTitle.pack_start(self.imgTray)
        self.hbxTitle.pack_start(self.btnTitle)
        
        self.btnTitle.connect("clicked",self.appClose,self.app.scroll)
        self.hbxTitle.show_all()
        self.NB.insert_page(self.app.scroll,self.hbxTitle,2)
        self.NB.set_current_page(2)
        print "app opend"
    
    def appClose(self, object, app) :
        
        self.NB.remove_page(self.NB.page_num(app))
        app.destroy()
        print "app closed"
    
    def logout(self, object):
        self.win.destroy()
        objLoginScreen = LoginScreen()
    
    def wallp(self,object,uname):
        wall = Wall(uname)
    
    def users(self, object,uname):
        if os.path.isfile(os.path.dirname(os.path.realpath(__file__))+"/users/"+uname+"/admin"):
            usr = Users()
        else :
            print "not admin"
            message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK)
            message.set_markup("Only an admin user can manage the users. Please contact your system administrator.")
            message.run()
            message.destroy()
    def appc(self, object,uname,scr):
        ac = AppC(self,uname,scr)
    def clock(self, object):
        print "clock"
        winClock = gtk.Window(gtk.WINDOW_TOPLEVEL)
        winClock.fullscreen()
        lblTime = gtk.Label(time.strftime("%H:%M:%S %d %B %Y", time.localtime()))
        vbxClock = gtk.VBox()
        vbxClock.pack_start(lblTime)
        hbxEntry = gtk.HBox()
        adjH = gtk.Adjustment(float(time.strftime("%H", time.localtime())),00,23,1,1,0)
        spnH = gtk.SpinButton(adjH,1,0)
        spnH.set_wrap(True)
        adjM = gtk.Adjustment(float(time.strftime("%M", time.localtime())),00,59,1,1,0)
        spnM = gtk.SpinButton(adjM,1,0)
        spnM.set_wrap(True)
        adjS = gtk.Adjustment(float(time.strftime("%S", time.localtime())),00,59,1,1,0)
        spnS = gtk.SpinButton(adjS,1,0)
        spnS.set_wrap(True)
        adjd = gtk.Adjustment(float(time.strftime("%d", time.localtime())),00,31,1,1,0)
        spnd = gtk.SpinButton(adjd,1,0)
        spnd.set_wrap(True)
        adjY = gtk.Adjustment(float(time.strftime("%Y", time.localtime())),1970,2100,1,1,0)
        spnY = gtk.SpinButton(adjY,1,0)
        cmbB = gtk.combo_box_new_text()
        cmbB.append_text('Jan')
        cmbB.append_text('Feb')
        cmbB.append_text('Mar')
        cmbB.append_text('Apr')
        cmbB.append_text('May')
        cmbB.append_text('Jun')
        cmbB.append_text('Jul')
        cmbB.append_text('Aug')
        cmbB.append_text('Sep')
        cmbB.append_text('Oct')
        cmbB.append_text('Nov')
        cmbB.append_text('Dec')
        
        
        lblH = gtk.Label("Hour :")
        lblM = gtk.Label("Minute :")
        lblS = gtk.Label("Seconds :")
        lbld = gtk.Label("Day :")
        lblB = gtk.Label("Month :")
        lblY = gtk.Label("Year :")
        
        hbxEntry.pack_start(lblH)
        hbxEntry.pack_start(spnH)
        hbxEntry.pack_start(lblM)
        hbxEntry.pack_start(spnM)
        hbxEntry.pack_start(lblS)
        hbxEntry.pack_start(spnS)
        hbxEntry.pack_start(lbld)
        hbxEntry.pack_start(spnd)
        hbxEntry.pack_start(lblB)
        hbxEntry.pack_start(cmbB)
        hbxEntry.pack_start(lblY)
        hbxEntry.pack_start(spnY)
        
        def close(self,win):
            win.destroy()
        def setTime(self):
            print 'sudo date -s "'+str(int(spnd.get_value()))+' '+cmbB.get_active_text()+' '+str(int(spnY.get_value()))+' '+str(int(spnH.get_value()))+':'+str(int(spnM.get_value()))+':'+str(int(spnS.get_value()))+'"'
            os.system('sudo date -s "'+str(int(spnd.get_value()))+' '+cmbB.get_active_text()+' '+str(int(spnY.get_value()))+' '+str(int(spnH.get_value()))+':'+str(int(spnM.get_value()))+':'+str(int(spnS.get_value()))+'"')
            winClock.destroy()
            
        btnSet = gtk.Button("Set")
        vbxClock.pack_start(hbxEntry)
        vbxClock.pack_start(btnSet)
        btnSet.connect("clicked",setTime)
            
        def updateTime():
            lblTime.set_text(time.strftime("%H:%M:%S %d %B %Y", time.localtime()))
            gobject.timeout_add( 1000, updateTime)
        updateTime()
        btnCl = gtk.Button("Close")
        btnCl.connect("clicked",close,winClock)
        vbxClock.pack_start(btnCl)
        winClock.add(vbxClock)
        winClock.set_title("Set Time")
        winClock.show_all()
        print time.strftime("%H:%M:%S %d %B %Y", time.localtime())
    
    def rotater(self,object):
        global rotate
        if rotate == 0 :
            self.txt = "normal"
            rotate+=1
        elif rotate == 1 :
            self.txt = "left"
            rotate+=1
        elif rotate == 2 :
            self.txt = "inverted"
            rotate+=1
        elif rotate == 3 :
            self.txt = "right"
            rotate = 0
        
        print "xrandr -o "+self.txt+str(rotate)
        os.system("xrandr -o "+self.txt)
    
    def restart(self, object) :
        print "restart"
        os.system("shutdown -r now")
    
    def shutdown(self, object):
        print "shutdown"
        os.system("shutdown -P now")
    
    def keyB(self, object) :
        print "keybord"
        os.system("onboard")
        self.NB.set_current_page(1) 
            
class MenuItem():
    
    def __init__(self,i,uname):
        self.id = i
        self.path = os.path.dirname(os.path.realpath(__file__))+"/users/"+uname+"/apps/"
        print self.path
        while True :
            if not os.path.isdir(self.path+str(self.id)):
                self.id+=1
            else :
                break
        self.path +="/"+str(self.id)
        self.btn= gtk.Button()
        icon = gtk.Image()
        icon.set_from_file(self.path+"/icon.png")
        icon.show()
        self.btn.add(icon)

class RunApp() :
    
    def __init__(self,url) :
        self.bro = webkit.WebView()

        self.bro.open(url+"/index.html")
        self.scroll = gtk.ScrolledWindow()
        
        icon = gtk.Image()
        icon.set_from_file(url+"/icon.png")
        icon.show()
        self.scroll.add(self.bro)
        self.scroll.show_all()
class Users() :
    def __init__(self):
        winUsers = gtk.Window()
        winUsers.fullscreen()
        vbxUsers = gtk.VBox()
        path = os.path.dirname(os.path.realpath(__file__))+"/users"
        userList = os.listdir(path)
        txtUname = gtk.Entry(10)
        txtPass = gtk.Entry(10)
        lblU = gtk.Label("User Name")
        lblP = gtk.Label("Password")
        hbxUn = gtk.HBox()
        hbxPs = gtk.HBox()
        hbxUn.pack_start(lblU)
        hbxUn.pack_start(txtUname)
        hbxPs.pack_start(lblP)
        hbxPs.pack_start(txtPass)
        scrUsers = gtk.ScrolledWindow()
        scrUsers.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        vbxUser = gtk.VBox()
        for u in userList :
            hbxU = gtk.HBox()
            lblU = gtk.Label(u)
            btnDlt = gtk.Button("Delete")
            hbxU.pack_start(lblU)
            hbxU.pack_start(btnDlt)
            btnDlt.connect("clicked",self.dltUser,u,path,hbxU)
            vbxUser.pack_start(hbxU,True,False)
        scrUsers.add_with_viewport(vbxUser)
        vbxUsers.pack_start(scrUsers)
        btnAdd = gtk.Button("ADD")
        tglAdmin = gtk.ToggleButton("Make Admin")
        vbxUsers.pack_start(gtk.Label("Create a New User :"))
        vbxUsers.pack_start(hbxUn)
        vbxUsers.pack_start(hbxPs)
        vbxUsers.pack_start(tglAdmin)
        vbxUsers.pack_start(btnAdd)    
        btnC = gtk.Button("Close")
        btnC.connect("clicked",self.close,winUsers)
        vbxUsers.pack_start(btnC)
        btnAdd.connect("clicked",self.addUser,txtUname,txtPass,tglAdmin,winUsers)
        winUsers.add(vbxUsers)
        winUsers.show_all()
    
    def close(self, object, win):
        win.destroy()
    def dltUser(self,object,u,path,hbx):
        os.system("rm -r "+path+"/"+u)
        hbx.destroy()
    def addUser(self,object,u,p,a,winU):
        path = os.path.dirname(os.path.realpath(__file__))
        u = u.get_text()
        p = p.get_text()
        a = a.get_active()
        os.system("cp -r default_user users/"+u)
        path += "/users/"+u
        print path
        os.system("mv "+path+"/pass "+path+"/"+p)
        if not  a :
            os.system("rm "+path+"/admin")
        
        winU.destroy()
class AppC() :
    def __init__(self,object,user,s):
        
        url = "http://localhost/site88/"
        
        path = os.path.dirname(os.path.realpath(__file__))
        path +="/users/"+user+"/apps/"
        
        
        try :
            print requests.get(url).status_code
            if requests.get(url).status_code == 200 :
                print "IFED TRY"
                winAppC = gtk.Window()
                winAppC.fullscreen()
                scrAppC = gtk.ScrolledWindow()
                scrAppC.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
                vbxAppC = gtk.VBox()
                
                num = int(requests.get(url+"appId").content) + 1
                print num
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
                        btn.connect("clicked",self.deleteApp,num-1,user,winAppC,s)
                    else :
                        btn = gtk.Button("  Install ")
                        btn.connect("clicked",self.downloadApp,num-1,user,winAppC,url,s)
                    hbxAppItem.pack_start(btn,False, True)
            
    
                    vbxAppC.pack_start(hbxAppItem,False,False)
                    num -=1
                btnC = gtk.Button("Close")
                btnC.connect("clicked",self.close,winAppC)

                vbxAppC.pack_start(btnC,True,False)
                scrAppC.add_with_viewport(vbxAppC)
                winAppC.add(scrAppC)
                winAppC.show_all()
            
            else :
                print "server down in if statement"
                self.show_error_msg()
               
                
            
        except:
            print "serverdown"
            self.show_error_msg()
           
    
    def show_error_msg(self):
        message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK)
        message.set_markup("Unable to establish a connection with the Server. Please try agian later.")
        message.run()
        message.destroy()
    
    def downloadApp(self,object,appid, user,win,url,s):
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
        s.re_draw()
        win.destroy()
    def deleteApp(self,object,appid, user,win,s):
        print "delete "+str(appid)+" of "+user
        path = os.path.dirname(os.path.realpath(__file__))
        
        path +="/users/"+user+"/apps/"
        os.system("rm -r "+path+"/"+str(appid))
        s.re_draw()
        win.destroy()
    
    def close(self,object,win):
        win.destroy()

class Wall():
    def __init__(self,uname):
        winWall = gtk.Window()
        vbxWall = gtk.VBox()
        scrImgWin = gtk.ScrolledWindow()
        scrImgWin.set_policy(gtk.POLICY_NEVER,gtk.POLICY_AUTOMATIC)
        vbxImgWin = gtk.VBox()
        scrImgWin.add_with_viewport(vbxImgWin)
        btnClose = gtk.Button("Close")
        btnClose.connect("clicked",self.close,winWall)
        vbxWall.pack_start(scrImgWin,True,True)
        vbxWall.pack_start(btnClose,True,False)
        winWall.add(vbxWall)
        
        path = os.path.dirname(os.path.realpath(__file__))
        
        lstImages = os.listdir(path+"/wall/")
        for item in lstImages :
            btn = gtk.Button(item)
            btn.connect("clicked",self.change,item,uname)
            vbxImgWin.pack_start(btn,True,False)
        
        winWall.show_all()
        winWall.fullscreen()
    def close(self,object,win):
        win.destroy()
        print "wall closed"
    def change(self, object,item,user):
        file = open("users/"+user+"/wallpaper","w")
        file.write(item)
        file.close()
        print "wallpaper changed to %s" % item
if __name__ == "__main__" :
    objLoginScreen = LoginScreen()
    
    gtk.main()
