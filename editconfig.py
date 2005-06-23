# Copyright (C) 2005 Manu Garg <manugarg@gmail.com>

# This file is a configuration file editor shipped with pyMailer.

# It is called from pyMailerw to edit smtp servers and contacts 
# configuration.

# editconfig.py is a free software; you can redistribute  it and/or 
# modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.  

# editconfig.py is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GML; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


from Tkinter import * 
import tkFont
from tkFileDialog import asksaveasfilename

class EditConfig(Frame):
    def __init__(self, parent=None,file=None):
        Frame.__init__(self, parent)
	self.file = file
	self.parent = parent
        self.pack(expand=YES, fill=BOTH)                 # make me expandable
        self.makewidgets()
        self.settext(self.file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)                  # xlink sbar and text
        text.config(font=tkFont.Font(family="Courier",size=10))
        text.config(yscrollcommand=sbar.set)             # move one moves other
	sbar.grid(row=0,column=1,sticky=N+S)	         # pack first=clip last
        text.grid(row=0,column=0,sticky=N+S+E+W)      	 # text clipped first
	buttF = Frame(self)
	Button(buttF, text='Save',  command=self.onSave)\
		.grid(row=1,column=0,sticky=SW)
	Button(buttF, text='Quit',  command=self.onQuit)\
		.grid(row=1,column=1,sticky=SW)
	buttF.grid(row=1,column=0,sticky=SW)
        self.text = text
    def settext(self, file=None):
        if file: 
            text = open(file, 'r').read()
	    self.text.delete('1.0', END)                     # delete current text
	    self.text.insert('1.0', text)                    # add at line 1, col 0
	    self.text.mark_set(INSERT, '1.0')                # set insert cursor
	    self.text.focus()                                # save user a click
    def onSave(self):
	if self.file == None:
	    self.file = asksaveasfilename()
	if self.file:
	    alltext = self.gettext() 
	    open(self.file, 'w').write(alltext)
    def onQuit(self):
	self.parent.destroy()
    def gettext(self):                                   # returns a string
        return self.text.get('1.0', END+'-1c')           # first through last
 
if __name__ == '__main__':
    root = Tk()
    try:
        st = EditConfig(file=sys.argv[1])              # filename on cmdline
    except IndexError:
        st = EditConfig(text='Words\ngo here')         # or not: 2 lines
    def show(event): print repr(st.gettext())            # show as raw string
    root.bind('<Key-Escape>', show)                      # esc = dump text
    root.mainloop()

