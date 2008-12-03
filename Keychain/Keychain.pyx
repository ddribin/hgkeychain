def FourCharCode(s):
	return ord(s[0]) << 24 | ord(s[1]) << 16 | ord(s[2]) << 8 | ord(s[3])

def LengthOrZero(x):
	if not x:
		return 0
	else:
		return len(x)

####################################################################################################

kSecProtocolTypeFTP = FourCharCode('ftp ')
kSecProtocolTypeFTPAccount = FourCharCode('ftpa')
kSecProtocolTypeHTTP = FourCharCode('http')
kSecProtocolTypeIRC	 = FourCharCode('irc ')
kSecProtocolTypeNNTP = FourCharCode('nntp')
kSecProtocolTypePOP3 = FourCharCode('pop3')
kSecProtocolTypeSMTP = FourCharCode('smtp')
kSecProtocolTypeSOCKS = FourCharCode('sox ')
kSecProtocolTypeIMAP = FourCharCode('imap')
kSecProtocolTypeLDAP = FourCharCode('ldap')
kSecProtocolTypeAppleTalk = FourCharCode('atlk')
kSecProtocolTypeAFP	 = FourCharCode('afp ')
kSecProtocolTypeTelnet = FourCharCode('teln')
kSecProtocolTypeSSH	 = FourCharCode('ssh ')
kSecProtocolTypeFTPS = FourCharCode('ftps')
kSecProtocolTypeHTTPS = FourCharCode('htps')
kSecProtocolTypeHTTPProxy = FourCharCode('htpx')
kSecProtocolTypeHTTPSProx = FourCharCode('htsx')
kSecProtocolTypeFTPProxy  = FourCharCode('ftpx')
kSecProtocolTypeSMB	 = FourCharCode('smb ')
kSecProtocolTypeRTSP = FourCharCode('rtsp')
kSecProtocolTypeRTSPProxy = FourCharCode('rtsx')
kSecProtocolTypeDAAP = FourCharCode('daap')
kSecProtocolTypeEPPC = FourCharCode('eppc')
kSecProtocolTypeIPP	 = FourCharCode('ipp ')
kSecProtocolTypeNNTPS = FourCharCode('ntps')
kSecProtocolTypeLDAPS = FourCharCode('ldps')
kSecProtocolTypeTelnetS = FourCharCode('tels')
kSecProtocolTypeIMAPS = FourCharCode('imps')
kSecProtocolTypeIRCS = FourCharCode('ircs')
kSecProtocolTypePOP3S = FourCharCode('pops')

####################################################################################################

cdef extern from "Python.h":
	object PyString_FromStringAndSize(char *s, Py_ssize_t len)

cdef extern from "CoreFoundation/CoreFoundation.h":
	ctypedef void * CFTypeRef
	void CFRelease(CFTypeRef cf)

cdef extern from "Security/Security.h":
	ctypedef int OSStatus
	ctypedef unsigned short UInt16
	ctypedef unsigned int UInt32
	ctypedef int SecProtocolType
	ctypedef int SecAuthenticationType
	ctypedef void * SecKeychainRef
	ctypedef void * SecKeychainItemRef

	OSStatus SecKeychainFindInternetPassword(CFTypeRef keychainOrArray, UInt32 serverNameLength, char *serverName, UInt32 securityDomainLength, char *securityDomain, UInt32 accountNameLength, char *accountName, UInt32 pathLength, char *path, UInt16 port, SecProtocolType protocol, SecAuthenticationType authenticationType, UInt32 *passwordLength, void **passwordData, SecKeychainItemRef *itemRef)

	OSStatus SecKeychainAddInternetPassword(SecKeychainRef keychain, UInt32 serverNameLength, char *serverName, UInt32 securityDomainLength, char *securityDomain, UInt32 accountNameLength, char *accountName, UInt32 pathLength, char *path, UInt16 port, SecProtocolType protocol, SecAuthenticationType authenticationType, UInt32 passwordLength, void *passwordData, SecKeychainItemRef *itemRef)

	OSStatus SecKeychainItemCopyContent(SecKeychainItemRef itemRef, void *itemClass, void *attrList, UInt32 *length, void **outData)

#	OSStatus SecKeychainItemFreeContent(SecKeychainAttributeList *attrList, void *data)
	OSStatus SecKeychainItemFreeContent(void *attrList, void *data)

	OSStatus SecKeychainItemModifyContent(SecKeychainItemRef itemRef, void *attrList, UInt32 length, void *data)

	OSStatus SecKeychainItemDelete(SecKeychainItemRef itemRef)

####################################################################################################

cdef class KeychainItem:
	cdef SecKeychainItemRef _k

	def __init__(self):
		self._k = NULL

	def __del__(self):
		if self._k != NULL:
			CFRelease(self._k)
			self._k = NULL

	property password:
		"A doc string can go here."
		def __get__(self): 
			cdef UInt32 thePasswordLength
			cdef void *thePasswordPtr
			thetStatus = SecKeychainItemCopyContent(self._k, NULL, NULL, &thePasswordLength, &thePasswordPtr)
			thePassword = PyString_FromStringAndSize(<char *>thePasswordPtr, thePasswordLength)
			theStatus = SecKeychainItemFreeContent(NULL, thePasswordPtr)
			return thePassword
		def __set__(self, password):
			cdef char *thePasswordPtr
			thePasswordPtr = password
			theStatus = SecKeychainItemModifyContent(self._k, NULL, len(password), thePasswordPtr)

####################################################################################################


####################################################################################################

def FindInternetPassword(serverName = '', securityDomain = '', accountName = '', path = '', port = 0, protocol = kSecProtocolTypeHTTP, authenticationType = 0x64666C74):
	cdef UInt32 thePasswordLength
	cdef void *thePasswordPtr
	cdef SecKeychainItemRef theKeychainItemRef
	cdef KeychainItem theKeychainItem

	theStatus = SecKeychainFindInternetPassword(NULL, LengthOrZero(serverName), serverName, LengthOrZero(securityDomain), securityDomain, LengthOrZero(accountName), accountName, LengthOrZero(path), path, port, protocol, authenticationType, &thePasswordLength, &thePasswordPtr, &theKeychainItemRef)
	if theStatus != 0:
		return (None, None)
	
	thePassword = PyString_FromStringAndSize(<char *>thePasswordPtr, thePasswordLength)
	theStatus = SecKeychainItemFreeContent(NULL, thePasswordPtr)

	theKeychainItem = KeychainItem()
	theKeychainItem._k = theKeychainItemRef

	return (thePassword, theKeychainItem)

####################################################################################################

def AddInternetPassword(serverName = '', securityDomain = '', accountName = '', path = '', port = 0, protocol = kSecProtocolTypeHTTP, authenticationType = 0x64666C74, password = ''):
	cdef char *thePasswordPtr
	thePasswordPtr = password
	
	theResult = SecKeychainAddInternetPassword(NULL, LengthOrZero(serverName), serverName, LengthOrZero(securityDomain), securityDomain, LengthOrZero(accountName), accountName, LengthOrZero(path), path, port, protocol, authenticationType, LengthOrZero(password), thePasswordPtr, NULL)
