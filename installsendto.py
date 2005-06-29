import sys, os, os.path

userhome = os.environ['USERPROFILE']
cwd=os.getcwd()

file=open(userhome+'\\SendTo\\pyMailer.bat','w')
fname, ext = os.path.splitext(sys.argv[0])

if ext == ".py":
	pypath=sys.prefix+'\\python'
	file.write(pypath+' '+cwd+'\\pymailerw.py %*')
else:
	file.write(cwd+'\\pymailerw %*')	
file.close()
