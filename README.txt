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
hgkeychain is aware of [auth] settings in your ~/.hgrc.  For example, if you have a BitBucket account, you could set this up as such:

  [auth]
  bb.prefix = bitbucket.org/
  bb.username = {username}
  bb.schemes =  http https

The prefix is used to store your password in keychain, so all repositories with the same prefix will share the same keychain item.  This keeps your keychain from getting cluttered up with a single keychain item per repository.  Note that [auth] requires at least Mercurial verion 1.3.

You can turn on logging to help debug problems like so:

  [hgkeychain]
  logging=1
