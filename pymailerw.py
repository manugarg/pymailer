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

__author__ = 'manugarg@gmail.com (Manu Garg)'

import Tkinter
#from tkMessageBox import *
from tkMessageBox import showinfo as showinfo
import tkFileDialog
import sys, os, re
import pymailer
from editconfig import EditConfig

def _AskPassword(prompt):
  win = Tkinter.Toplevel()
  win.title('Password Prompt')
  Tkinter.Label(win, text=prompt).grid(row=0, column=0, padx=5, pady=10)
  entvar = Tkinter.StringVar()
  ent = Tkinter.Entry(win, textvariable=entvar, show='*')
  ent.grid(row=0, column=1, padx=5, pady=10)
  ent.bind('<Return>', lambda event, savewin=win: savewin.destroy())
  ent.focus_set(); win.grab_set(); win.wait_window()
  win.update()
  return entvar.get()    # ent widget is now gone


def _GetContacts(conf):
  """
  Opens the contacts file and returns selected email addresses
  """
  varlist=[]                #temp holder for var list
  win = Tkinter.Toplevel()
  win.title('Select Contacts')
  r = 0
  try:
      file = open(conf, 'r')
  except:
      Tkinter.Label(win, justify=Tkinter.LEFT, text = "Config file not found")\
              .grid(row=r, column=0, sticky=Tkinter.W)
      r = r+1
      file = None
  if file:
    for line in file.readlines():
      if re.match('^\s*$|^\s*#', line):
        continue
      line = line.replace('\n', '')
      var = Tkinter.StringVar()
      Tkinter.Checkbutton(win, text=line, variable=var, onvalue=line,
                          anchor=Tkinter.W).grid(row=r, column=0,
                          sticky=Tkinter.W, padx=5)
      varlist.append(var)
      r = r+1
  file.close()
  Tkinter.Button(win, text='Done', relief=Tkinter.GROOVE,
                 command=win.destroy).grid(row=r, column=0, sticky=Tkinter.W,
                                           padx=5, pady=5)
  win.grab_set(); win.wait_window()
  win.update()
  return (', ').join([v.get() for v in varlist if v.get()])


class _RcptsFrame(Tkinter.Frame):
  def __init__(self, parent, conf):
    Tkinter.Frame.__init__(self, parent)
    self.conf = conf
    self.vars = []
    self.others = Tkinter.IntVar()
    self._MakeWidgets()

  def _MakeWidgets(self):
    r = 0
    Tkinter.Label(self, justify=Tkinter.LEFT, text = "Select recipients:")\
            .grid(row=r, column=0, sticky=Tkinter.NW)
    r = r+1
    try:
      file = open(self.conf, 'r')
    except:
      Tkinter.Label(self, justify=Tkinter.LEFT, text = "Config file not found")\
                .grid(row=r, column=0, sticky=Tkinter.W)
      r = r+1
      file = None
    if file:
      i = 1
      for to in file.readlines():
        if i > 5:  break                            #Not >5 on main window
        if re.match('^\s*$|^\s*#', to):            #comments and blank
            continue
        to = to.replace('\n', '')
        var = Tkinter.StringVar()
        cb = Tkinter.Checkbutton(self, text=to, variable=var,
                                 onvalue=to, anchor=Tkinter.W)
        cb.grid(row=r, column=0, sticky=Tkinter.W, padx=5)
        if i == 1: cb.select()
        self.vars.append(var)
        r, i = r+1, i+1
      file.close()
    self.o_cb = Tkinter.Checkbutton(self, text='Others (Comma seperated list)',
                          variable=self.others, command=self._HandleOthers)
    self.o_cb.grid(row=r, column=0, sticky=Tkinter.W, padx=5)
    r = r+1
    self.e=Tkinter.Entry(self, state=Tkinter.DISABLED, width=30)
    self.e.grid(row=r, column=0, sticky=Tkinter.W, padx=10)
    Tkinter.Button(self, text="Find", relief=Tkinter.GROOVE,
                   command=self._FindContacts).grid(row=r, column=1, padx=5,
                                                    pady=5, sticky=Tkinter.W)

  def _FindContacts(self):
    self.o_cb.select()
    self.e.config(state=Tkinter.NORMAL)
    str =_GetContacts(self.conf)
    self.e.insert(Tkinter.END, str)

  def _HandleOthers(self):
    if self.others.get():
      self.e.config(state=Tkinter.NORMAL)
    else:
      self.e.config(state=Tkinter.DISABLED)

  def _GetVars(self):
    varlist = []
    for v in self.vars:
      if v.get() and v.get() != '0':
        varlist.append(v.get())
    if self.e.get() and self.others.get():
      o_list = self.e.get().split(',')
      for t in o_list:
        varlist.append(t)
    return varlist


class _SenderFrame(Tkinter.Frame):
  def __init__(self, parent, conf=None):
    Tkinter.Frame.__init__(self, parent)
    self.conf = conf
    self.var = Tkinter.StringVar()
    self._MakeWidgets()

  def _MakeWidgets(self):
    r = 0
    Tkinter.Label(self, justify=Tkinter.LEFT, text = "Select send options:")\
            .grid(row=r, column=0, sticky=Tkinter.NW)
    r = r+1
    try:
      file = open(self.conf, 'r')
    except:
      Tkinter.Label(self, justify=Tkinter.LEFT, text="(Config file not found)")\
                .grid(row=r, column=0, sticky=Tkinter.NW)
      r = r+1
      file = None
    if file:
      i = 1
      for smtpstr in file.readlines():
        if re.match('^\s*$|^\s*#', smtpstr):
          continue
        smtpstr = smtpstr.replace('\n', '')
        server, encrypt, username, passwd, sender = smtpstr.split('|')
        sender = sender.replace('\n', '')
        labelstr = sender+" @ "
        if server is '':
          labelstr = labelstr+'localhost'
        else:
          labelstr = labelstr+server
        if encrypt:
          labelstr = labelstr+" ("+encrypt+")"
        rb = Tkinter.Radiobutton(self, text=labelstr, justify=Tkinter.LEFT,
                                 variable=self.var, value=smtpstr)
        rb.grid(row=r, column=0, sticky=Tkinter.W)
        if i == 1: rb.select()
        r, i = r+1, i+1
      file.close()

  def _GetVars(self):
    if self.var.get():
      return self.var.get()
    else:
      return None


class _MailFrame(Tkinter.Frame):
  def __init__(self, parent, files=[]):
    Tkinter.Frame.__init__(self, parent)
    self.files = files
    self.sendinline = Tkinter.IntVar()
    Tkinter.Label(self, text='Subject').grid(row=0, column=0,
                                            sticky=Tkinter.NW, padx=5, pady=5)
    self.subject = Tkinter.Entry(self, width=25)
    self.subject.grid(row=0, column=1, padx=5, pady=5, sticky=Tkinter.NW)

    Tkinter.Label(self, text='Body(optional)').grid(row=1, column=0,
                                              sticky=Tkinter.NW, padx=5, pady=5)
    textF = Tkinter.Frame(self)
    sbar = Tkinter.Scrollbar(textF)
    self.body = Tkinter.Text(textF, height=4, width=40, relief=Tkinter.SUNKEN)
    sbar.config(command=self.body.yview)
    self.body.config(yscrollcommand=sbar.set)
    sbar.grid(row=0, column=1, sticky=Tkinter.N+Tkinter.S)
    self.body.grid(row=0, column=0, padx=5, sticky=Tkinter.NW)
    textF.grid(row=1, column=1, pady=5, sticky=Tkinter.NW)

    Tkinter.Label(self, text='File').grid(row=2, column=0, sticky=Tkinter.NW,
                                          padx=5, pady=5)
    fileF = Tkinter.Frame(self)
    self.fileEnt = Tkinter.Entry(fileF, width=25)
    self.fileEnt.grid(row=0, column=0, padx=5, sticky=Tkinter.NW)
    if self.files != []:
      FileNameStr = (' | ').join(self.files)
      self.fileEnt.delete(0, Tkinter.END)
      self.fileEnt.insert(0, FileNameStr)
      self.subject.delete(0, Tkinter.END)
      substr=('+').join([os.path.basename(file) for file in self.files])
      self.subject.insert(0, substr)
    Tkinter.Button(fileF, text="Find", relief=Tkinter.GROOVE,
                   command=self._FindFile).grid(row=0, column=1, padx=5,
                                                sticky=Tkinter.NW)
    cb = Tkinter.Checkbutton(fileF, text="Send Inline", variable=self.sendinline,
                              onvalue="1", anchor=Tkinter.W)
    cb.grid(row=0, column=2, sticky=Tkinter.NW, padx=5)
    fileF.grid(row=2, column=1, pady=5, sticky=Tkinter.NW)

  def _FindFile(self):
    FileNames = tkFileDialog.askopenfilenames()
    if (FileNames == []):
        return
    FileNameStr = (' | ').join(FileNames)
    self.fileEnt.delete(0, Tkinter.END)
    self.fileEnt.insert(0, FileNameStr)
    self.subject.delete(0, Tkinter.END)
    substr = ('+').join([os.path.basename(FileName) for FileName in FileNames])
    self.subject.insert(0, substr)

  def _GetVars(self):
    varslist = []
    filelist = []
    varslist.append(self.subject.get())
    varslist.append(self.body.get('1.0', Tkinter.END+'-1c'))
    if self.fileEnt.get():
        filelist = self.fileEnt.get().split(' | ')
    varslist.append(filelist)
    varslist.append(self.sendinline.get())
    return varslist

# This is the main window
class _MailerWin:
  def __init__(self, files=[]):
    self.files = files
    self._GetConf()
    self.root = Tkinter.Tk()
    self._MakewidgetsAndShow()
    self.root.mainloop()

  def _MakewidgetsAndShow(self):
    self.mainF = Tkinter.Frame(self.root)
    self.mainF.option_add("*font", "Sans 11")
    self.rcptsF = _RcptsFrame(self.mainF, self.contactsconf)
    self.rcptsF.grid(row=0, column=0, sticky=Tkinter.NW, padx=5, pady=5)
    self.smtpF = _SenderFrame(self.mainF, self.smtpconf)
    self.smtpF.grid(row=0, column=1, sticky=Tkinter.NW, padx=5, pady=5)

    #mail frame
    self.mailF = _MailFrame(self.mainF, self.files)
    self.mailF.grid(row=3, column=0, sticky=Tkinter.W, pady=20)

    buttF = Tkinter.Frame(self.mainF)
    Tkinter.Button(buttF, text='Send', relief=Tkinter.GROOVE,
                   command=self._Done, anchor=Tkinter.W).grid(row=0, column=0,
                                                             padx=5)
    Tkinter.Button(buttF, text='Edit Contacts', relief=Tkinter.GROOVE,
           command=(lambda conf=self.contactsconf:self._EditConf(conf)))\
            .grid(row=0, column=1, padx=5)
    Tkinter.Button(buttF, text='Edit Send Options', relief=Tkinter.GROOVE,
           command=(lambda conf=self.smtpconf:self._EditConf(conf)))\
            .grid(row=0, column=2, padx=5)
    Tkinter.Button(buttF, text='Reload', relief=Tkinter.GROOVE,
                   command=self._Reload).grid(row=0, column=3, padx=5)
    buttF.grid(row=4, column=0, pady=5)

    self.mainF.pack()

  def _Reload(self):
    self.mainF.destroy()
    self._MakewidgetsAndShow()
    self.root.mainloop()

  def _GetConf(self):
    if sys.platform == 'win32':
      userhome = os.environ['USERPROFILE']
    else:
      userhome = os.environ['HOME']
    self.smtpconf = os.path.join(userhome, '.pymailer', 'smtp.txt')
    self.contactsconf = os.path.join(userhome, '.pymailer', 'contacts.txt')
    self._CheckConf(self.contactsconf)
    self._CheckConf(self.smtpconf)

  def _CheckConf(self, conf):
    if not os.path.exists(conf):
      print "Config file not found. Trying creating"
      if not os.path.exists(os.path.dirname(conf)):
        try:
          os.makedirs(os.path.dirname(conf))
        except:
          showinfo('Error', 'Could not create configuration directory %s' % \
              (os.path.dirname(conf)))
          sys.exit(1)
      try:
        fd = file(conf, 'w')
        if conf == self.contactsconf:
          fd.write('#Enter email addresses. First 5 will appear on main window')
        if conf == self.smtpconf:
          fd.write('#smtpserver:port|encrypt|username|password|sender\n')
          fd.write('#smtp.gmail.com:587|TLS|user@gmail.com||user@gmail.com\n')
          fd.write('#smtp.yourcompany.com||||user@ge.com\n')
        fd.close()
      except:
        showinfo('Error', 'Could not create configuration file %s' % (conf))
        sys.exit(1)

  def _EditConf(self, conf):
    win = Tkinter.Toplevel()
    frame = EditConfig(win, conf)
    frame.pack()
    win.mainloop()

  def _Done(self):
    subject, mailbody, filelist, sendinline = self.mailF._GetVars()
    rcptslist = self.rcptsF._GetVars()
    if len(rcptslist) == 0:
      showinfo('Error', 'Please select recipient/s')
      return None
    smtp = self.smtpF._GetVars()
    if smtp == None:
      showinfo('Error', 'Please select smtp server')
      return None
    server, encrypt, username, passwd, sender = smtp.split('|')
    if username is not '' and passwd is '':
      prompt = 'Password for %s on %s ' % (username, server)
      passwd = _AskPassword(prompt)
    smtpstr = server+"|"+encrypt+"|"+username+"|"+passwd
    ret, msg=pymailer.Mail(rcpts=rcptslist, sender=sender, smtpStr=smtpstr,
                          subject=subject, body=mailbody, fileList=filelist,
                          sendinline=sendinline)
    if ret == 1:
      showinfo('Successful', 'Message Sent Successfully')
      self.root.destroy()
    else:
      showinfo('Some Error Occured', msg)

if __name__ == '__main__':
  try:
    files = []
    for filename in sys.argv[1:]:
      if os.path.isfile(filename):
        files.append(filename)
      if os.path.isdir(filename):
        for file in os.listdir(filename):
          path = os.path.join(filename, file)
          if not os.path.isfile(path):
              continue
          files.append(path)
    _MailerWin(files)              # filename on cmdline
  except IndexError:
    _MailerWin()

print "I reached the end"
