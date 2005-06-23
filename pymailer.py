# This file is the command line interface of pyMailer package.

# pyMailer.py is a free software; you can redistribute  it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  

# pyMailer.py is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GML; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


'''
Usage: pymailer.py [options] to [to ...]*

Options:
    -h, --help	Print this message and exit.

    -a 		Attachment
    -s,--subject 
    		Subject
    -f,--from 	Fromaddr
    --smtpstr   Smtp string in the format 'server:port|encrypt|user|password'
    --smtpsvr	Smtp server in the format server:port. 
    		All other fields are considered empty in smtpstr

`to' is the email address of the recipient of the message, and multiple
recipients may be given.
'''

import mimetypes
import mta	#local
import sys, os
from email import Encoders
from email.Message import Message
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def Mail(sender, rcpts, smtpStr='|||', subject=None, body=None, fileList=[], sendinline=0):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = ', '.join(rcpts)
    msg['From'] = sender
    if body:
	msgbody = MIMEText(body)
	msg.attach(msgbody)
    for filename in fileList:
	ctype, encoding = mimetypes.guess_type(filename)
	if ctype is None or encoding is not None:
	    ctype = 'application/octet-stream'
	maintype, subtype = ctype.split('/',1)
	fp=open(filename,'rb')
	msgpart = MIMEBase(maintype, subtype)
	msgpart.set_payload(fp.read())
	fp.close()
	Encoders.encode_base64(msgpart)
	if sendinline:
	    msgpart.add_header('Content-Disposition', 'inline', filename=os.path.basename(filename))
	else:
	    msgpart.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filename))
	msg.attach(msgpart)
    smtp=mta.MTA(smtpStr)
    ret,msg=smtp.sendmail(sender,rcpts,msg.as_string())
    return (ret,msg)

def usage(code, msg=''):
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)

def main():
    import getopt
    attachList=[]
    try:
	opts,args = getopt.getopt(sys.argv[1:], 'ha:s:f:b:'\
		, ['help', 'subject=','from=','body=','smtpstr=','smtpsvr='])
    except getopt.error, msg:
        usage(1, msg)
	
    smtpstr,smtpsvr,fromaddr,sub='|||','','',''
    body=None 
    for opt, arg in opts:
	if opt in ('-h','--help'):
	    usage(0)
	elif opt in ('-a',):
	    attachList.append(arg)
	elif opt in ('-s','--subject'):
	    sub=arg
	elif opt in ('-f','--from'):
	    fromaddr=arg
        elif opt in ('--smtpstr',):
	    smtpstr=arg
        elif opt in ('--smtpsvr',):
	    smtpsvr=arg
        elif opt in ('--body',):
	    body=arg

    if len(args) < 1:	usage(1)
    
    if body == None:
	body=sys.stdin.read()
    if smtpsvr is not '' and smtpstr is '|||':
	smtpstr=smtpsvr+'|||'
    ret,msg=Mail(sender=fromaddr,rcpts=args,subject=sub,body=body,fileList=attachList,smtpStr=smtpstr)
    if ret==1:
	print "Message sent successfully"
    if ret == -1:
	print "Unsuccessful:",msg
		
if __name__ == '__main__':
    main()
