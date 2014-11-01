import pxssh
class Sms2Ssh:
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
	self.password = password
	self.connection = pxssh.pxssh()
	self.__isLoggedIn = 1
    __isLoggedIn = 0
    def isLoggedIn(self):
	return self.__isLoggedIn
    def login(self):
        if not self.connection.login(self.host,self.username,self.password):
		print "SSH session failed on login."
	else:
		print "SSH session login successful"
    #logs out and destroys the current object
    def logout(self):
	self.connection.logout()
	#self.__del__()
    def sendMessage(self,command):
	try:
		self.connection.sendline(command)
		self.connection.prompt()
		print self.connection.before
	except pxssh.ExceptionPxssh, e:
	        print str(e)
    def __del__(self):
	pass
class YourClass:
    def __init__(self):
	self.numbers = {}
    def newConnection(self,number,host,username,password):
	self.numbers[number]=Sms2Ssh(host,username,password)
	self.numbers[number].login()
    def logout(self,number):
	self.numbers[number].logout()
	del self.numbers[number]
    def sendMessage(self,number,message):
	if self.numbers[number].isLoggedIn:
		return self.numbers[number].sendMessage(message)
newcl = YourClass()
newcl.newConnection("07467783960","kilburn.cs.man.ac.uk","mbax4hb2","Mike_UK_2014")
newcl.sendMessage("07467783960","ls -l")
newcl.newConnection("07467783961","kilburn.cs.man.ac.uk","mbax4cs5","kate_UK_2014")
newcl.sendMessage("07467783961","ls -l")
