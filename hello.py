from flask import Flask, session, redirect, url_for, escape, request
import twilio.twiml
import pxssh
import json
import threading


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
            return 'SSH session failed on login.'
        else:
            return 'SSH session login successful'

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

app = Flask(__name__)
blah = {}
@app.route('/', methods=['GET', 'POST'])
def index():
    phonenumber = request.values.get('From', None)
    if not blah.has_key(phonenumber):
        body = request.values.get('Body', None)
        action = json.loads(body)
# TODO: validate inputs
        host = action['host']
        username = action['username']
        password = action['password'] #long live plain text passwords
        session['connection'] = Sms2Ssh(host,username,password)
        session['connection'].login()
        blah[phonenumber] = session  
        return "Session value set."
    else:
        message = request.values.get('Body', None)
        #TODO: logout LENE + MANCARE
        blah[phonenumber]['connection'].sendMessage(message)


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
if __name__ == '__main__':
    app.run(debug=True)
