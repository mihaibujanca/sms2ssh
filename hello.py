from flask import Flask, session, redirect, url_for, escape, request
from twilio.rest import TwilioRestClient
import twilio.twiml
import pxssh
import json
import threading
from threading import Thread
from Queue import Queue

import base64
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) ) 

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))


class Sms2Ssh:

    def __init__(
        self,
        host,
        port,
        username,
        password,
        ):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = pxssh.pxssh()
        
        self.__isLoggedIn = 1

    def login(self):
        try:
        
            self.connection.force_password = True
        
            #self.connection.prompt()
            if not self.connection.login(self.host, self.username, self.password, 'ansi', '[#$]', 100, self.port, False):
                print "you:"
                return False
            else:
                return True
        except pxssh.ExceptionPxssh, e:
            print str(e)        

    # logs out and destroys the current object

    def logout(self):
        self.connection.logout()

    # self.__del__()

    def sendMessage(self, command):
        try:
            self.connection.sendline(command)
            self.connection.prompt()
            return self.connection.before
        except pxssh.ExceptionPxssh, e:
            print str(e)

    def __del__(self):
        pass

def run(queue, host, port, username, password, phonenumber):
    print "\n"
    print host
    print username  
    print password
    s = Sms2Ssh(host, port, username, password)
    if s.login() is True:
        print "You have successfully loged in!"
        while(1):
            message = queue.get()
            if message == 'logout':
                return "You have been logged out!"
            if message is not None:
                response = s.sendMessage(message)
                # Your Account Sid and Auth Token from twilio.com/user/account
                account_sid = "AC79b0bec1d39cd65eb5a47dc3d43bb988"
                auth_token  = "7f7d1edeb5f360e19d6a9d0aae01a3c3"
                client = TwilioRestClient(account_sid, auth_token)
                client.messages.create(body=response,
                                        to=phonenumber,    # Replace with your phone number
                                        from_="+441133202312")
    else:
        return 'Could not connect!'                


app = Flask(__name__)

threads = {}
queues = {}
@app.route('/', methods=['GET', 'POST'])
def index():
    phonenumber = request.values.get('From', None)
    if not phonenumber in threads.keys():
        #Get details of phonenumber
        body = request.values.get('Body', None)
        action = json.loads(body)
        # TODO: validate inputs
        host = action['host']
        port = action['port']
        username = action['username']
        password_encrypt = action['password']
        encr = action['encr']
        if encr == 'true':
            thekey = host
            cypher = AESCipher(thekey)
            password = cypher.decrypt(password_encrypt)
        else:
            password = password_encrypt    
        #Create queue;
        queues[phonenumber] = Queue()
        # Create thread;
        threads[phonenumber] = Thread(target=run, args= (queues[phonenumber], host, port, username, password, phonenumber))
        #Login the user
        threads[phonenumber].start()
        return "Hello, Customer"
    else:
        message = request.values.get('Body', None)
        print message  
        queues[phonenumber].put(message.format())
        return "Thank you, customer"

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(debug=True)
