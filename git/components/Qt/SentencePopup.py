from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QDesktopWidget
from os.path import join
from components.Resources import Resources


class SentencePopup(QtGui.QWidget):
    def __init__(self, title='Try To Learn', id=0, sentence='', translate='', parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeom(500, 200)

        self.setWindowTitle(title + '#' + str(id))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        self.setToolTip(title)
        self.setObjectName("toolTipWindow")
        self.setStyleSheet(Resources.read(join('assets', 'styles', 'tooltip.pss')))

        self.setLeftPanel(sentence)
        self.setRightPanel(translate)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.leftText, 0, 0, 1, 1)
        layout.addWidget(self.rightText, 0, 1)
        self.setLayout(layout)
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))
        self.show()

        self.resizeAfterShow()

    def setLeftPanel(self, sentence):
        self.leftText = QtGui.QLabel(sentence)
        self.leftText.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.leftText.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        #self.leftText.setWordWrap(True)
        self.leftText.setObjectName('command')

    def setRightPanel(self, translate):
        self.rightText = QtGui.QLabel(translate)
        self.rightText.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.rightText.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        #self.rightText.setWordWrap(True)
        self.rightText.setObjectName('command')


    def setGeom(self, width, height):
        resolution = QDesktopWidget().screenGeometry()

        width = min(resolution.width(), width)
        height = min(resolution.height(), height)

        self.setGeometry(resolution.width() - width, resolution.height() - height, width, height)
        #self.resize(500, 500)

        pos_x = resolution.width() - width
        pos_y = 20
        self.move(pos_x, pos_y)

    def resizeAfterShow(self):
        resolution = QDesktopWidget().screenGeometry()
        LGeom = self.leftText.geometry()
        RGeom = self.rightText.geometry()

        MaxWidth = LGeom.width() + RGeom.width()
        MaxHeight = LGeom.height() + RGeom.height()

        width = min(resolution.width() - 300, MaxWidth)
        height = min(resolution.height() - 100, MaxHeight)

        self.setGeom(width, height)

        self.leftText.setWordWrap(True)
        self.rightText.setWordWrap(True)

        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)

        self.setMinimumSize(50, 50)
        self.setMaximumSize(resolution.width(), resolution.height())

    def close(self):
        QtGui.QWidget.close(self)
