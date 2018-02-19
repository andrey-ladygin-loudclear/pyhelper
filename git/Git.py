import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from components.Qt.SentencePopup import SentencePopup
from components.Resources import Resources
from components.Tray import Tray
from components.Command import Command
from components.Qt.CLineEdit import CLineEdit
from components.helpers.DBLite import DBLite

#import components.helpers.Lingualeo.export

def main():
    app = QApplication(sys.argv)
    resolution = QDesktopWidget().screenGeometry()
    mila = App()
    mila.resize(resolution.width() - 20, 300)
    mila.move(0, 0)
    mila.setWindowTitle('Milana')
    mila.show()
    trayIcon = Tray(mila)
    trayIcon.show()
    sys.exit(app.exec_())


####################################################################
class App(QWidget):
    lastCommand = ''

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowIcon(QIcon("assets/images/icon.png"))

        # create objects
        self.TextPanel = QLabel("\nHi! Have a nice day!")

        self.TextPanel.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.TextPanel.setContentsMargins(15, 10, 10, 10)
        self.TextPanel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.CLineEdit = CLineEdit()

        self.setObjectName("Window")
        self.CLineEdit.setObjectName("inputCommand")
        self.TextPanel.setObjectName("commandBox")
        self.setStyleSheet(Resources.readStyleSheet('window.pss'))

        rightPanel = QGridLayout()
        buttonGetConf = QPushButton("Get Conf")
        buttonPushConf = QPushButton("Push Conf")

        buttonGetConfFromFolder = QPushButton("Copy Conf from `conf`")
        buttonCopyConfToFolder = QPushButton("Copy Conf` to `conf`")

        buttonCopyPemFromFolder = QPushButton("Copy pems from folder")
        buttonGetPemsFromDrive = QPushButton("Get pems from drive")
        buttonPushPemsToDrive = QPushButton("Push pems to drive")


        rightPanel.addWidget(buttonGetConf)
        rightPanel.addWidget(buttonPushConf)
        rightPanel.addWidget(buttonGetConfFromFolder)
        rightPanel.addWidget(buttonCopyConfToFolder)
        rightPanel.addWidget(buttonCopyPemFromFolder)
        rightPanel.addWidget(buttonGetPemsFromDrive)
        rightPanel.addWidget(buttonPushPemsToDrive)

        # layout
        layout = QGridLayout()
        self.TextPanel.setFixedHeight(250)

        layout.addWidget(self.TextPanel, 0, 0, 1, 1)
        layout.addWidget(self.CLineEdit, 1, 0)
        layout.addLayout(rightPanel, 0, 1)

        self.setLayout(layout)
        self.command = Command()

        self.db = DBLite()
        self.db.start()

        # connections
        self.connect(self.CLineEdit, SIGNAL("enterPressed"), self.inputCommandExecute)
        self.connect(self.CLineEdit, SIGNAL("ctrlSpacePressed"), self.deactivate)
        self.connect(self.TextPanel, SIGNAL("linkActivated(QString)"), self.OpenURL)
        self.connect(self.command, SIGNAL("updateCommandTextBox(PyQt_PyObject, PyQt_PyObject)"), self.updateCommandTextBox)
        self.connect(self.db, SIGNAL("showSentencePopup(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.showSentencePopup)

        #self.connect(buttonGetConf, SIGNAL("clicked()"), lambda: self.commandExecute("get conf -update"))
        #self.connect(buttonPushConf, SIGNAL("clicked()"), lambda: self.commandExecute("push conf -update"))
        #self.connect(buttonGetConfFromFolder, SIGNAL("clicked()"), lambda: self.commandExecute("copy conf from"))
        #self.connect(buttonCopyConfToFolder, SIGNAL("clicked()"), lambda: self.commandExecute("copy conf to"))
        #self.connect(buttonCopyPemFromFolder, SIGNAL("clicked()"), lambda: self.commandExecute("copy pems"))
        #self.connect(buttonGetPemsFromDrive, SIGNAL("clicked()"), lambda: self.commandExecute("get pems -update"))
        #self.connect(buttonPushPemsToDrive, SIGNAL("clicked()"), lambda: self.commandExecute("push pems -update"))

    def updateCommandTextBox(self, message, delimiter='<br>'):
        self.TextPanel.setText('<qt>' + self.TextPanel.text() + delimiter + message + '</qt>')

    def showSentencePopup(self, id, sentence, translate):
        self.popup = SentencePopup(id=id, sentence=sentence, translate=translate)

    def OpenURL(self, URL):
        print URL

    def activate(self):
        self.show()
        self.CLineEdit.focusWidget()

    def deactivate(self):
        self.hide()

    def inputCommandExecute(self):
        command = str(self.CLineEdit.text())
        self.lastCommand = command
        self.printMessage(command)
        self.CLineEdit.setText('')
        self.commandExecute(command)

    def commandExecute(self, command):
        if not command: return ''
        res = self.command.execute(command)
        if res: self.printMessage(res)

    def printMessage(self, message):
        self.updateCommandTextBox(message, '<br>')

    def closeEvent(self, event):
        self.db.canProccess = False

if __name__ == "__main__":
    main()