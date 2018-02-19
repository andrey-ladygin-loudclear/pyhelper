import os
from components.helpers import GenerateShScripts
from PyQt4 import QtGui
from PyQt4 import QtCore
from functools import partial
from Resources import Resources
from components.Qt.Popup import Popup


class Tray(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.window = parent
        self.setIcon(QtGui.QIcon("assets/images/icon.png"))
        self.iconMenu = QtGui.QMenu(parent)
        self.setContextMenu(self.iconMenu)

        confs = Resources.getConfigs()

        #self.quitAction.setShortcut(QKeySequence(self.tr("Ctrl+Q")))

        for instance in confs:
            if confs[instance]['PARAMS']:
                name = confs[instance]['PARAMS']['name']
                itemMenu = QtGui.QMenu(self.iconMenu)
                itemMenu.setTitle(name)
                self.iconMenu.addMenu(itemMenu)

                detailsItem = itemMenu.addAction("Show Details")
                self.connect(detailsItem, QtCore.SIGNAL('triggered()'), partial(self.instanceDetails, confs[instance]))

                for env in confs[instance]:
                    if env != 'PARAMS':
                        conf = confs[instance][env]

                        subItemMenu = itemMenu.addAction("Connect " + env)
                        file = GenerateShScripts.generateSh(conf)
                        #self.connect(subItemMenu, QtCore.SIGNAL('triggered()'), partial(self.instanceAction, conf))
                        self.connect(subItemMenu, QtCore.SIGNAL('triggered()'), partial(self.runShFile, file))

        quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.iconMenu.addAction(quitAction)
        self.show()

    def instanceAction(self, opt):
        print("instanceAction")
        print(opt)

    def runShFile(self, file):
        os.system("gnome-terminal --command '" + file + "'")

    def instanceDetails(self, opts):
        title = opts['PARAMS']['name'] + ' Details'
        message = ''
        for env in opts:
            message += env + ': \n'
            for row in opts[env]:
                message += "%s:     %s\n" % (row, opts[env][row])

            if 'host' in opts[env]:
                connect = 'ssh '
                if 'pem' in opts[env]:
                    connect += '-i ~/pems/' + opts[env]['pem'] + ' '

                connect += opts[env]['host']

                if 'port' in opts[env]:
                    connect += ' -p ' + opts[env]['port'] + ' '

                message += "%s:     %s\n" % ('Connect', connect)

            message += '\n'

        self.popup = Popup(title, message)