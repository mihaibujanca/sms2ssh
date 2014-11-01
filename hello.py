from flask import Flask, session, redirect, url_for, escape, request
import twilio.twiml
import pxssh
import json
import threading
import Queue


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
    s = Sms2Ssh(username, host, password)
    if s.login() is True:
        while(1):
            message = queue.get()
            if message == 'logout':
                return False
            if message is not None:
                s.sendMessage(message)
    else:
        return 'Could not connect!'                




app = Flask(__name__)

threads{}
queues{}
@app.route('/', methods=['GET', 'POST'])
def index():
    phonenumber = request.values.get('From', None)
    if not threads[phonenumber]
        #Create queue;
        queues[phonenumber] = Queue()
        # Create thread;
        threads[phonenumber] = Thread(target=run, args= (queue[phonenumber], username, host, password))
        
        #Get details of phonenumber
        body = request.values.get('Body', None)
        action = json.loads(body)
        # TODO: validate inputs
        host = action['host']
        username = action['username']
        password = action['password'] #long live plain text passwords
        #Login the user
        threads[phonenumber].start()
    else:
        message = request.values.get('Body', None)    
        queues[phonenumber].put(message)


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(debug=True)
