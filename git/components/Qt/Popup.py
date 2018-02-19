from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QDesktopWidget
from os.path import join
from components.Resources import Resources


class Popup(QtGui.QWidget):
    def __init__(self, title='Popup', message='', params={}, parent=None):
        QtGui.QWidget.__init__(self, parent)

        width = 300
        height = 200

        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry(resolution.width() - width, resolution.height() - height, width, height)

        pos_x = resolution.width() / 2 - width / 2
        pos_y = resolution.height() / 2 - height / 2
        self.move(pos_x, pos_y)

        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.setToolTip(title)
        self.setObjectName("toolTipWindow")
        self.setStyleSheet(Resources.read(join('assets', 'styles', 'tooltip.pss')))

        self.CComamnd = QtGui.QLabel(message)
        #self.CComamnd.setFixedHeight(50)
        self.CComamnd.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.CComamnd.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.CComamnd.setObjectName('command')

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.CComamnd)
        self.setLayout(layout)
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
        self.show()

    #def show(self, title='Tooltip', command='', res='This is a QWidget'):
    #    QtGui.QWidget.show(self)

    def close(self):
        QtGui.QWidget.close(self)
