from PyQt4 import QtGui


class Tray(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.window = parent
        self.setIcon(QtGui.QIcon("assets/images/city.png"))
        self.iconMenu = QtGui.QMenu(parent)
        self.setContextMenu(self.iconMenu)

        quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)
        self.iconMenu.addAction(quitAction)
        self.show()