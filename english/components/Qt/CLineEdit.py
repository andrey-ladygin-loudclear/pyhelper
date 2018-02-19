from PyQt4.QtCore import QEvent, Qt, SIGNAL
from PyQt4.QtGui import QLineEdit, QApplication


class CLineEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)

    def event(self, event):

        if (event.type()==QEvent.KeyPress):
            modifiers = QApplication.keyboardModifiers()

            if modifiers == Qt.ShiftModifier:
                pass#print('Shift+Click')
            elif modifiers == Qt.ControlModifier and event.key()==Qt.Key_Space:
                self.emit(SIGNAL("ctrlSpacePressed"))
                return True

            if event.key()==Qt.Key_Return:
                self.emit(SIGNAL("enterPressed"))
                return True

        return QLineEdit.event(self, event)