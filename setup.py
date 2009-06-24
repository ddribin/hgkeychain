from distutils.core import setup
from distutils.extension import Extension

setup(
	name = "hgkeychain",
	version = '0.1.1',
	author = 'Jonathan Wight',
	author_email = 'jwight@mac.com',
	url = 'http://toxicsoftware.com',
	description = 'Mercurial Keychain Extension',
	long_description = '''hgkeychain is an extension for mercurial that lets the user use the MacOS X keychain to store passwords for remote repositories.''',
	license = 'BSD',
	requires = [],
	py_modules = ['hgkeychain'],
	install_requires = ['pykeychain'],
	keywords = "mercurial hg version",
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: MacOS X',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: MacOS :: MacOS X',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Version Control'
		],
	platforms = 'MacOS X',

	)
