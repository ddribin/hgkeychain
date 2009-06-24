from distutils.core import setup
from distutils.extension import Extension

setup(
	name = "hgkeychain",
	version = '0.1',
	author = 'Jonathan Wight',
	author_email = 'jwight@mac.com',
	url = 'http://toxicsoftware.com',
	description = 'Mercurial Keychain Extension',
	long_description = '''TODO''',
	license = 'BSD',
	requires = [],
#	packages = ['Keychain'],
	install_requires = ['Keychain'],
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: MacOS X',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: MacOS :: MacOS X',
		],
	platforms = 'MacOS X',

	ext_modules = [
		Extension("Keychain", ["Keychain.pyx"], extra_link_args = ['-framework', 'Security', '-framework', 'CoreFoundation'])
		],
	cmdclass = {'build_ext': build}
	)
