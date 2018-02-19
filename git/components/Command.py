from PyQt4 import QtCore
import multiprocessing
from components.Resources import Resources
from components.helpers.Cmd import Cmd
from components.helpers.CreateHelper.Create import Create
from components.helpers.GoogleDriveService import GoogleDriveService
from components.helpers.Disk import Disk
from components.helpers.ParseCommandArguments import ParseCommandArguments


class Command(QtCore.QObject):
    instance = None

    def __init__(self, *args):
        QtCore.QObject.__init__(self, *args)
        self.GoogleDriveService = GoogleDriveService(self)
        self.Disk = Disk(self)
        self.Cmd = Cmd(self)
        super(QtCore.QObject, self).__init__()

    def execute(self, command):
        res = self.static(command)

        if not res:
            pass
            #self.runSubProccessCommand(command)
            #service = multiprocessing.Process(name=command, target=self.runSubProccessCommand, args=(command,))
            #service.daemon = True
            #service.start()

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

    def runSubProccessCommand(self, command):
        name = multiprocessing.current_process().name
        commandComponents = command.split(' ')
        #name = command

        if 'push' in commandComponents and 'pems' in commandComponents: return self.GoogleDriveService.pushPems(commandComponents)
        if 'get' in commandComponents and 'pems' in commandComponents: return self.GoogleDriveService.getPems(commandComponents)

        if 'copy' in commandComponents and 'pems' in commandComponents: return self.Disk.copyPems(commandComponents)

        if 'push' in commandComponents and 'conf' in commandComponents: return self.GoogleDriveService.pushConf(commandComponents)
        if 'get' in commandComponents and 'conf' in commandComponents: return self.GoogleDriveService.getConf(commandComponents)

        if 'copy' in commandComponents and 'from' in commandComponents and 'conf' in commandComponents: return self.Disk.copyConfFrom(commandComponents)
        if 'copy' in commandComponents and 'to' in commandComponents and 'conf' in commandComponents: return self.Disk.copyConfTo(commandComponents)

        if 'cmd' in commandComponents: return self.Cmd.new()

        self.emitMessage(command+': Undefined Command!')

    def emitMessage(self, command, delimiter="<br>"):
        self.emit(QtCore.SIGNAL("updateCommandTextBox(PyQt_PyObject, PyQt_PyObject)"), command, delimiter)

    def copy(self, message):
        pass
        #r = Tk()
        #r.withdraw()
        #r.clipboard_clear()
        #r.clipboard_append(message)
        #r.destroy()
