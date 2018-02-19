import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from components.Qt.SentencePopup import SentencePopup
from components.Tray import Tray
from components.helpers.DBLite import DBLite

def main():
    app = QApplication(sys.argv)
    resolution = QDesktopWidget().screenGeometry()
    mila = App()
    #mila.resize(resolution.width() - 20, 300)
    #mila.move(0, 0)
    #mila.setWindowTitle('Milana')
    mila.resize(0, 0)
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


        self.db = DBLite()
        self.db.start()

        self.connect(self.db, SIGNAL("showSentencePopup(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), self.showSentencePopup)

    def showSentencePopup(self, id, sentence, translate):
        try:
            self.popup.close()
        except AttributeError:
            pass

        self.popup = SentencePopup(id=id, sentence=sentence, translate=translate)

    def closeEvent(self, event):
        self.db.canProccess = False

    def close(self):
        QWidget.close(self)

if __name__ == "__main__":
    main()