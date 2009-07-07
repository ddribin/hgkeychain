About
=====
hgkeychain is an extension for mercurial that lets the user use the MacOS X keychain to store passwords for remote repositories.

Requirements
============
Mac OS X 10.5+ (should work on older OSes but only tested on 10.5 and 10.6)
Python 2.5 (should work on older versions of Python but only tested on 2.5 and 2.6)
Mercurial 0.9+ (works on 1.0 through 1.3)
My pykeychain Python Module

Installation
============
The easiest way to install hgkeychain is to use easy_install or pip:

	sudo easy_install -U pykeychain

(The sudo command may be optional depending on your machine's set up)

Activation
==========
Edit your ~/.hgrc file to activate the extension:

	[extensions]
	hgkeychain=

See http://www.selenic.com/mercurial/wiki/index.cgi/UsingExtensions for more information on installing and activating mercurial extensions.

Usage
=====
Once properly installed and activated hgkeychain will allow mercurial to store and retrieve repository passwords using the user's keychain.

You should generally embed the remote repository's username in the repository URL when performing a clone, push or pull operation. E.g.:

	http://username@example.com/hg/repository

If you try to clone, push or pull to a password protected repository mercurial will query the user's Keychain for the repository password. If no password is found, mercurial will prompt the user for the password (via the terminal) and then store the password in the Keychain.

Configuration
=============
You can turn on logging to help debug problems like so:

[hgkeychain]
logging=1

You can now map URL replacements to URL regular expressions. This is handy if you host a ton of repositories on a server and do NOT want your keychain cluttered up with a single keychain entry per repository.

The following example maps all repositories hosted on "example.com" and "example.local" to "example", resulting in just the one keychain entry.

(Note the syntax for this configuration is liable to change)

[hgkeychain_url_replacements]
url1 = {"pattern": "http://example\\.com/hg/.*)", "replacement": "http://example/hg/"}
url2 = {"pattern": "http://example\\.local\\/hg/.*", "replacement": "http://example/hg/"}

