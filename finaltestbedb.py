#!/usr/bin/python
import wx,sys,threading,os,sys,commands
import re,signal,zipfile,socket
import time,pexpect
import wx.gizmos as gizmos
from datetime import datetime

ID=wx.NewId()

class TestBed(wx.Frame):
    def __init__(self,parent,id,title):
        # initialization of all widgets are done here
        wx.Frame.__init__(self,parent,id,title,wx.DefaultPosition,size=wx.Size(1000,750),style=wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.CAPTION)
        global username
        global username2
        global pswd
        menubar=wx.MenuBar() # for menu creation
        file=wx.Menu()        
        file.Append(101,'Quit','close the application')        
        menubar.Append(file,'File')        
        self.SetMenuBar(menubar)
        self.StatusBar=self.CreateStatusBar()
        self.Bind(wx.EVT_MENU,self.OnClose,id=101)        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        Container=wx.BoxSizer(wx.VERTICAL)   #total frame can be treat as container deviding into two panels as Heading and Worker panels....
        HeadingPanel=wx.Panel(self,-1,style=wx.SIMPLE_BORDER,size=wx.Size(900,90))
        HeadingPanel.SetBackgroundColour('gray')
        WorkerPanel=wx.Panel(self,-1,style=wx.SIMPLE_BORDER)        
        Container.Add(HeadingPanel,0,wx.EXPAND)
        Container.Add(WorkerPanel,1,wx.EXPAND|wx.ALL)
        self.SetSizer(Container)
        
        box1=wx.TextEntryDialog(None,'get username','','')
	if box1.ShowModal()==wx.ID_OK:
            username=box1.GetValue()
                
        Title=" Wireless Ad-hoc TestBed "
        HeadingFont=wx.Font(25,wx.ROMAN,wx.NORMAL,wx.NORMAL)
        Heading=wx.StaticText (HeadingPanel,-1,Title,(250,30),style=wx.ALIGN_CENTRE) # Heading panel to add Headings
        Heading.SetFont(HeadingFont)
       
        WorkerSizer=wx.BoxSizer(wx.HORIZONTAL) # Workers panel is devided into two more panels as worker1 and worker2
        self.Worker1=wx.Panel(WorkerPanel,-1)
        self.Worker1.SetBackgroundColour('gray')        
        self.Worker2=wx.Panel(WorkerPanel,-1)
        self.Worker2.SetBackgroundColour('gray')
        WorkerSizer.Add(self.Worker1,1,wx.EXPAND)
 
        WorkerSizer.Add(self.Worker2,1,wx.EXPAND)
        WorkerPanel.SetSizer(WorkerSizer)
        self.SideHeadingFont=wx.Font(15,wx.ROMAN ,wx.NORMAL,wx.NORMAL ) # Worker1 widgets are initialized here
        ProtocolSelection=wx.StaticText(self.Worker1,-1," Protocol Selection :",(20,50))
        ProtocolSelection.SetFont(self.SideHeadingFont)

        #for time display
        
        
        Protocols=["AODV","OLSR"]
        self.ProtocolValue=wx.ComboBox(self.Worker1,-1,pos=(230,50),size=(150,-1),choices=Protocols,style=wx.CB_DROPDOWN)
        NodeSelection=wx.StaticText(self.Worker1,-1," Node Selection :",(20,150))
        NodeSelection.SetFont(self.SideHeadingFont)
        self.Nodes=["1","2","3","4","5","6","7"]
        self.NodeValue=wx.ComboBox(self.Worker1,-1,pos=(230,150),size=(150,-1),choices=self.Nodes,style=wx.CB_DROPDOWN)
        DataRateSelection=wx.StaticText(self.Worker1,-1," Data Rate: ",(20,200))
        DataRateSelection.SetFont(self.SideHeadingFont)
        DataRates=["2","4","16","32"]
        self.DataRateValue=wx.ComboBox (self.Worker1,-1,pos=(230,200),size=(150,-1),choices=DataRates,style=wx.CB_DROPDOWN)
        wx.StaticText(self.Worker1,-1,"MB/s",(260,205))
        wx.Button(self.Worker1,1," APPLY CHANGES ",(50,280),size=(120,30))
        self.SyncButton=wx.Button(self.Worker1,2," Time Synchronisation",(210,280))
        os.system('sh run.sh')
        self.StartButton=wx.Button(self.Worker1,3," START ",(50,335),size=(90,30))
        self.StopButton=wx.Button(self.Worker1,4,"STOP",(210,335),size=(90,30))
       # self.PingButton=wx.Button(self.Worker1,15,"PING",(310,335),size=(90,30))
        self.SyncButton.Enable(False)
        self.StopButton.Enable(False)
        self.StartButton.Enable(False)        
        self.Bind(wx.EVT_BUTTON,self.OnApplyChanges,id=1)
        self.Bind(wx.EVT_BUTTON,self.Synchronisation,id=2)
        self.Bind(wx.EVT_BUTTON,self.OnStart,id=3)
        self.Bind(wx.EVT_BUTTON,self.OnStop,id=4)
       # self.Bind(wx.EVT_BUTTON,self.OnPing,id=15)
        FileTransfering=wx.StaticText(self.Worker1,-1," File Transfer:",(20,400))
        FileTransfering.SetFont(self.SideHeadingFont)
        self.CheckBox=wx.CheckBox(self.Worker1, -1, 'send raw data', (20,480))
        wx.EVT_CHECKBOX(self, self.CheckBox.GetId(), self.OnPing)
        self.CheckBox=wx.CheckBox(self.Worker1, -1, 'Is It Source Node', (20,450))
        wx.EVT_CHECKBOX(self, self.CheckBox.GetId(), self.ShowNodes)
        self.FileInput=wx.TextCtrl(self.Worker1,-1,"",pos=(20,550),size=(150,25))
        rawTransfer=wx.StaticText(self.Worker1,-1," no of raw data packets to be sent:",(20,520))
        self.rawInput=wx.TextCtrl(self.Worker1,-1,"",pos=(240,520),size=(90,25))
        self.LoadButton=wx.Button(self.Worker1,wx.NewId(),'load file',(180,550))
        self.Loaddir=wx.Button(self.Worker1,wx.NewId(),'load directory',(280,550))
        self.Bind(wx.EVT_BUTTON,self.OnLoad,id=self.LoadButton.GetId())
        self.Bind(wx.EVT_BUTTON,self.OnLoaddir,id=self.Loaddir.GetId())
        #self.fl=wx.TextCtrl(self.Worker1,-1,"",pos=(300,90),size=(70,30))
        self.TransferButton=wx.Button(self.Worker1,wx.NewId(),'Transfer',(50,570))
        self.Bind(wx.EVT_BUTTON,self.OnTransfer,id=self.TransferButton.GetId())
        
	self.SetAutoLayout(True)
	
	#self.p1=multiprocessing.Process(target=os.system, args=('bash /root/sch.sh',))
	
        NeighborsFound=wx.StaticText(self.Worker2,-1," Neighbors Detected:",(20,60))
        NeighborsFound.SetFont(self.SideHeadingFont)
        self.NeighborsDisplay=wx.TextCtrl(self.Worker2,-1,"",pos=(250,60),size=(190,50),style=wx.TE_MULTILINE)
        
        UploadText=wx.StaticText(self.Worker2,-1," Whom To Upload :",(40,210))
        UploadText.SetFont(self.SideHeadingFont)
        
        self.Destination=wx.TextCtrl(self.Worker2,-1,"",pos=(230,210),size=(150,30))
        UploadLogFiles=wx.Button(self.Worker2,6," Upload LogFiles",(140,250),size=(130,30))
        self.Bind(wx.EVT_BUTTON,self.UploadLogs,id=6)       
        self.SetBackgroundColour('yellow')  
        self.DestNode=""
        self.IP=""
        self.SelectedProtocol=""
        self.SelectedRate=""
        self.ProtocolCount=0
        self.Last=0
        self.LogFileName=""
        self.NeighborsDetected=[]
        self.neigh=[]
        self.neighb=['10.0.0.7','10.0.0.2','10.0.0.3','10.0.0.4','10.0.0.5','10.0.0.6']
        self.Old=[]
        self.GROUP="10.0.0.255" # broadcast address for this network
        self.PORT=10001  # port number
        self.argument=[]
        self.trans=""
        self.recv=""
        self.sent=[]
        
        self.loss=""
        self.flood=0
        self.t2="0"
        self.t3="0"
        self.weight=0.5
        self.weight1 = 0
        self.weight2=1 
        self.rrec2="0"
        self.rrec3="0"
        self.rfor2="0"
        self.rfor3="0"
        self.drec2="0"
        self.drec3="0"
        self.rth=30
        self.dth="0"
        self.fld=0
    

	

    def Onblackcheck(self,event):
         os.system("sysctl -w net.ipv4.ip_forward=0")
         
        
    def Onflood(self,event):
          print "text"
          self.flood=1 
          fpoint=file("/home/"+username+"/Desktop/flood.txt",'w')
          fpoint.writelines("1")
          fpoint.close()
                   
            

    def OnPing(self,event):
     global username
     if self.rawInput.GetValue()=="":
            self.dlg=wx.MessageDialog(self," Please Select the values ","warning",wx.OK|wx.ICON_ERROR)
            self.dlg.ShowModal()
            self.dlg.Destroy() 
     else :
       if self.SelectedProtocol=="OLSR" and self.IP=="10.0.0.1":
           wx.StaticText(self.Worker2,-1,"data packets dropped by each neighbor:",(40,290))
           self.ddrop=wx.TextCtrl(self.Worker2,-3,"",pos=(330,290),size=(100,50),style=wx.TE_MULTILINE)
           wx.StaticText(self.Worker2,-1," raw data packets forwarded by each neighbor:\n t2",(40,399))
           self.dfor=wx.TextCtrl(self.Worker2,-3,"",pos=(330,399),size=(100,50),style=wx.TE_MULTILINE)
           wx.StaticText(self.Worker2,-1,"raw data packets received by the node:\n t4",(40,510))
           self.drec=wx.TextCtrl(self.Worker2,-3,"",pos=(330,510),size=(100,50),style=wx.TE_MULTILINE)
           wx.StaticText(self.Worker2,-1,"blackhole \n trust value:",(0,565))
           self.brr=wx.TextCtrl(self.Worker2,-3,"",pos=(90,565),size=(70,50),style=wx.TE_MULTILINE)
           wx.StaticText(self.Worker2,-1,"flooding\n trust value:",(190,565))
           self.frr=wx.TextCtrl(self.Worker2,-3,"",pos=(270,565),size=(70,50),style=wx.TE_MULTILINE)
       else:
          if self.SelectedProtocol=="AODV" and self.IP=="10.0.0.1":
             wx.StaticText(self.Worker2,-1,"data packets dropped by each neighbor:",(40,290))
             self.ddrop=wx.TextCtrl(self.Worker2,-3,"",pos=(330,290),size=(100,50),style=wx.TE_MULTILINE)
             wx.StaticText(self.Worker2,-1,"rreq forwarded by each neigbor:\n (t1)",(40,345))
             self.rfor=wx.TextCtrl(self.Worker2,-3,"",pos=(330,345),size=(100,50),style=wx.TE_MULTILINE)
             wx.StaticText(self.Worker2,-1," raw data packets forwarded by each neighbor:\n (t2)",(40,399))
             self.dfor=wx.TextCtrl(self.Worker2,-3,"",pos=(330,399),size=(100,50),style=wx.TE_MULTILINE)
             wx.StaticText(self.Worker2,-1,"rreq received by the node:\n (t3)",(40,455))
             self.rrec=wx.TextCtrl(self.Worker2,-3,"",pos=(330,455),size=(100,50),style=wx.TE_MULTILINE)
             wx.StaticText(self.Worker2,-1,"raw data packets received by the node:\n (t4)",(40,510))
             self.drec=wx.TextCtrl(self.Worker2,-3,"",pos=(330,510),size=(100,50),style=wx.TE_MULTILINE)
             wx.StaticText(self.Worker2,-1,"blackhole \n trust value:",(0,565))
             self.brr=wx.TextCtrl(self.Worker2,-3,"",pos=(90,565),size=(70,50),style=wx.TE_MULTILINE)
             wx.StaticText(self.Worker2,-1,"flooding\n trust value:",(190,565))
             self.frr=wx.TextCtrl(self.Worker2,-3,"",pos=(270,565),size=(70,50),style=wx.TE_MULTILINE)

       if self.IP=="10.0.0.1":
         print "entered ping"
        
         for values in self.neighb:
           print "neighb="+str(values)
           print "start pinging"
           self.old= commands.getstatusoutput('hping3 -c %s -G -V -I wlan0 -s 8765 -p 80 %s'%(self.rawInput.GetValue(),values))
           print self.old
           filename="home/ape/Desktop/p"+str(values)
           fpoint=file(filename,'w')
           print fpoint
           fpoint.writelines("%s"%str(self.old))
           fpoint.close()
      
           self.trans=self.rawInput.GetValue()
           print self.trans
           fp=file(filename,'r')    
           for line in fp.readlines():
               MainString=re.search(r'\w+ packets received',line)
               print MainString.group().strip()
               if MainString:
                      SubString=re.search(r'\w+',MainString.group())
                      if SubString:
	                             self.recv=(SubString.group().strip())
           fp.close()
           print self.recv
           self.loss=int(self.trans)-int(self.recv)
           print "'''''''''''''''''''''''''''"
           print self.loss
           if values=="10.0.0.7":
              self.lost=self.loss
              print "lost packets="
              print self.lost
           if values=="10.0.0.2":               
                self.t2=(float(self.recv))/(float(self.trans))
                fpoint=file("/home/"+username+"/Desktop/aodvfile/10.0.0.2/log21.txt",'w')
                fpoint.writelines("%s=%s/%s"%(str(self.t2),str(self.recv),str(self.trans)))
                fpoint.close()
                for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.2":
                     self.dfor.AppendText('2:')
                     self.dfor.AppendText(str(self.t2))
                     self.dfor.AppendText('\n')
                     self.ddrop.AppendText('2:')
                     self.ddrop.AppendText(str(self.lost))
                     self.ddrop.AppendText('\n')
           if values=="10.0.0.3":               
                self.t3=(float(self.recv))/(float(self.trans))
                fpoint=file("/home/"+username+"/Desktop/aodvfile/10.0.0.3/log31.txt",'w')
                fpoint.writelines("%s=%s/%s"%(str(self.t3),str(self.recv),str(self.trans)))
                fpoint.close()
                for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.3":
                       self.dfor.AppendText('3:')
                       self.dfor.AppendText(str(self.t3))
                       self.dfor.AppendText('\n')
                       self.ddrop.AppendText('3:')
                       self.ddrop.AppendText(str(self.loss))
                       self.ddrop.AppendText('\n')
           if values=="10.0.0.4":               
                self.t4=(float(self.recv))/(float(self.trans))
                fpoint=file("/home/"+username+"/Desktop/aodvfile/10.0.0.4/log41.txt",'w')
                fpoint.writelines("%s=%s/%s"%(str(self.t4),str(self.recv),str(self.trans)))
                fpoint.close()
                for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.4":
                       self.dfor.AppendText('4:')
                       self.dfor.AppendText(str(self.t4))
                       self.dfor.AppendText('\n')
                       self.ddrop.AppendText('4:')
                       self.ddrop.AppendText(str(self.lost))
                       self.ddrop.AppendText('\n')
           if values=="10.0.0.5":               
                self.t5=(float(self.recv))/(float(self.trans))
                fpoint=file("/home/"+username+"/Desktop/aodvfile/10.0.0.5/log51.txt",'w')
                fpoint.writelines("%s=%s/%s"%(str(self.t5),str(self.recv),str(self.trans)))
                fpoint.close()
                for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.5":
                       self.dfor.AppendText('5:')
                       self.dfor.AppendText(str(self.t5))
                       self.dfor.AppendText('\n')
                       self.ddrop.AppendText('5:')
                       self.ddrop.AppendText(str(self.lost))
                       self.ddrop.AppendText('\n')
           if values=="10.0.0.6":               
                self.t6=(float(self.recv))/(float(self.trans))
                fpoint=file("/home/"+username+"/Desktop/aodvfile/10.0.0.6/log61.txt",'w')
                fpoint.writelines("%s=%s/%s"%(str(self.t6),str(self.recv),str(self.trans)))
                fpoint.close()
                for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.6":
                       self.dfor.AppendText('6:')
                       self.dfor.AppendText(str(self.t6))
                       self.dfor.AppendText('\n')
                       self.ddrop.AppendText('6:')
                       self.ddrop.AppendText(str(self.lost))
                       self.ddrop.AppendText('\n')
           
       else:
          for values in self.NeighborsDetected:
            os.system('hping3 -c %s -G -V -I wlan0 -s 8765 -p 80 %s'%(self.rawInput.GetValue(),values))
           
        
       if (self.IP=="10.0.0.1"):         
         if self.SelectedProtocol=="AODV":
              print "start aodv calculation"
              self.Timer()
         else:
            if self.SelectedProtocol=="OLSR":
                print "start olsr cal"
                self.olsrcal(30)           
         
        
     # When "ApplyChanges" button clicked   
    def OnApplyChanges(self,event):
        global username
        if self.ProtocolValue.GetValue()=="" or self.NodeValue.GetValue()=="" or self.DataRateValue.GetValue()=="" :
            self.dlg=wx.MessageDialog(self," Please Select the values ","warning",wx.OK|wx.ICON_ERROR)
            self.dlg.ShowModal()
            self.dlg.Destroy()
        else:   
               self.SelectedProtocol=self.ProtocolValue.GetValue()
               self.SelectedNode=self.NodeValue.GetValue()
               self.SelectedRate=self.DataRateValue.GetValue()
               self.IP="10.0.0." + self.SelectedNode
               
               NM_Status=os.popen('service network-manager status','r')#knowing the status of network manager
               if re.search(r'start/running',NM_Status.readline()):
                   os.system('stop network-manager')
               NM_Status.close()
               os.system('ifconfig wlan0 down')
               os.system('iwconfig wlan0 mode ad-hoc')             
               os.system('iwconfig wlan0 channel 11')
               os.system('ifconfig wlan0 up')
               os.system('iwconfig wlan0 essid "check"')
               os.system('iwconfig wlan0 rate "%d"'%int(self.SelectedRate))
               os.system('ifconfig wlan0 "%s" netmask 255.255.255.0' %(self.IP)) 
               print "syyyyyyyyybvv"
               self.SyncButton.Enable(True)
               self.dlg=wx.MessageDialog(self,"Selected IP=%s and Selected Protocol=%s " %(self.IP,self.SelectedProtocol),"Properties",wx.OK|wx.ICON_INFORMATION)
               self.dlg.ShowModal()
               self.dlg.Destroy() 
               userfile=file('/root/username.txt','w')
	       userfile.writelines(username)
               userfile.close()
        		
        if self.IP=="10.0.0.2" or self.IP=="10.0.0.3" or self.IP=="10.0.0.4" or self.IP=="10.0.0.5" or self.IP=="10.0.0.6":
               ModeSelection=wx.StaticText(self.Worker1,-1," Mode Selection :",(20,90))
               ModeSelection.SetFont(self.SideHeadingFont)
               self.CheckBoxF=wx.CheckBox(self.Worker1, -1, 'flooding', (230,90))
               self.CheckBoxB=wx.CheckBox(self.Worker1, -1, 'black hole', (230,120))
               wx.EVT_CHECKBOX(self, self.CheckBoxB.GetId(), self.Onblackcheck)
               wx.EVT_CHECKBOX(self, self.CheckBoxF.GetId(), self.Onflood)    
       
	#os.system('bash /root/sch.sh&')
     # showing the list of files and directories           
    def OnLoad(self,evt): 
                  global username2
                  global pswd              
                  self.FileInput.SetValue("")
                  dlg=wx.FileDialog(self,'choose file',os.getcwd (),'','*.*',wx.OPEN)
                  if dlg.ShowModal()==wx.ID_OK:
                      path=dlg.GetPath()               
                      self.FileInput.AppendText(path)
                      box2=wx.TextEntryDialog(None,'get username','','')
	              if box2.ShowModal()==wx.ID_OK:
                        username2=box2.GetValue() 
                  	box3=wx.TextEntryDialog(None,'get password','','')
	          	if box3.ShowModal()==wx.ID_OK:
                         pswd=box3.GetValue()         

    def OnLoaddir(self,evt): 
                  global username2
                  global pswd 
                  userPath="/home/"             
                  self.FileInput.SetValue("")
                  dlg=wx.DirDialog(None,"choose directory",style=1,defaultPath=userPath,pos=(10,10))
                  if dlg.ShowModal()==wx.ID_OK:
                      path=dlg.GetPath()               
                      self.FileInput.AppendText(path)
                      box2=wx.TextEntryDialog(None,'get username','','')
	              if box2.ShowModal()==wx.ID_OK:
                        username2=box2.GetValue() 
                  	box3=wx.TextEntryDialog(None,'get password','','')
	          	if box3.ShowModal()==wx.ID_OK:
                         pswd=box3.GetValue()  
                 
      # when transfer button clicked
    def OnTransfer(self,evt):
          global username2
          global pswd
          if self.FileInput.GetValue()=='':
             dlg=wx.MessageDialog(self,'first load any file','Warning',wx.OK|wx.ICON_ERROR)
             dlg.ShowModal()
          else:
               if self.CheckBox.GetValue()==False:
                     dlg=wx.MessageDialog(self,'This Is Not A Source Node','Warning',wx.OK|wx.ICON_ERROR)
                     dlg.ShowModal()
               elif self.DestNode=="":       
                           dlg=wx.MessageDialog(self,'Select Destination Node','Warning',wx.OK|wx.ICON_EXCLAMATION)
                           dlg.ShowModal()
               else:
                     try:
		              FileName=self.FileInput.GetValue()
		              Dest="10.0.0."+self.DestNode
                              fp=file('/tmp/logs/sources','w')
			      fp.write("Source=%s"%self.IP)
			      fp.write('\n')
			      fp.write("Destination=%s"%Dest)
			      fp.close()
                              t0 = time.clock()
                              print time.clock() - t0, "Start Time"
                              Transfer=TransferThread(FileName,Dest,self)
		              Transfer.start()
                     except Exception:		              
                             dlg=wx.MessageDialog(self,'Error in Transfering' ,'Error',wx.OK|wx.ICON_ERROR)
                             dlg.ShowModal()
                             dlg.Destroy()              
                                     
    # when close the application  
    def OnClose(self,event):
	global username
        self.Terminate=True
        try :
           self.thread.stop(self.Terminate)# for stopping protocol thread
           self.ProtocolCount=0
           
        except Exception: # if no protocol is running 
            NM_Status=os.popen('service network-manager status','r')
            if re.search(r'stop/waiting',NM_Status.readline()):
                 os.system('start network-manager')
            self.Destroy()

    # for showing transmission destination nodes...
    def ShowNodes(self,evt):
          
          if self.CheckBox.GetValue():                   
                   RemainNodes=[]
                   for node in self.Nodes:
                          if node!= self.NodeValue.GetValue():
                                RemainNodes.append(node)
                   self.DestinationNode=wx.StaticText(self.Worker1,-1," Destination Node:",(180,450))
                   self.DestinationNode.SetFont(wx.Font(9,wx.ROMAN,wx.NORMAL,wx.NORMAL))
                   self.DestinationValue=wx.ComboBox(self.Worker1,wx.NewId(),pos=(295,450),size=(50,-1),choices=RemainNodes,style=wx.CB_DROPDOWN)
                   self.Bind(wx.EVT_COMBOBOX,self.OnSelectDest,id=self.DestinationValue.GetId())
          else:
              
                   self.DestinationNode.Enable(False)
                   self.DestinationValue.Enable(False)
              
     # for catching selected node in the destination list/home/"+self.username+"/Desktop/"+self.FileName
    def OnSelectDest(self,evt):
            self.DestNode=self.DestinationValue.GetValue()
            
            
            
     # Showing neighbors when running any protocol.       
    def NeighborsDetection(self,Protocol):
                   if Protocol=="AODV":
                             
		             FP=file('/tmp/logs/aodv.txt')		             
		             TempList=[]
		             FP.seek(self.Last)                             
		             for Line in FP.readlines():                           
		                   MainStr=re.findall(r'(\w+\.\w+\.\w+\.\w+) new NEIGHBOR',Line)
		                   if MainStr:         		                           
		                        self.NeighborsDetected.append(MainStr[0])
                                        self.neigh.append(MainStr[0])
		                   MainStr2=re.findall(r'route_delete_timeout: (\w+\.\w+\.\w+\.\w+)',Line)
		                   if MainStr2:
		                        Removed=MainStr2[0]                                         
                                        for Neighbor in self.NeighborsDetected:
                                            if Neighbor!=Removed:                                              
                                                 TempList.append(Neighbor)                                                 
		                        self.NeighborsDetected=TempList		                        

                             
		             if self.NeighborsDisplay.GetValue()=='':		                                                        
		                    for ip in self.NeighborsDetected:
                                          self.Old.append(ip)
		                          self.NeighborsDisplay.AppendText(ip)
		                          self.NeighborsDisplay.AppendText('\n')
		                                     

		             else:   
                                                                 
		                   if self.Old != self.NeighborsDetected :                                        
		                          self.NeighborsDisplay.SetValue('')
		                          self.Old=[]                                          
		                          for ip in self.NeighborsDetected:
                                                self.Old.append(ip)
		                                self.NeighborsDisplay.AppendText(ip)
		                                self.NeighborsDisplay.AppendText('\n')
		      
		             self.Last=FP.tell()
		             FP.close()
                   

                   elif Protocol=="OLSR":                             
                             
                             FP=file('/tmp/logs/olsr')
                             
                             FP.seek(self.Last)
                             for Line in FP.readlines():
                                 NeighborIP=re.findall(r'Adding \w+\.\w+\.\w+\.\w+=>(\w+\.\w+\.\w+\.\w+)',Line)
                                 if NeighborIP:
                                      self.NeighborsDetected.append(NeighborIP[0])
                                      self.neigh.append(NeighborIP[0])
     
                                 RmIP=re.findall(r'TC: del edge entry (\w+\.\w+\.\w+\.\w+) > \w+\.\w+\.\w+\.\w+',Line)
                                 if RmIP:
                                     TempList=[]
                                     Removed=RmIP[0]                                     
                                     for Neighbor in self.NeighborsDetected:
                                         if Neighbor!=Removed:                                                
                                                TempList.append(Neighbor) 
                                     
                                     self.NeighborsDetected=TempList                                    
                             
                             
                             if self.NeighborsDisplay.GetValue()=='':		                    
		                    for ip in self.NeighborsDetected:

                                          self.Old.append(ip)
		                          self.NeighborsDisplay.AppendText(ip)
		                          self.NeighborsDisplay.AppendText('\n')
                                                                        
		                    
		             else:
		                  if self.Old != self.NeighborsDetected:
		                       self.NeighborsDisplay.SetValue('')
		                       self.Old=[]                                      
		                       for ip in self.NeighborsDetected:
                                              self.Old.append(ip)
		                              self.NeighborsDisplay.AppendText(ip)
		                              self.NeighborsDisplay.AppendText('\n')
                             self.Last=FP.tell()
		             FP.close()



 
                       
    # when start button is clicked.
    def OnStart(self,event):
	global username
        if self.ProtocolCount==0:    
            NM_Status=os.popen('service network-manager status','r')
            if re.search(r'start/running',NM_Status.readline()):        
                  os.system('ifconfig wlan0 down')
                  os.system('iwconfig wlan0 mode ad-hoc')             
                  os.system('iwconfig wlan0 channel 11')
                  os.system('ifconfig wlan0 up')
                  os.system('iwconfig wlan0 essid "check"')
                  os.system('iwconfig wlan0 rate "%d"'%int(self.SelectedRate))
                  os.system('ifconfig wlan0 "%s" netmask 255.255.255.0' %(self.IP)) 
            NM_Status.close()
            self.PreviousProtocol=self.SelectedProtocol
            self.StopButton.Enable(True)
            self.ProtocolCount=1
            self.LogFileName=self.IP+"_"+self.SelectedProtocol+".zip"

            FP=file('/root/.ssh/known_hosts','w')
            FP.write("")
            FP.close()
            self.cur=datetime.now()
            print self.cur    
            self.Daemonize()
            self.thread=WorkerThread(self.flood,self.SelectedProtocol,self.IP,self.SelectedRate,self.LogFileName,self)
            self.thread.start()           
            
        else:
             self.StatusBar.SetStatusText(' %s protocol Is Running '%(self.PreviousProtocol))
       
        if self.IP=='10.0.0.1':
		os.system("mkdir -p /home/"+username+"/Desktop/aodvfile/10.0.0.2")

		os.system("cd /home/"+username+"/Desktop/aodvfile;mkdir -p 10.0.0.3")
                os.system("chmod 777 /home/"+username+"/Desktop/aodvfile")#possible change
                timetaken=wx.StaticText(self.Worker2,-1,"time taken to calculate trust values:",(20,20))
                timetaken.SetFont(self.SideHeadingFont)
                self.td=wx.TextCtrl(self.Worker2,-1,"",pos=(400,20),size=(70,30))
                 

    # when stop button was clicked
    def OnStop(self,event):
        global username
        self.ProtocolCount=0
        self.thread.stop()
        os.system("rm -rf /home/"+username+"/Desktop/aodvfile")
        os.system("iptables -F")
        os.system("sysctl -w net.ipv4.ip_forward=1")        

     # when Time-synchronisation button was clicked
    def Synchronisation(self,evt):
          print("now in synchronisation")
          
          Set=False
          progressMax = 10
	  dialog = wx.ProgressDialog("Progress of Time Synchronization","Wait for 10 seconds for synchronize", progressMax,	style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME |wx.PD_REMAINING_TIME)
	  KeepGoing = True
	  count = 0
          if self.NodeValue.GetValue()=="1": # who is selected node value=1 then it can broadcast the time value
	        while KeepGoing and count < progressMax:
		    count = count + 1
                
                    service = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
                    service.setsockopt( socket.SOL_SOCKET, socket.SO_BROADCAST, 1 )
                    service.connect((self.GROUP,self.PORT))
                    
                    TimeValue=time.ctime(time.time())
                    service.send(TimeValue)
                    print "current time is",TimeValue
                   
                    Set=True

                    service.close()
                    wx.Sleep(1)
                    KeepGoing = dialog.Update(count)
          else: # remain nodes are ready to capture the time value
                 while KeepGoing and count<progressMax:
                       count=count+1                       
                       try:
		               if Set==False:                                                   
		                  s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		                  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)		                  
                                  socket.setdefaulttimeout(1.0)
		                  s.bind((self.GROUP, self.PORT))                          
		                  t,server=s.recvfrom(65535)                                                
		                  s.close()
		                  
                       except socket.timeout:
                              pass
                       
                       if t and Set==False:                            
                            os.system('date -s" %s"'%t)
                            Set=True
                        
                   
		       wx.Sleep(1)
		       KeepGoing = dialog.Update(count)
	  dialog.Destroy()
          if Set==False:
               print"Synchronisation failed"
          self.StartButton.Enable(True)
          
           
    # when upload log files button was clicked
    def UploadLogs(self,event):
          global username2
          global pswd
          box2=wx.TextEntryDialog(None,'get username','','')
	  if box2.ShowModal()==wx.ID_OK:
                        username2=box2.GetValue() 
          box3=wx.TextEntryDialog(None,'get password','','')
	  if box3.ShowModal()==wx.ID_OK:
                       pswd=box3.GetValue()         
          self.DestinationIP=self.Destination.GetValue()
          if re.search(r'\w+\.\w+\.\w+\.\w+',self.DestinationIP):                
                      FileName="/"+self.LogFileName                      
                      Dest=self.DestinationIP
                      Transfer=TransferThread(FileName,Dest,self)
                      Transfer.start()                                     

          else:
                 self.dlg=wx.MessageDialog(self,'Enter IP Address','Invalid Input',wx.OK|wx.ICON_ERROR)
                 self.dlg.ShowModal()
                 self.dlg.Destroy()
          
    # when any error occured in transfering a file
    def OnError(self):
                 dlg=wx.MessageDialog(self,'Error in Transfering','Error',wx.OK|wx.ICON_ERROR)
                 dlg.ShowModal()
                 dlg.Destroy()
     # when sucessfully transfered a file to selected destination
    def OnSucess(self,FileName,Destination):
                self.File=str(FileName)
                self.Dst=str(Destination)
                dlg=wx.MessageDialog(self," %s was sucessfully transfered to %s" %(self.File,self.Dst),"Transfer",wx.OK|wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                t0 = time.time()
                print time.time() - t0, "FILE RECEIVED TIME"   
    
    # run the application in background
    def Daemonize(self):
        try:
            pid=os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError,e:
            sys.stderr.write("fork #1 failed: %d (%s) \n" % (e.errno,e.strerror))
            sys.exit(1)
        os.chdir("/")
        os.setsid()
        os.umask(0)

        try:
            pid=os.fork()
            if pid > 0 :
                sys.exit(0)
        except OSError,e:
            sys.stderror.write("fork #2 failed: %d (%s) \n " % (e.errno,e.strerror))
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr .flush()   
                

             
    def Timer(self):
              global username
              for values in self.neighb:
                 if values=="10.0.0.2" :
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t3.txt"
                  if os.path.exists(self.PathToFetch):
                   
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec2=MainString.group().strip()
                   print "rrec2="+self.rrec2
	           fp6.close()
                  

                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor2=MainString.group().strip()
                   print "rfor2="+self.rfor2
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log22.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor2)))
                   fpoint.close()
                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.2":
                       self.rfor.AppendText('2:')
                       self.rfor.AppendText(str(self.rfor2))
                       self.rfor.AppendText('\n')                
                                    
 
                 if values=="10.0.0.3":
                  
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t3.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                     
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec3=MainString.group().strip()
	           fp6.close()
                   print "rrec3="+str(self.rrec3)
                            
                   
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor3=float(MainString.group().strip())
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log32.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor3)))
                   fpoint.close()
                   print "rfor3="+str(self.rfor3)
                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.3":
                     self.rfor.AppendText('3:')
                     self.rfor.AppendText(str(self.rfor3))
                     self.rfor.AppendText('\n')                  
                 
                 if values=="10.0.0.4":
                  
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t4.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                     
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec4=MainString.group().strip()
	           fp6.close()
                   print "rrec4="+str(self.rrec4)
                            
                   
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor4=float(MainString.group().strip())
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log32.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor4)))
                   fpoint.close()
                   print "rfor4="+str(self.rfor4)

                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.4":
                     self.rfor.AppendText('4:')
                     self.rfor.AppendText(str(self.rfor4))
                     self.rfor.AppendText('\n')
                 
                 if values=="10.0.0.5":
                  
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t5.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                     
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec5=MainString.group().strip()
	           fp6.close()
                   print "rrec5="+str(self.rrec5)
                            
                   
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor5=float(MainString.group().strip())
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log32.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor5)))
                   fpoint.close()
                   print "rfor5="+str(self.rfor5)
                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.5":
                     self.rfor.AppendText('5:')
                     self.rfor.AppendText(str(self.rfor5))
                     self.rfor.AppendText('\n')

                 if values=="10.0.0.5":
                  
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t5.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                     
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec5=MainString.group().strip()
	           fp6.close()
                   print "rrec5="+str(self.rrec5)
                            
                   
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor5=float(MainString.group().strip())
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log32.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor5)))
                   fpoint.close()
                   print "rfor5="+str(self.rfor5)
                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.5":
                     self.rfor.AppendText('5:')
                     self.rfor.AppendText(str(self.rfor5))
                     self.rfor.AppendText('\n')
                 if values=="10.0.0.6":
                  
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t6.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                     
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec6=MainString.group().strip()
	           fp6.close()
                   print "rrec6="+str(self.rrec6)
                            
                   
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor6=float(MainString.group().strip())
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log32.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor6)))
                   fpoint.close()
                   print "rfor6="+str(self.rfor6)
                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.6":
                     self.rfor.AppendText('6:')
                     self.rfor.AppendText(str(self.rfor6))
                     self.rfor.AppendText('\n')
                 if values=="10.0.0.7":
                  
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t7.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                     
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rrec7=MainString.group().strip()
	           fp6.close()
                   print "rrec7="+str(self.rrec7)
                            
                   
                  self.PathToFetch="/home/"+username+"/Desktop/aodvfile/"+values+"/t1.txt"
                  if os.path.exists(self.PathToFetch):
                   fp6=file(self.PathToFetch,'r')
                   for Line in fp6.readlines():
	                     MainString=re.search(r'\w+',Line)
	                     self.rfor7=float(MainString.group().strip())
	           fp6.close()
                   fpoint=file("/home/"+username+"/Desktop/aodvfile/log32.txt",'w')
                   fpoint.writelines("%s"%(str(self.rfor7)))
                   fpoint.close()
                   print "rfor7="+str(self.rfor7)
                  for neighbors in self.NeighborsDetected:
                   if neighbors=="10.0.0.7":
                     self.rfor.AppendText('7:')
                     self.rfor.AppendText(str(self.rfor7))
                     self.rfor.AppendText('\n')
                
              self.trustcal()           
              
 
    def trustcal(self):  
	      global username
              self.dth=2500
              self.t42=0
              self.t43=0
              self.fr2=0.0
              self.fd2=0.0
              self.fr3=0.0
              self.fd3=0.0
              self.ftrust2=0
              self.ftrust3=0
              self.btrust2=0
              self.btrust3=0
              
              
              for values in self.neighb:
                   if values=="10.0.0.2":
                        
                         os.system('tshark -r /tmp/logs/AodvOutput -R olsr -z "io,stat,1,tcp,ip.src==10.0.0.2,ip.dst==10.0.0.1">> /home/'+username+'/Desktop/aodvfile/10.0.0.2/t42.txt')
                         if os.path.exists("/home/"+username+"/Desktop/aodvfile/10.0.0.2/t42.txt"):
                           fp=file('home/'+username+'/Desktop/aodvfile/10.0.0.2/t42.txt','r')
                         
                           for line in fp.readlines():
                             MainString=re.search(r'\w+\.\w+-\w+\.\w+ \s+ \w+',line)
                             if MainString:
                                   SubString=re.search(r'\s+\w+',MainString.group())
                                   if SubString:
                                          self.t42=self.t42+int(SubString.group())
                           if self.rrec2<>"0":  
                            self.fr2=(1-((float(self.rrec2)-float(self.rth))/float(self.rth)))
                            fpoint=file("/home/"+username+"/Desktop/aodvfile/log23.txt",'w')
                            fpoint.writelines("%s=(1-((%s-%s)/%s))"%(str(self.fr2),str(self.rrec2),str(self.rth),str(self.rth)))
                            fpoint.close()
                         for neighbors in self.NeighborsDetected:
                            if neighbors=="10.0.0.2":
                              self.rrec.AppendText('2:')
                              self.rrec.AppendText(str(self.fr2))
                              self.rrec.AppendText('\n')
                      
                         if self.t42<>0:
                          self.fd2=(1-((float(self.t42)-float(self.dth))/float(self.dth)))
                         for neighbors in self.NeighborsDetected:
                            if neighbors=="10.0.0.2":
                              self.drec.AppendText('2:')
                              self.drec.AppendText(str(self.fd2))
                              self.drec.AppendText('\n')
                         fpoint=file("/home/"+username+"/Desktop/aodvfile/log24.txt",'w')
                         fpoint.writelines("%s=(1-((%s-%s)/%s))"%(str(self.fd2),str(self.t42),str(self.dth),str(self.dth)))
                         fpoint.close()
                   
                         if self.fr2<>0.0 and self.fd2<>0.0:
                          self.ftrust2=self.weight*(float(self.fr2)+float(self.fd2))
                         if self.ftrust2<>0:
                          print "trust value calculated"
                          if self.ftrust2>1:

                                 self.ftrust2=1
                          else:
                                 self.ftrust2=-1
                          print self.ftrust2
                         for neighbors in self.NeighborsDetected:
                             if neighbors=="10.0.0.2":
                               self.frr.AppendText('2:')
                               self.frr.AppendText(str(self.ftrust2))
                               self.frr.AppendText('\n')
                         if self.ftrust2<0:
                              os.system('iptables -A INPUT -s 10.0.0.2 -j DROP')
                              self.dlg=wx.MessageDialog(self,'10.0.0.2 detected as flooding nodeand dropped','trust value',wx.OK|wx.ICON_EXCLAMATION)
                              self.dlg.ShowModal()
                              self.dlg.Destroy()
                         
                         if self.rfor2<>0 and self.t2<>0:    
                          self.btrust2 = (self.weight1*float(self.rfor2)+self.weight2*float(self.t2))
		         print self.btrust2
                         if self.lost<>0:
                                self.btrust2=-1
                         if self.btrust2<>0:  
                           if self.btrust2>0.75:
                               self.btrust2=1
                           else :
                               self.btrust2=-1
                         for neighbors in self.NeighborsDetected:
                             if neighbors=="10.0.0.2":
                               self.brr.AppendText('2:')
                               self.brr.AppendText(str(self.btrust2))
                               self.brr.AppendText('\n')
                          
                           
                      
                           
                         if self.btrust2<0:
			     os.system('iptables -A INPUT -s 10.0.0.2 -j DROP')
                             self.dlg=wx.MessageDialog(self,'10.0.0.2 detected as malicious and dropped','trust value',wx.OK|wx.ICON_EXCLAMATION)
                             self.dlg.ShowModal()
                             self.dlg.Destroy()
                           

                   if values=="10.0.0.3": 
                      os.system('tshark -r /tmp/logs/AodvOutput -R olsr -z "io,stat,1,tcp,ip.src==10.0.0.3,ip.dst==10.0.0.1">> /home/'+username+'/Desktop/aodvfile/10.0.0.3/t43.txt')
                      if os.path.exists("/home/"+username+"/Desktop/aodvfile/10.0.0.3/t43.txt"):
                        fp=file('/home/'+username+'/Desktop/aodvfile/10.0.0.3/t43.txt','r')
                        for line in fp.readlines():
                             MainString=re.search(r'\w+\.\w+-\w+\.\w+ \s+ \w+',line)
                             if MainString:
                                   SubString=re.search(r'\s+\w+',MainString.group())
                                   if SubString:
                                          self.t43=self.t43+int(SubString.group())
                          
                        print "tshark value="+str(self.t43) 
                     
                      if self.rrec3<>0:
                         self.fr3=(1-((float(self.rrec3)-float(self.rth))/float(self.rth)))
                      for neighbors in self.NeighborsDetected:
                        if neighbors=="10.0.0.3":
                           self.rrec.AppendText('3:')
                           self.rrec.AppendText(str(self.fr3))
                           self.rrec.AppendText('\n')
                      fpoint=file("/home/"+username+"/Desktop/aodvfile/log33.txt",'w')
                      fpoint.writelines("%s=(1-((%s-%s)/%s))"%(str(self.fr3),str(self.rrec3),str(self.rth),str(self.rth)))
                      fpoint.close()
                      
                      if self.t43<>0:  
                       self.fd3=(1-((float(self.t43)-float(self.dth))/float(self.dth)))
                      for neighbors in self.NeighborsDetected:
                            if neighbors=="10.0.0.3":
                             self.drec.AppendText('3:')
                             self.drec.AppendText(str(self.fd3))
                             self.drec.AppendText('\n')

                      fpoint=file("/home/"+username+"/Desktop/aodvfile/log34.txt",'w')
                      fpoint.writelines("%s=(1-((%s-%s)/%s))"%(str(self.fd3),str(self.t43),str(self.dth),str(self.dth)))
                      fpoint.close()
                  
                      if self.rrec3<>0 and self.t43<>0:
                       self.ftrust3=self.weight*(float(self.rrec3)+float(self.t43))
                      if self.ftrust3<>0:
                       if self.ftrust3>1:
                               self.ftrust3=1
                       else:
                               self.ftrust3=-1
                      print self.ftrust3
                      for neighbors in self.NeighborsDetected:
                         if neighbors=="10.0.0.3":
                          self.frr.AppendText('3:')
                          self.frr.AppendText(str(self.ftrust3))
                          self.frr.AppendText('\n') 
                      if self.ftrust3<0:
                            os.system('iptables -A INPUT -s 10.0.0.3 -j DROP')
                            self.dlg=wx.MessageDialog(self,'10.0.0.3 detected as flooding node and dropped','trust values',wx.OK|wx.ICON_EXCLAMATION)
                            self.dlg.ShowModal()
                            self.dlg.Destroy() 
                      if self.rfor3<>0 and self.t3<>0:     
                       self.btrust3 = (self.weight1*float(self.rfor3)+self.weight2*float(self.t3))
		      print self.btrust3
                      if self.btrust3<>0:
                       print "trust for blackhole"
                       if self.btrust3>0.75:
                              self.btrust3=1
                       else:
                               self.btrust3=-1
                      for neighbors in self.NeighborsDetected:
                         if neighbors=="10.0.0.3":
                            self.brr.AppendText('3:')
                            self.brr.AppendText(str(self.btrust3))
                            self.brr.AppendText('\n')  
                       
                       
                        
                        
                      if self.btrust3<0:
			   os.system('iptables -A INPUT -s 10.0.0.3 -j DROP')
                           self.dlg=wx.MessageDialog(self,'10.0.0.3 detected as malicious node and dropped','trust values',wx.OK|wx.ICON_EXCLAMATION)
                           self.dlg.ShowModal()
                           self.dlg.Destroy()
                        
                       
              self.cur2=datetime.now()
              print self.cur2
              self.c=self.cur2-self.cur
              print self.c.seconds 
              self.td.SetValue(str(self.c.seconds))   

    def olsrcal(self,seconds): 
              self.runtime=seconds
              time.sleep(self.runtime) 
              self.dth=2500
              self.t42=0
              self.t43=0
              for values in self.neighb:
                   if values=="10.0.0.2":
                        #if os.path.exists('/home/ape/Desktop
                           os.system('tshark -r /tmp/logs/OlsrOutput -R aodv -z "io,stat,1,tcp,ip.src==10.0.0.2,ip.dst==10.0.0.1">> /home/'+username+'/Desktop/aodvfile/10.0.0.2/t42.txt')
                           fp=file('/home/'+username+'/Desktop/aodvfile/10.0.0.2/t42.txt','r')
                           for line in fp.readlines():
                             MainString=re.search(r'\w+\.\w+-\w+\.\w+ \s+ \w+',line)
                             if MainString:
                                   SubString=re.search(r'\s+\w+',MainString.group())
                                   if SubString:
                                          self.t42=self.t42+int(SubString.group())
                          
                           self.btrust2 = float(self.t2)
		           print self.btrust2
                         
                           if self.btrust2>0.75:
                               self.btrust2=1
                           else:
                               self.btrust2=-1
                           for neighbors in self.NeighborsDetected:
                             if neighbors=="10.0.0.2":
                              self.brr.AppendText('2:')
                              self.brr.AppendText(str(self.btrust2))
                              self.brr.AppendText('\n')                                  

                           self.fd2=(1-((float(self.t42)-float(self.dth))/float(self.dth)))
                           for neighbors in self.NeighborsDetected:
                             if neighbors=="10.0.0.2":
                               self.drec.AppendText('2:')
                               self.drec.AppendText(str(self.fd2))
                               self.drec.AppendText('\n')
                           fpoint=file("/home/"+username+"/Desktop/aodvfile/log24.txt",'w')
                           fpoint.writelines("%s=(1-((%s-%s)/%s))"%(str(self.fd2),str(self.t42),str(self.dth),str(self.dth)))
                           fpoint.close()
                   

                           self.ftrust2=float(self.fd2)
                           if self.ftrust2>1:
                                 self.ftrust2=1
                           else:
                                 self.ftrust2=-1
                           print self.ftrust2
                           for neighbors in self.NeighborsDetected:
                               if neighbors=="10.0.0.2":
                                   self.frr.AppendText('2:')
                                   self.frr.AppendText(str(self.ftrust2))
                                   self.frr.AppendText('\n')
                        
                           if self.ftrust2<1:
                              os.system('iptables -A INPUT -s 10.0.0.2 -j DROP')
                              self.dlg=wx.MessageDialog(self,'10.0.0.2 detected as flooding node and dropped','trust values',wx.OK|wx.ICON_EXCLAMATION)
                              self.dlg.ShowModal()
                              self.dlg.Destroy()
                           if self.btrust2<1:
			     os.system('iptables -A INPUT -s 10.0.0.2 -j DROP')
                             self.dlg=wx.MessageDialog(self,'10.0.0.2 detected as malicious node and dropped','trust values',wx.OK|wx.ICON_EXCLAMATION)
                             self.dlg.ShowModal()
                             self.dlg.Destroy()
              
                   if values=="10.0.0.3":
                        #if os.path.exists('/home/ape/Desktop
                           os.system('tshark -r /tmp/logs/OlsrOutput -R aodv -z "io,stat,1,tcp,ip.src==10.0.0.3,ip.dst==10.0.0.1">> /home/'+username+'/Desktop/aodvfile/10.0.0.3/t43.txt')
                           fp=file('/home/'+username+'/Desktop/aodvfile/10.0.0.3/t43.txt','r')
                           for line in fp.readlines():
                             MainString=re.search(r'\w+\.\w+-\w+\.\w+ \s+ \w+',line)
                             if MainString:
                                   SubString=re.search(r'\s+\w+',MainString.group())
                                   if SubString:
                                          self.t43=self.t43+int(SubString.group())
                          
                           self.btrust3 = float(self.t3)
		           print self.btrust3
                          
                        
                           if self.btrust3>0.75:
                               self.btrust3=1
                           else:
                               self.btrust3=-1
                           for neighbors in self.NeighborsDetected:
                                if neighbors=="10.0.0.3":
                                  self.brr.AppendText('3:')
                                  self.brr.AppendText(str(self.btrust3))
                                  self.brr.AppendText('\n')
                          
                          

                           self.fd3=(1-((float(self.t43)-float(self.dth))/float(self.dth)))
                           for neighbors in self.NeighborsDetected:
                               if neighbors=="10.0.0.3":
                                  self.drec.AppendText('3:')
                                  self.drec.AppendText(str(self.fd3))
                                  self.drec.AppendText('\n')
                           fpoint=file("/home/"+username+"/Desktop/aodvfile/log34.txt",'w')
                           fpoint.writelines("%s=(1-((%s-%s)/%s))"%(str(self.fd3),str(self.t43),str(self.dth),str(self.dth)))
                           fpoint.close()
                   

                           self.ftrust3=float(self.fd3)
                           if self.ftrust3>1:
                                 self.ftrust3=1
                           else:
                               self.ftrust3=-1
                           print self.ftrust3
                           for neighbors in self.NeighborsDetected:
                              if neighbors=="10.0.0.3":
                                 self.frr.AppendText('3-')
                                 self.frr.AppendText(str(self.ftrust3))
                                 self.frr.AppendText('\n')
                        
                           if self.ftrust3<1:
                              os.system('iptables -A INPUT -s 10.0.0.3 -j DROP')

                              self.dlg=wx.MessageDialog(self,'10.0.0.3 detected as flooding node and dropped','trust values',wx.OK|wx.ICON_EXCLAMATION)
                              self.dlg.ShowModal()
                              self.dlg.Destroy()
                           if self.btrust3<1:
			     os.system('iptables -A INPUT -s 10.0.0.3 -j DROP')
                             self.dlg=wx.MessageDialog(self,'10.0.0.3 detected as malicious node and dropped','trust values',wx.OK|wx.ICON_EXCLAMATION)
                             self.dlg.ShowModal()
                             self.dlg.Destroy()
              self.cur2=datetime.now()
              print self.cur2
              self.c=self.cur2-self.cur
              print self.c.seconds
              self.td.SetValue(str(self.c.seconds))    


# this can check about the given ip is pinging or not
class Ping(threading.Thread):
     def __init__(self,TestIP):
          threading.Thread.__init__(self)
          self.IP=TestIP
          self._stop=threading.Event()
          self.Result=None


     def run(self):
          lifeline = re.compile(r"(\d) received")
          Result=os.popen('ping -c 2 -i 0.2 "%s"'%(self.IP),'r') 
          while 1 :
               line = Result.readline()
               if not line:
                     break
               igot = re.findall(lifeline,line)               
               if igot:                  
                  if int(igot[0]) == 2: 
                        self.Result=True
                  else:                      
                       self.Result=False
          Result.close()
     
     def GetValue(self):
            
            return self.Result

     def stop(self):
            self._stop.set()  
        
   

# to start the selected protocol
class WorkerThread(threading.Thread):
    def __init__(self,flood,SelectedProtocol,IP,SelectedRate,LogFileName,window):
        threading.Thread.__init__(self)
        self.SelectedProtocol=SelectedProtocol        
        self.IP=IP
        self.flood=flood
        self.SelectedRate=SelectedRate
        self.Window=window
        self.finished=threading.Event()
        self.LogPath='/tmp/logs'
        self.LogFileName=LogFileName
        os.system('mkdir -p /tmp/logs')
        
        
    def run(self):
        if self.SelectedProtocol=="AODV": 
               os.system('tshark -p -i wlan0 -w /tmp/logs/AodvOutput &')
               time.sleep(0.5) 
               print('AODV is starting.......')                         
               os.system('aodvd -r 1 > /tmp/logs/aodv.txt &')
               time.sleep(0.2)
               
               
               while True and not self.finished.isSet():
                         
                         wx.CallAfter(self.Window.NeighborsDetection,self.SelectedProtocol)
                         self.finished.wait(1)
                        
        
       
                     
        else:
              if self.SelectedProtocol=='OLSR':	
                         os.system('tshark -p -i wlan0 -w /tmp/logs/OlsrOutput &') 
                         time.sleep(0.5)
                         print('OLSR is starting')
                         os.system('olsrd -i wlan0 >> /tmp/logs/olsr &')                                
                         time.sleep(0.5)
                         while True and not self.finished.isSet():
                                wx.CallAfter(self.Window.NeighborsDetection,self.SelectedProtocol)
                                self.finished.wait(1)
       
                
                                  
               

    def stop(self,Terminate=False): # for stop the selected protocol and start the network-manager
	 global username
         if not self.finished.isSet():
              self.finished.set()              
              if self.SelectedProtocol=="AODV":
                   self.ReturnValue=os.popen('pgrep aodv','r')                    
                   self.pid=self.ReturnValue.readline()
                   self.ReturnValue.close()                   
                   os.system('cp /var/log/aodvd.rtlog /tmp/logs/aodvd_rt.txt')   
                   print('aodv is closing')
              else:
                   if  self.SelectedProtocol=="OLSR":
                         self.ReturnValue=os.popen('pgrep olsrd','r')
                         self.pid=self.ReturnValue.readline()
                         self.ReturnValue.close()                     
           
                              
              os.system('kill "%d"'%int(self.pid))
              self.Window.NeighborsDisplay.SetValue('')
              self.Window.NeighborsDetected=[]
              self.Window.Old=[]
              self.Window.Last=0
              
	      self.ReturnValue=os.popen('pgrep tshark','r')                    
	      self.Tsharkpid=self.ReturnValue.readline()
	      self.ReturnValue.close()
	      os.system('kill "%d"'%int(self.Tsharkpid))
		      
           
                          
              zip = zipfile.ZipFile(self.LogFileName, 'w', zipfile.ZIP_DEFLATED)
              rootlen = len(self.LogPath) +1
              for base, dirs, files in os.walk(self.LogPath):
                     for filename in files:
                          fn = os.path.join(base, filename)        
                          zip.write(fn, fn[rootlen:])
              zip.close() 
              time.sleep(0.1)
              os.system('cp /'+self.LogFileName+' /home/'+username+'/Desktop')
              os.system('rm -rf %s'%self.LogPath) 
                         
              if Terminate:
                  self.Window.Destroy()
         else:
             if Terminate:
                  NM_Status=os.popen('service network-manager status','r')
                  if re.search(r'stop/waiting',NM_Status.readline()):
                        os.system('start network-manager')
                  NM_Status.close()
                  self.Window.Destroy()
             else:
                  self.Window.StatusBar.SetStatusText('No Protocol Is Running')
 

                 

# for file transfering
class TransferThread(threading.Thread):
       def __init__(self,FileName,Destination,Window):
               threading.Thread.__init__(self)
               self.FileName=FileName
               self.Destination=Destination
               self.Window=Window
       def run(self):
               
               global username2
               global pswd
               try:
                  print "before"
                  print pswd
                  print username2
		  
                  child = pexpect.spawn('scp -r -o StrictHostKeyChecking=no PubKeyAuthentication=no "%s" %s@"%s":/home/%s/Desktop'%(self.FileName,username2,self.Destination,pswd))
	          child.expect("password:")
	          child.sendline(pswd)
	          child.expect(pexpect.EOF, timeout = 15 * 60)
                  wx.CallAfter(self.Window.OnSucess,self.FileName,self.Destination)
                  print child.before
                  print 'after'
                  

               except Exception:
                         wx.CallAfter(self.Window.OnError)
                       

                              
              
class MyApp(wx.App):
    def OnInit(self):
        frame=TestBed(None,-1,'Test Bed')        
        frame.Show(True)
        return True

app=MyApp(0)
app.MainLoop()
