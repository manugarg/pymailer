from distutils.core import setup
import py2exe

setup(console=["pymailer.py"], 
		options = {"py2exe": {"packages": ["encodings"]}},
		)
setup(windows=["pymailerw.py"], 
		options = {"py2exe": {"packages": ["encodings"]}},
		)
setup(console=["installsendto.py"])
