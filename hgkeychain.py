#!/usr/bin/env python

'''
### How to install:

Drop _this_ file into your hgext directory. Location of this directory is install dependent.

See: http://www.selenic.com/mercurial/wiki/index.cgi/UsingExtensions?highlight=%28%28WritingExtensions%29%29

Edit your ~/.hgrc file to include:

[extensions]
MacOSXKeychain=

### Notes
Test on Mercurial 0.95 w/Python 2.5 on Mac OS 10.5
'''

import mercurial.demandimport
mercurial.demandimport.disable() # TODO - this is probably very bad.

from mercurial import (hg, repo)

try:
	from mercurial.url import passwordmgr
except:
	from mercurial.httprepo import passwordmgr

from mercurial.i18n import _

import urlparse
import urllib2
import Keychain

########################################################################################

cmdtable = dict()

# cmdtable = {
#     # cmd name        function call
#     "print-parents": (print_parents,
#                      # see mercurial/fancyopts.py for all of the command
#                      # flag options.
#                      [('s', 'short', None, 'print short form'),
#                       ('l', 'long', None, 'print long form')],
#                      "hg print-parents [options] node")
# }

# def extsetup():
# 	pass
# 
# def reposetup(ui, repo):
# 	pass
# 
# def print_parents(ui, repo, node, **opts):
# 	pass

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

	def find_user_password(self, realm, authuri):
		authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm.find_user_password(self, realm, authuri)
		theUsername, thePassword = authinfo
#		thePassword = thePassword if thePassword != '' else None

		if not hasattr(self, '_cache'):
			self._cache = {}
	
		theKey = (realm, authuri)
		if theKey in self._cache:
			return self._cache[theKey]

		if not theUsername:
			theUsername = self.ui.prompt(_("user:"), default=None)

		if not thePassword:
			parsed_url = urlparse.urlparse(authuri)
			port = parsed_url.port if parsed_url.port else 0
			thePassword, theKeychainItem = Keychain.FindInternetPassword(serverName = parsed_url.netloc, accountName = theUsername, port = port, path = parsed_url.path)

			if not thePassword:
				thePassword = self.ui.getpass(_('password for user \'%s\': ') % theUsername)
				if thePassword:
					Keychain.AddInternetPassword(serverName = parsed_url.netloc, accountName = theUsername, port = port, path = parsed_url.path, password = thePassword)

			if thePassword:
				self._cache[theKey] = (theUsername, thePassword)

		return theUsername, thePassword
