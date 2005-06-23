# pymailerw.py is the graphical interface of pymailer package.

# pymailerw.py is a free software; you can redistribute  it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  

# pymailerw.py is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GML; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from Tkinter import *
from tkMessageBox import *
import sys, os, tkFileDialog, re
import pymailer
from editconfig import EditConfig

def askpassword(prompt):    
    win = Toplevel()       
    win.title('Password Prompt')
    Label(win, text=prompt).grid(row=0,column=0,padx=5,pady=10)
    entvar = StringVar()
    ent = Entry(win, textvariable=entvar, show='*')
    ent.grid(row=0,column=1,padx=5,pady=10)
    ent.bind('<Return>', lambda event, savewin=win: savewin.destroy())
    ent.focus_set(); win.grab_set(); win.wait_window()
    win.update()
    return entvar.get()    # ent widget is now gone


def getcontacts(conf):
    '''Opens the contacts file and 
    returns selected email addresses'''
    varlist=[]		   	#temp holder for var list
    win = Toplevel()       
    win.title('Select Contacts')
    r=0
    try:
	file = open(conf,'r')
    except:
	Label(win, justify=LEFT, text = "Config file not found")\
		.grid(row=r,column=0,sticky=W)
	r=r+1
	file = None
    if file:
	for line in file.readlines():
	    if re.match('^\s*$|^\s*#',line):
		continue
	    line = line.replace('\n','')
	    var=StringVar()
	    Checkbutton(win,text=line,variable=var,onvalue=line,anchor=W)\
		    .grid(row=r,column=0,sticky=W,padx=5)
	    varlist.append(var) 
	    r=r+1
	file.close()
    Button(win,text='Done',relief=GROOVE,command=win.destroy)\
	    .grid(row=r,column=0,sticky=W,padx=5,pady=5)
    win.grab_set(); win.wait_window()
    win.update()
    return (', ').join([v.get() for v in varlist if v.get()])
    

class RcptsFrame(Frame):
    def __init__(self, parent, conf):
	Frame.__init__(self,parent)
	self.conf = conf
	self.vars = []
	self.others = IntVar()
	self.make_widgets()	
    
    def make_widgets(self):
	r=0
	Label(self, justify=LEFT, text = "Select recipients:")\
		.grid(row=r,column=0,sticky=NW)
	r=r+1
	try:
	    file = open(self.conf,'r')
	except:
	    Label(self, justify=LEFT, text = "Config file not found")\
		    .grid(row=r,column=0,sticky=W)
	    r=r+1
	    file = None
	if file:
	    i=1
	    for to in file.readlines():
		if i>5:	break				#Not >5 on main window
		if re.match('^\s*$|^\s*#',to):		#comments and blank
		    continue
		to = to.replace('\n','')		
		var=StringVar()
		cb=Checkbutton(self,text=to,variable=var,onvalue=to,anchor=W)
		cb.grid(row=r,column=0,sticky=W,padx=5)
		if i==1: cb.select()
		self.vars.append(var) 
		r,i=r+1,i+1
	    file.close()
	self.o_cb=Checkbutton(self,text='Others (Comma seperated list)'\
		,variable=self.others,command=self.HandleOthers)
	self.o_cb.grid(row=r,column=0,sticky=W,padx=5)
	r=r+1
	self.e=Entry(self,state=DISABLED,width=30)
	self.e.grid(row=r,column=0,sticky=W,padx=10)
	Button(self, text="Find",relief=GROOVE, command=self.findContacts)\
		.grid(row=r,column=1,padx=5,pady=5,sticky=W)	
     
    def findContacts(self):
	self.o_cb.select()
	self.e.config(state=NORMAL)
	str=getcontacts(self.conf)
	self.e.insert(END, str)
    
    def HandleOthers(self):
	if self.others.get():
	    self.e.config(state=NORMAL)
	else:
	    self.e.config(state=DISABLED)
    
    def getVars(self):
	varlist = []
	for v in self.vars:
	    if v.get() and v.get() != '0':
		    varlist.append(v.get())
	if self.e.get() and self.others.get():
	    o_list= self.e.get().split(',')
	    for t in o_list:
		varlist.append(t)
	return varlist


class SenderFrame(Frame):
    def __init__(self, parent, conf=None):
	Frame.__init__(self,parent)
	self.conf = conf
	self.var = StringVar()
	self.make_widgets()	
    
    def make_widgets(self):
	r=0
	Label(self, justify=LEFT, text = "Select send options:")\
		.grid(row=r,column=0,sticky=NW)
	r=r+1
	try:
	    file = open(self.conf,'r')
	except:
	    Label(self, justify=LEFT, text = "(Config file not found)")\
		    .grid(row=r,column=0,sticky=NW)
	    r=r+1
	    file = None
	if file:
	    i=1
	    for smtpstr in file.readlines():
		if re.match('^\s*$|^\s*#',smtpstr):
		    continue
		smtpstr = smtpstr.replace('\n','')
		server,encrypt,username,passwd,sender = smtpstr.split('|') 
		sender = sender.replace('\n','')
		labelstr = sender+" @ "
		if server is '':
		    labelstr = labelstr+'localhost'
		else:
		    labelstr = labelstr+server
		if encrypt:
		    labelstr = labelstr+" ("+encrypt+")"
		rb=Radiobutton(self, text=labelstr,justify=LEFT, variable=self.var, value=smtpstr)
		rb.grid(row=r,column=0,sticky=W)
		if i==1: rb.select()
		r,i=r+1,i+1
	    file.close()
    
    def getVars(self):
	if self.var.get():
	    return self.var.get()
	else:
	    return None


class MailFrame(Frame):
    def __init__(self,parent,files=[]):
	Frame.__init__(self,parent)
	self.files = files
	self.sendinline = IntVar()
	Label(self,text='Subject').grid(row=0,column=0,sticky=NW,padx=5,pady=5)
	self.subject=Entry(self,width=25)
	self.subject.grid(row=0,column=1,padx=5,pady=5,sticky=NW)
	
	Label(self,text='Body(optional)')\
		.grid(row=1,column=0,sticky=NW,padx=5,pady=5)
	textF=Frame(self)
	sbar = Scrollbar(textF)
	self.body=Text(textF,height=4,width=40,relief=SUNKEN)
	sbar.config(command=self.body.yview)
	self.body.config(yscrollcommand=sbar.set)            
	sbar.grid(row=0,column=1,sticky=N+S)
	self.body.grid(row=0,column=0,padx=5,sticky=NW)
	textF.grid(row=1,column=1,pady=5,sticky=NW)

	Label(self,text='File').grid(row=2,column=0,sticky=NW,padx=5,pady=5)
	fileF=Frame(self)
	self.fileEnt=Entry(fileF,width=25)
	self.fileEnt.grid(row=0,column=0,padx=5,sticky=NW)
	if self.files != []:
	    FileNameStr = (' | ').join(self.files)
	    self.fileEnt.delete(0, END)
	    self.fileEnt.insert(0, FileNameStr)
	    self.subject.delete(0, END)
	    substr=('+').join([os.path.basename(file) for file in self.files])
	    self.subject.insert(0,substr)
	Button(fileF, text="Find",relief=GROOVE, command=self.FindFile)\
		.grid(row=0,column=1,padx=5,sticky=NW)	
	cb=Checkbutton(fileF,text="Send Inline",variable=self.sendinline,onvalue="1",anchor=W)
	cb.grid(row=0,column=2,sticky=NW,padx=5)
	fileF.grid(row=2,column=1,pady=5,sticky=NW)

    def FindFile(self):
	FileNames = tkFileDialog.askopenfilenames()
	if (FileNames==[]):
	    return
	FileNameStr = (' | ').join(FileNames)
	self.fileEnt.delete(0, END)
	self.fileEnt.insert(0, FileNameStr)
	self.subject.delete(0, END)
	substr=('+').join([os.path.basename(FileName) for FileName in FileNames])
	self.subject.insert(0,substr)
    
    def getVars(self):
	varslist = []
	filelist = []
	varslist.append(self.subject.get())
	varslist.append(self.body.get('1.0', END+'-1c'))
	if self.fileEnt.get():
	    filelist=self.fileEnt.get().split(' | ')
	varslist.append(filelist)
	varslist.append(self.sendinline.get())
	return varslist

# This is the main window
class MailerWin:
    def __init__(self,files=[]):
	self.files = files
	self.getconf()
	self.root = Tk()
        self.make_widgets_and_show()
	self.root.mainloop()

    def make_widgets_and_show(self):
	self.mainF = Frame(self.root)
	self.rcptsF = RcptsFrame(self.mainF,self.contactsconf)
	self.rcptsF.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
	self.smtpF = SenderFrame(self.mainF,self.smtpconf)
	self.smtpF.grid(row=0,column=1,sticky=NW,padx=5,pady=5)

	#mail frame
	self.mailF = MailFrame(self.mainF,self.files)
	self.mailF.grid(row=3,column=0,sticky=W,pady=20)
	
	buttF = Frame(self.mainF)
	Button(buttF,text='Send',relief=GROOVE,command=self.done,anchor=W)\
		.grid(row=0,column=0,padx=5)
	Button(buttF,text='Edit Contacts',relief=GROOVE,command=(lambda conf=self.contactsconf:self.editconf(conf)) )\
		.grid(row=0,column=1,padx=5)
	Button(buttF,text='Edit Send Options',relief=GROOVE,command=(lambda conf=self.smtpconf:self.editconf(conf)) )\
		.grid(row=0,column=2,padx=5)
	Button(buttF,text='Reload',relief=GROOVE,command=self.reload )\
		.grid(row=0,column=3,padx=5)
	buttF.grid(row=4,column=0,pady=5)

	self.mainF.pack()

    def reload(self):
	self.mainF.destroy()
	self.make_widgets_and_show()
	self.root.mainloop()

    def getconf(self):
	if sys.platform == 'win32':
	    userhome = os.environ['USERPROFILE']
	    self.smtpconf = userhome+'\\.pymailer\\.smtp.info'
	    self.contactsconf = userhome+'\\.pymailer\\.contacts.info'
	else:
	    userhome = os.environ['HOME']
	    self.smtpconf = userhome+'/.pymailer/.smtp.info'
	    self.contactsconf = userhome+'/.pymailer/.contacts.info'
	self.checkconf(self.contactsconf)
	self.checkconf(self.smtpconf)

    def checkconf(self,conf):
	if not os.path.exists(conf):
	    print "Config file not found. Trying creating"
	    if not os.path.exists(os.path.dirname(conf)):
		try:
		    os.makedirs(os.path.dirname(conf))
		except:
		    showinfo('Error','Could not create configuration directory %s' % (os.path.dirname(conf)))
		    sys.exit(1)
	    try:
		fd=file(conf,'w')
		if conf==self.contactsconf:
		    fd.write('#Enter email addresses. First 5 will appear on main window')
		if conf==self.smtpconf:
		    fd.write('#smtpserver:port|encrypt|username|password|sender\n')
		    fd.write('#smtp.gmail.com:587|TLS|user@gmail.com||user@gmail.com\n')
		    fd.write('#smtp.yourcompany.com||||user@ge.com\n')
		fd.close()
	    except:
		showinfo('Error','Could not create configuration file %s' % (conf))
		sys.exit(1)

    def editconf(self,conf):
	win = Toplevel()
	frame = EditConfig(win,conf)
	frame.pack()
	win.mainloop()

    def done(self):
	subject,mailbody,filelist,sendinline = self.mailF.getVars()
	rcptslist = self.rcptsF.getVars()
	if len(rcptslist) == 0:
	    showinfo('Error','Please select recipient/s')
	    return None
	smtp = self.smtpF.getVars()
	if smtp == None:
	    showinfo('Error',"Please select smtp server")
	    return None
	server,encrypt,username,passwd,sender = smtp.split('|')
	if username is not '' and passwd is '':
	    prompt = 'Password for %s on %s ' % (username,server)
	    passwd = askpassword(prompt)
	smtpstr = server+"|"+encrypt+"|"+username+"|"+passwd
	ret,msg=pymailer.Mail(rcpts=rcptslist, sender=sender,\
		smtpStr=smtpstr, subject=subject, body=mailbody,fileList=filelist,sendinline=sendinline)
	if ret == 1:
	    showinfo('Successful','Message Sent Successfully')
	    self.root.destroy()
	else:
	    showinfo('Some Error Occured',msg)

if __name__ == '__main__':
    try:
	files = []
	for filename in sys.argv[1:]:
	    if os.path.isfile(filename):
		files.append(filename)
	    if os.path.isdir(filename):
		for filename in os.listdir(filename):
		    path=os.path.join(filename,filename)
		    if not os.path.isfile(path):
			continue
		    files.append(path)
	MailerWin(files)              # filename on cmdline
    except IndexError:
        MailerWin()

print "I reached the end"
