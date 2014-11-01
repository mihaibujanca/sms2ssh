from flask import Flask, request, redirect
import twilio.twiml
import pxssh
import json


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

    __isLoggedIn = 0

    def isLoggedIn(self):
        return self.__isLoggedIn

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


class YourClass:

    def __init__(self):
        self.numbers = {}

    def newConnection(
        self,
        number,
        host,
        username,
        password,
        ):

        self.numbers[number] = Sms2Ssh(host, username, password)
        return self.numbers[number].login()

    def logout(self, number):
        self.numbers[number].logout()
        del self.numbers[number]

    def sendMessage(self, number, message):
        if self.numbers[number].isLoggedIn:
            return self.numbers[number].sendMessage(message)


newcl = YourClass()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_monkey():
    message = ''
    number = request.values.get('From', None)
    body = request.values.get('Body', None)
    action = json.loads(body)
    if not number in newcl.numbers.keys():
        message = newcl.newConnection(number, action['host'],
                action['username'], action['password'])
        message = newcl.sendMessage(number, "date")
    else:
        if action['command'] == 'logout':
            newcl.logout(number)
        else:
            message = newcl.sendMessage(number, action['command'])
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)
if __name__ == '__main__':
    app.run(debug=True)

