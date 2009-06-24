import Keychain

print Keychain.AddInternetPassword(serverName = 'example.org', accountName = 'test', password = 'test_password')

#serverName = '', securityDomain = '', accountName = '', path = '', port = 0, protocol = kSecProtocolTypeHTTP, authenticationType = 0x64666C74, password = ''):


print Keychain.FindInternetPassword(serverName = 'example.org', accountName = 'test')
