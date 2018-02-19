from PyQt4 import QtCore
from PyQt4 import QtGui
from os.path import join
from random import randint
import sqlite3 as lite
import sys
import time


class DBLite(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.con = None
        self.daemon = True

    def run(self):
        try:
            self.canProccess = True
            self.con = lite.connect(join('database', 'database.db'))
            self.cur = self.con.cursor()

            while self.canProccess:
                #secondsToSleep = randint(300, 420)
                secondsToSleep = randint(100, 400)
                time.sleep(secondsToSleep)
                data = self.select()
                self.emit(QtCore.SIGNAL("showSentencePopup(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), data[0], data[1], data[2])

        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if self.con:
                self.con.close()

    def select(self):
        #self.cur.execute('SELECT * FROM sentences where id = 16 ORDER BY RANDOM() LIMIT 1;')
        self.cur.execute('SELECT * FROM sentences WHERE learned = 0 ORDER BY RANDOM() LIMIT 1;')
        return self.cur.fetchone()
