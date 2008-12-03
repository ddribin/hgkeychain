from distutils.core import setup
from distutils.extension import Extension

try:
	from Cython.Distutils import build_ext
except:
	from Pyrex.Distutils import build_ext


setup(
	name = "Keychain",
	version = '0.1',
	author = 'Jonathan Wight',
	author_email = 'jwight@mac.com',
	url = 'http://toxicsoftware.com',
	description = 'Mac OS X Keychain Module',
	long_description = '''Trivial module to interact with the Mac OS X keychain. Pyobjc STILL can't access the Security framework without issues.''',
	license = 'BSD',
	requires = [],
#	packages = ['Keychain'],
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
	cmdclass = {'build_ext': build_ext}
	)
