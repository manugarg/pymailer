from distutils.core import setup
import py2exe
      
setup(console=["pymailer.py"])
setup(windows=["pymailerw.py"])
setup(console=["installsendto.py"])
