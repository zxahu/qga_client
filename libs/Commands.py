__all__ = ['Entry', 'OpenFile']
import base64

class BaseCommand:

    input = ''
    result= ''
    handler = None
    prompt = ""

    finish = False

    def __init__(self, handler):
        self.handler = handler

    def do(self):
        userInput = self.input()
        self.execute(userInput)

    def input(self):
        return raw_input(self.prompt)


    def execute(self, userInput):
        if userInput in ('exit', 'quit'):
            return self.close()

    def query(self, command):
        self.handler.send(command)
        return self.recieve()

    def close(self):
        print 'Exit'

    def recieve(self):
        return self.handler.recieve()

class OpenFile(BaseCommand):
    prompt = "File>"
    fileHandleId = None
    content = ''

    def execute(self, userInput, mode='r'):
        if userInput in ('exit', 'quit'):
            return self.close()

        userInput = userInput.split(" ")
        filename  = userInput[0]

        if len(userInput) > 2 and userInput[1] in ('w', 'r', 'a'):
            mode = userInput[1]

        query = { 'execute' : 'guest-file-open', 'arguments' : {'path': filename, 'mode' : mode} }
        result = self.query(query)

        if 'return' in result.keys() and result['return'] != 0:
            self.fileHandleId = result['return']
            print self.openFile()

        self.do()

    def openFile(self, init=True):
        data = ''
        query  = {'execute' : 'guest-file-read', 'arguments' : {'handle': self.fileHandleId, 'count' : 1<<10}}
        while True:
            result = self.query(query)

            data  += result['return']['buf-b64']
            if result['return']['eof'] :
                break

        return base64.decodestring(data)

    def closeFile(self):
        if self.fileHandleId is not None:
            query  = {'execute' : 'guest-file-close', 'arguments' : {'handle': self.fileHandleId}}
            self.fileHandleId = None
            self.query(query)

    def close(self):
        self.closeFile()

class Entry(BaseCommand):
    prompt = "+>"

    commandMap = {
        'guest-file-open' : OpenFile,
    }

    def execute(self, userInput):
        if userInput in ('exit', 'quit'):
            return self.close()

        if userInput in self.commandMap.keys():
            object = self.commandMap[userInput](self.handler)
            object.do()
        else:
            command = {'execute': userInput}
            result =  self.query(command)
            try: print result['return']
            except: print "Error"

        self.do()
