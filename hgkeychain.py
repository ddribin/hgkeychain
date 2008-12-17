#!/usr/bin/env python

'''
### How to install:

Drop _this_ file into your hgext directory. Location of this directory is install dependent.

See: http://www.selenic.com/mercurial/wiki/index.cgi/UsingExtensions?highlight=%28%28WritingExtensions%29%29

Edit your ~/.hgrc file to include:

[extensions]
MacOSXKeychain=

### Notes
Tested on Mercurial 0.95 w/Python 2.5 on Mac OS 10.5
Tested on Mercurial 1.1 w/Python 2.5 on Mac OS 10.5
'''

import mercurial.demandimport
mercurial.demandimport.disable() # TODO - this is probably very bad.

from mercurial import (hg, repo)
from mercurial.i18n import _

try:
	from mercurial.url import passwordmgr
except:
	from mercurial.httprepo import passwordmgr

import logging

logger = logging.getLogger('hgkeychain')

handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)-5s|%(name)s| %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

########################################################################################

#### From http://mail.python.org/pipermail/python-dev/2008-January/076194.html

def monkeypatch_class(name, bases, namespace):
	assert len(bases) == 1, "Exactly one base class required"
	base = bases[0]
	for name, value in namespace.iteritems():
		if name != "__metaclass__":
			setattr(base, name, value)
	return base

########################################################################################

_find_user_password = passwordmgr.find_user_password

class MyHTTPPasswordMgr(passwordmgr):
	__metaclass__ = monkeypatch_class
	url_replacements = None

	def getExpressions(self):
		import simplejson
		import re

		theExpressions = dict()

		if self.url_replacements:
			for name, value in self.url_replacements:
				d = simplejson.loads(value)
				thePattern = d['pattern']
				theReplacement = d['replacement']
				thePattern = re.compile(thePattern)
				theExpressions[thePattern] = theReplacement
		return theExpressions
	expressions = property(getExpressions)

	def find_user_password(self, realm, authuri):
		import urlparse
		import urllib2
		import Keychain

		authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm.find_user_password(self, realm, authuri)
		theUsername, thePassword = authinfo

		if not hasattr(self, '_cache'):
			self._cache = {}

		theKey = (realm, authuri)
		if theKey in self._cache:
			return self._cache[theKey]

		if not theUsername:
			theUsername = self.ui.prompt(_("user:"), default=None)

		if not thePassword:
			for theExpression, theReplacement in self.expressions.items():
				theMatch = theExpression.match(str(authuri))
				if theMatch:
					newauthuri = theMatch.expand(theReplacement)
					if newauthuri:
						logger.info('Replacing original URL of (%s) with (%s)' % (authuri if len(authuri) < 50 else authuri[:47] + '...' , newauthuri))
						authuri = newauthuri
						break

			parsed_url = urlparse.urlparse(authuri)
			port = parsed_url.port if parsed_url.port else 0

			logger.info('Searching for username (%s) and url (%s) in keychain' % (theUsername, authuri))
			thePassword, theKeychainItem = Keychain.FindInternetPassword(serverName = parsed_url.netloc, accountName = theUsername, port = port, path = parsed_url.path)

			if not thePassword:
				thePassword = self.ui.getpass(_('password for user \'%s\': ') % theUsername)
				if thePassword:
					logger.info('Storing username (%s) and url (%s) in keychain' % (theUsername, authuri))
					Keychain.AddInternetPassword(serverName = parsed_url.netloc, accountName = theUsername, port = port, path = parsed_url.path, password = thePassword)

			if thePassword:
				self._cache[theKey] = (theUsername, thePassword)

		return theUsername, thePassword

########################################################################################

cmdtable = dict()

def uisetup(ui):
	theConfig = dict(ui.configitems('hgkeychain'))
	if 'logging' in theConfig:
		logger.setLevel(int(theConfig['logging']))

	MyHTTPPasswordMgr.url_replacements = ui.configitems('hgkeychain_url_replacements')
