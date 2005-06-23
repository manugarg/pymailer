import sys, os

userhome = os.environ['USERPROFILE']
pypath=sys.prefix+'\\python'
cwd=os.getcwd()

file=open(userhome+'\\SendTo\\pyMailer.bat','w')
file.write(cwd+'\\pymailerw %1')
file.close()
