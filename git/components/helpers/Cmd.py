import os
from subprocess import call


class Cmd:
    def __init__(self, commandObject):
        pass

    def new(self):
        #call(["ls", "-l"])
        #call(["ssh", "skyzone@skyzone.com.au"])
        #call("ssh skyzone@skyzone.com.au", shell = True)
        os.system('ssh skyzone@skyzone.com.au')