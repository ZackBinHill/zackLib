# -*- coding: utf-8 -*-
# ------------------------------ Introduction ------------------------------ #
"""
Zack Log
This module defines ZackLogger class to handle different types of outputs.
Here are their default actions to message:
	<1> debug     : print message
	<2> info	  : print, save message to log file
	<3> warning   : print, save message to log file 
	<4> error	  : print, save message to log file and send message
	<5> exception : convenience method for logging and Error with exception information
	<6> critical  : ptint, save message to log file and send message

The key configuration parameters are defined in zackLog.conf file.
like logMode, logPath, logLevel, logAction.
"""
__version__ = '1.0.0'

# ------------------------------ Import ------------------------------------ #
import os
import sys
import datetime
import getpass
import ConfigParser 
import logging
try:
	import zackGlobal
	import zackMessage
	import zackEmail
except Exception,e:
	print 'Log:  {0}'.format(e)

# ------------------------------ Variables --------------------------------- #
_logLevels = {10:'Debug', 20:'Info', 30:'Warning', 40:'Error', 50:'Critical'}

# ------------------------------ Function and Class ------------------------ #
class ZackLogConfigError(Exception):
	pass

def _getConfigPath():
	""" Gets the path of the zackLog configuration file. """
	paths = ['/etc', os.path.dirname(__file__)]

	# Get the current path of zackLogger
	scriptPath = sys.argv[0]
	if scriptPath != '' and scriptPath != '-c':
		# Make absolute path and eliminate any symlinks if any.
		scriptPath = os.path.abspath(scriptPath)
		scriptPath = os.path.realpath(scriptPath)
		# Add the zackLogger's directory to the path we'll search for the config.
		paths[:0] = [os.path.dirname(scriptPath)]

	# Search for a config file
	for path in paths:
		path = os.path.join(path, 'zacklog.conf')
		if os.path.exists(path):
			return path

	# No config file was found
	raise ZackLogConfigError('Config path not found, searched %s' % ', '.join(paths))

class ZackLogConfig(ConfigParser.ConfigParser):
	""" Class to get arguments from zackLog configuration file """
	def __init__(self, path):
		ConfigParser.ConfigParser.__init__(self)
		self.read(path)

	def getLogMode(self):
		if self.has_option('log', 'logMode'):
			return self.getint('log', 'logMode')
		else:
			raise ZackLogConfigError('Can not get log logMode in config file.')

	def getLogLevel(self):
		if self.has_option('log', 'logging'):
			return self.getint('log', 'logging')
		else:
			raise ZackLogConfigError('Can not get log logging in config file.')		

	def getLogPath(self):
		if self.has_option('log', 'logPath'):
			path = self.get('log', 'logPath')
			path = zackGlobal.formatString(path)
			return path
		else:
			raise ZackLogConfigError('Can not get log logPath in config file.')

	def getLogAction(self):
		if self.has_option('log', level):
			action = self.get('log', level)
			action_list = action.split('.')
			return [int(eath) for eath in action_list]
		else:
			return [0]


class ZackFileHandler(logging.FileHandler):
	""" This file handler is to add a user name before the log message. """
	def __init__(self, user, filename, mode='a', encoding=None, delay=0):
		logging.FileHandler.__init__(self, filename, mode=mode, encoding=encoding, delay=dalay)
		self.user = user

	def emit(self, record):
		""" Just to add a user name before the log message. """
		record.msg = '%s - %s' % (self.user, record.msg)
		logging.FileHandler.emit(self, record)

class ZackLogger(logging.Logger):
	def __init__(self, plugin, redipients='', user=zackGlobal.LOCAL_USER):
		"""
		Builds a logger instance
		Arguments:
			plugin: script name
			recopients: recipients for sending email or message to,
						can be a string like 'zack', or a list os users
			user: person who will use this logger instance, default value is local user
		"""
		logging.Logger = plugin

		self.plugin = plugin
		self.recipients = recipients
		self.user = user

		self._logConfig = ZackLogConfig(_getConfigPath())

		self._setStreamHandler()
		self._setFileHandler()

		# set default log level by root
		self.setLevel(self._logConfig.getLogLevel(), handler=0)

	def _setFileHandler(self):
		""" Set file handler. """
		log_path, self.nowDate = self._getLogPath()
		# print log path 
		self.file_handler = ZackFileHandler(self.user, log_path)
		# log format example: 2010-10-10 10:10:10,100 - WARNING - test log 5
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		self.file_handler.setFormatter(formatter)
		self.addHandler(self.FileHandler)

	def _setStreamHandler(self):
		""" Set stream handler. """
		self.stream_handler = logging.StreamHander()
		self.addHandler(self.stream_handler)

	def _getLogPath(self):
		"""
		Creates log struct and get log file path.
		mode0:
			[logPath]/[plugin]/[plugin.2010-10-10]
		mode1:
			[logPath]/[plugin]/[2010-10]/[plugin.2010-10-10]
		"""
		nowTime = datetime.datetime.now()
		nowMon = nowTime.strftime('%Y-%m')
		nowDate = nowTime.strftime('%Y-%m-%d')

		script_dir = '%s/%s' % (self._logConfig.getLogPath(), self.plugin)

		if self._logConfig.getLogMode() == 0:
			pass
		elif self._logConfig.getLogMode() == 1:
			script_dir = '%s/%s' % (script_dir, nowMon)

		if not os.path.exists(script_dir):
			os.makedirs(script_dir)

		log_path = '%s/%s.%s' % (script_dir, self.plugin, nowDate)

	def setLevel(self, level, handler=1):
		"""
		Logging message which are less severe than level will be ignored.
		Arguments:
			level      :log level can be 10/20/30/40/50
			handler    : <0> set level by root
						 <1> set level by file_handler - default
						 <3> set level by stream_handler
		"""
		if handler == 0:
			return logging.Logger.setLevel(self, level)
		elif handler == 1:
			return self.file_handler.setLevel(level)
		elif handler == 2:
			return self.stream_handler.setLevel(level)

	def debug(self, msg, *args, **kwargs):
		"""
		Logs a message with level Debug(10) on this logger and do action by configuration.
		Arguments:
			msg    - the msg is the message format string 
			args   - arguments to format the msg, msg % args
			kwargs - exc_info=None, extra=None
		To pass exception information, use the keyword argument exc_info with a true vale,
		e.g.
			logger.debug('Houston, we have a %s', 'thorny problem', exc_info=1
		"""
		self._doAction('debug', 10, mag, *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		"""
		Logs a message with level info(20) on this logger and do action by configuration.
		Arguments:
			msg    - the msg is the message format string 
			args   - arguments to format the msg, msg % args
			kwargs - exc_info=None, extra=None
		To pass exception information, use the keyword argument exc_info with a true vale,
		e.g.
			logger.debug('Houston, we have a %s', 'thorny problem', exc_info=1
		"""
		self._doAction('info', 20, mag, *args, **kwargs)

	def warning(self, msg, *args, **kwargs):
		"""
		Logs a message with level warning(30) on this logger and do action by configuration.
		Arguments:
			msg    - the msg is the message format string 
			args   - arguments to format the msg, msg % args
			kwargs - exc_info=None, extra=None
		To pass exception information, use the keyword argument exc_info with a true vale,
		e.g.
			logger.debug('Houston, we have a %s', 'thorny problem', exc_info=1
		"""
		self._doAction('warning', 30, mag, *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		"""
		Logs a message with level error(40) on this logger and do action by configuration.
		Arguments:
			msg    - the msg is the message format string 
			args   - arguments to format the msg, msg % args
			kwargs - exc_info=None, extra=None
		To pass exception information, use the keyword argument exc_info with a true vale,
		e.g.
			logger.debug('Houston, we have a %s', 'thorny problem', exc_info=1
		"""
		self._doAction('error', 40, mag, *args, **kwargs)

	def critical(self, msg, *args, **kwargs):
		"""
		Logs a message with level critical(50) on this logger and do action by configuration.
		Arguments:
			msg    - the msg is the message format string 
			args   - arguments to format the msg, msg % args
			kwargs - exc_info=None, extra=None
		To pass exception information, use the keyword argument exc_info with a true vale,
		e.g.
			logger.debug('Houston, we have a %s', 'thorny problem', exc_info=1
		"""
		self._doAction('critical', 50, mag, *args, **kwargs)

	def _doAction(slef, type, level, msg, *args, **kwargs):
		"""
		Do action according to configuration file.
		action:
			0: do nothing
			1: send message
			2: send email
		Arguments:
			type: debug, info, warning, error, critical
			level  - log level id
			mag    - message for sending email or message
			args   - arguments to format the msg, msg % args
			kwargs - exc_info=None, extra=None
		"""
		# set file handler
		nowTime = datetime.datetime.now()
		nowDate = nowTime.strftime('%Y-%m-%d')
		if self.nowDate < nowDate:
			self._setFileHandler()

		# log message
		func = getattr(logging.Logger, typ)
		func(self, msg, *args, **kwargs)

		# send message
		if self.recipients:
			if args:
				msg = msg % args
				msg = '%s\n- sent from %s' % (msg, self.user)

				action_list = self._logConfig.getLogAction(_logLevels[level])
				# print 'type: %s, action_list: %s' % (typ, action_list)
				for each_action in action_list:
					if each_action == 1:
						content = '[%s] %s\n%s' % (_logLevels[level].upper(), self.plugin, msg)
						zackMessage.send(self.recipients, content, account='exception')
					elif each_action == 2:
						title = '[%s] %s' % (_logLevels[level].upper(), self.plugin)
						zackMessage.send(self.recipients, title, msg, sender='exception')


# ------------------------------ Command line ------------------------------ #
if __name__ == '__main__':
	logger = ZackLogger('test', recipients='brian')
	logger.debug('debug')
	logger.info('info')
	logger.warning('warning')
	logger.error('error')
	logger.critical('critical')
