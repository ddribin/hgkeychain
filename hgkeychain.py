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
Tested on Mercurial 1.3 w/Python 2.6 on Mac OS 10.6
'''

import mercurial.demandimport

from mercurial import (hg, repo, util)
from mercurial.i18n import _

try:
	from mercurial.url import passwordmgr
except:
	from mercurial.httprepo import passwordmgr

import logging
import urlparse
import urllib2
import keychain
import re

########################################################################################

logger = logging.getLogger('hgkeychain')
handler = logging.StreamHandler()
formatter = logging.Formatter("hgkeychain: %(levelname)-5s|%(name)s| %(message)s")
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

	def prefixUrl(self, base_url, prefix):
		if not prefix or prefix == '*':
			return base_url
		scheme, hostpath = base_url.split('://', 1)
		p = prefix.split('://', 1)
		if len(p) > 1:
			prefix_host_path = p[1]
		else:
			prefix_host_path = prefix
		shortest_url = scheme + '://' + prefix_host_path
		return shortest_url

	def find_user_password(self, realm, authuri):

		logger.debug('find_user_password() %s %s', realm, (authuri if len(authuri) < 50 else authuri[:47] + '...'))

		authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm.find_user_password(self, realm, authuri)
		theUsername, thePassword = authinfo

		if not hasattr(self, '_cache'):
			self._cache = {}

		auth = self.readauthtoken(authuri)
		keychainUri = authuri
		if auth:
			keychainUri = self.prefixUrl(authuri, auth.get('prefix'))
		logger.debug("Using URL for keychain: %s\n" % (keychainUri) )

		if not theUsername and auth:
			theUsername, thePassword = auth.get('username'), auth.get('password')
		if not theUsername:
			if not self.ui.interactive():
				raise util.Abort(_('hgkeychain: http authorization required'))
			self.ui.write(_("http authorization required\n"))
			self.ui.status(_("realm: %s\n") % realm)
			theUsername = self.ui.prompt(_("user:"), default=None)

		theKey = (realm, theUsername, keychainUri)
		if theKey in self._cache:
			return self._cache[theKey]

		if not thePassword:
			parsed_url = urlparse.urlparse(keychainUri)
			port = parsed_url.port if parsed_url.port else 0

			logger.info('Searching for username (%s) and url (%s) in keychain' % (theUsername, keychainUri))
			thePassword, theKeychainItem = keychain.FindInternetPassword(serverName = parsed_url.netloc, accountName = theUsername, port = port, path = parsed_url.path)

			if not thePassword:
				thePassword = self.ui.getpass(_('password for user \'%s\': ') % theUsername)
				if thePassword:
					logger.info('Storing username (%s) and url (%s) in keychain' % (theUsername, keychainUri))
					keychain.AddInternetPassword(serverName = parsed_url.netloc, accountName = theUsername, port = port, path = parsed_url.path, password = thePassword)

			if thePassword:
				self._cache[theKey] = (theUsername, thePassword)

		return theUsername, thePassword

########################################################################################

cmdtable = dict()

def uisetup(ui):
	theConfig = dict(ui.configitems('hgkeychain'))
	if 'logging' in theConfig:
		logger.setLevel(int(theConfig['logging']))
