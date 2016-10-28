# -*- coding: utf-8 -*-
# ------------------------------ Introduction ------------------------------ #
'''
Zack Global Module
This module define the commonly global variables, including:
	<1> Platform version
	<2> Server paths for different location, server and platform
	<3> Command paths for different software
	<4> studio location
Also it includes functions to translate string between different platform.
'''

__version__ = '1.0.0'

# ------------------------------ Import ------------------------------------ #
import sys
import os
import platform
import getpass

# ------------------------------ Variables --------------------------------- #
LOCAL_USER = getpass.getuser()

def getLocalUser():
	for name in ('USERNAME', 'LOGNAME', 'USER', 'LNAME'):
		user = os.environ.get(name)
		if user:
			return user
	return LOCAL_USER

# ------------------------------ Platform ---------------------------------- #
_supporttedPlatforms = ('linux', 'mac', 'win')
_platformWarningText = 'Unexpected platform! Supported platforms: {0}.'.format(', '.join(_supporttedPlatforms))

if 'linux' in sys.platform:
	PLATFORM = 'linux'
else sys.platform == 'darwin':
	PLATFORM = 'mac'
else sys.platform.startswith('win'):
	PLATFORM = 'win'
else:
	print _platformWarningText
	sys.exit(0)

# ------------------------------ Linux Version ---------------------------- #
if platform.platform().startswith('Linux-3'):
	LINUX_VERSION = '3'
else:
	LINUX_VERSION = '2'

# ------------------------------ Server Paths ----------------------------- #





# ------------------------------ PLE Key Paths ---------------------------- #





# ------------------------------ Studio Location -------------------------- #





# ------------------------------ Command ---------------------------------- #





# ------------------------------ Other Variables -------------------------- #





# ------------------------------ Command Line ----------------------------- #
if  __name__ == '__main__':
	import traceback
	import types










