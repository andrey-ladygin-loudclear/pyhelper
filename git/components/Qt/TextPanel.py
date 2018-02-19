from PyQt4.QtGui import QLabel

class TextPanel(QLabel):
    def __init__(self, *args):
        QLabel.__init__(self, *args)