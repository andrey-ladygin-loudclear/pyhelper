from PyQt4 import QtCore
import multiprocessing
from components.Resources import Resources
from components.helpers.Cmd import Cmd
from components.helpers.Disk import Disk


class Command(QtCore.QObject):
    instance = None

    def __init__(self, *args):
        QtCore.QObject.__init__(self, *args)
        self.Disk = Disk(self)
        self.Cmd = Cmd(self)
        super(QtCore.QObject, self).__init__()

    def execute(self, command):
        res = self.static(command)
        return res

    def static(self, command):
        if 'https://github.com/' in command:
            conf = Resources.Settings('github')
            command = command.replace('https://github.com/', 'https://'+conf['login']+':'+conf['pass']+'@github.com/')
            self.copy(command)
            return command

        if 'https://bitbucket.org' in command:
            conf = Resources.Settings('bitbucket')
            command = command.replace('https://bitbucket.org', 'https://'+conf['login']+':'+conf['pass']+'@bitbucket.org')
            self.copy(command)
            return command

        if 'create' in command:
            args = ParseCommandArguments(command).parse()
            try:
                Create(args)
            except Exception, e:
                return str(e)

        return None

    def emitMessage(self, command, delimiter="<br>"):
        self.emit(QtCore.SIGNAL("updateCommandTextBox(PyQt_PyObject, PyQt_PyObject)"), command, delimiter)

    def copy(self, message):
        pass
        #r = Tk()
        #r.withdraw()
        #r.clipboard_clear()
        #r.clipboard_append(message)
        #r.destroy()
