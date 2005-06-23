# Copyright (C) 2005 Manu Garg <manugarg@gmail.com>

# This file is a Mail Transport Agent modules shipped with pyMailer.

# MTA class is basically a wrapper for smtplib. It provides for the
# easy interface to smtp servers including encryption and authentication
# enabled smtp servers.

# mta.py is a free software; you can redistribute  it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  

# mta.py is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with GML; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# Added handling for local smtp server - feb 23, 2005

import smtplib, sys

class MTA:
    '''MTA class - Wrapper for SMTP'''
    def __init__(self,confStr):
	'''Pass config string as  - "server:port|encrypt(TLS or '')|username|password" '''
	self.configstr = confStr
	self.config = {}
	self.errmsg=None
	self.initialized,mssg=self.parseconfig()
	print mssg
	
    def parseconfig(self):
	list=self.configstr.split('|')
	if len(list) != 4:
	    self.errmsg="Incorrect configuration string"
	    return(-1,self.errmsg)
	if list[2] != '':
	    if list[3] == '':
		self.errmsg="Password not specified in the config string"
		return(-1,self.errmsg)
	self.config['server'] = list[0]
	self.config['encrypt'] = list[1]
	self.config['username'] = list[2]
	self.config['password'] = list[3]
	return(1,"Initialized")
    
    def sendmail(self,mailfrom,to,mssg):
	if self.initialized == -1:
	    return(-1,'Not initialized yet')
	smtp = smtplib.SMTP()
	try:
	    if self.config['server'] == '':
		smtp.connect()
	    else:
		smtp.connect(self.config['server'])
	except:
	    self.errmsg="Could not connect to %s:%s" % (self.config['server'],sys.exc_info()[0])
	    return (-1,self.errmsg)
	try:
	    smtp.ehlo()
	    if self.config['encrypt'] == 'TLS':
		smtp.starttls()
		smtp.ehlo()
	    if self.config['username'] != '' and  self.config['password'] != '':
		smtp.login(self.config['username'], self.config['password'])
	    smtp.sendmail(mailfrom,to,mssg)
	except:
	    self.errmsg="Some error while sending message:",sys.exc_info()[0]
	    smtp.quit()
	    return (-1,self.errmsg)
	return (1,'Successfully sent the message')
	smtp.quit()
