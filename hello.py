from flask import Flask, session, redirect, url_for, escape, request
import twilio.twiml
import pxssh
import json
import threading
from threading import Thread
from Queue import Queue


class Sms2Ssh:

    def __init__(
        self,
        host,
        username,
        password,
        ):

        self.host = host
        self.username = username
        self.password = password
        self.connection = pxssh.pxssh()
        self.__isLoggedIn = 1

    def login(self):
        if not self.connection.login(self.host, self.username,
                self.password):
            return False
        else:
            return True

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

def run(queue, username, host, password):
    s = Sms2Ssh("kilburn.cs.man.ac.uk", "mbax4hb2", "Mike_UK_2014")
    if s.login() is True:
        print "You have successfullyyy logggged inn"
        while(1):
            message = queue.get()
            if message == 'logout':
                return "You have been logged out"
            if message is not None:
                response = s.sendMessage(message)
                print response
                resp = twilio.twiml.Response()
                resp.message(response)
                return str(resp)
                return "wth"
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
        username = action['username']
        password = action['password'] #long live plain text passwords
        print host
        print username
        print password
        #Create queue;
        queues[phonenumber] = Queue()
        # Create thread;
        threads[phonenumber] = Thread(target=run, args= (queues[phonenumber], username, host, password))
        #Login the user
        threads[phonenumber].start()
        return "Hello, Customer"
    else:
        message = request.values.get('Body', None)    
        queues[phonenumber].put(message)
        return "Thank you, customer"

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(debug=True)
