from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QCursor
app = QtWidgets.QApplication([])
import math
from math import *

WIDTH = 50.0 # percent

#constants
Rearth = 6.4e6
Mearth = 6.0e24
Mmoon = 7.3e22
Rmoon = 1.7e6
G = 6.67e-11
c = 3e8
Melectron = 9.11e-31
Qelectron = -1.6e-19
Mneutron = 1.675e-27
Mproton = 1.673e-27
h = 6.63e-19
E0 = 8.85e-12
U0 = 4*pi*10**-7
Ke=1/(4*pi*E0)

STYLE = """
QWidget, QLineEdit, QLabel {
    background-color: #273238;
    color: #c1c1c1;
    font-size: 15px;
    font-family: mono;
}

QWidget {
    border-color: #c1c1c1;
    border-width: 1px;
    border-style: solid;
}

QLineEdit {
    border: none;
    border-color: #1e2529;
    border-width: 1px;
    border-bottom-style: dashed;
    outline: none;
    margin-bottom: 0px;
    padding: 0px;
}

QLabel {
    margin-top: 0px;
    padding: 0px;
    border: none;
}
"""

class WrapLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(WrapLabel, self).__init__(*args, **kwargs)

        self.textalignment = Qt.AlignLeft | Qt.TextWrapAnywhere
        self.isTextLabel = True
        self.align = None

    def paintEvent(self, event):

        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)

        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

        self.style().drawItemText(painter, self.rect(),
                                  self.textalignment, self.palette(), True, self.text())

class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central = QtWidgets.QWidget(self)

        self.layout = QtWidgets.QVBoxLayout(self.central)
        self.input_line = QtWidgets.QLineEdit(self.central)
        self.body_text = WrapLabel(self.central)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.body_text)

        self.input_line.textChanged[str].connect(self.onKeyPress)
        self.central.setLayout(self.layout)

        self.setStyleSheet(STYLE)
        self.setCentralWidget(self.central)
        
        cursor_pos = QCursor.pos()
        screen = QtWidgets.QApplication.screenAt(cursor_pos)
        size = screen.size()
        geom = screen.geometry()
        sw, sh = size.width(), size.height()

        winwidth = int(sw / 100 * WIDTH)
        winheight = self.layout.sizeHint().height() + 2
        self.winwidth = winwidth
        self.winheight = winheight
        self.setGeometry(int(sw / 2 - winwidth / 2) + geom.x(),
                         int(sh / 2 - winheight / 2) + geom.y(),
                         winwidth, winheight)
        self.setWindowFlag(Qt.Popup)
        self.input_line.setFocus()
        self.show()

    def closeEvent(self, event):
        QCoreApplication.quit()

    def onKeyPress(self, text):
        try:
            smts = text.split(";")
            exec("\n".join([smt.strip() for smt in smts[:-1]]))
            ret = str(eval(smts[-1]))
        except Exception as e:
            ret = str(e)

        self.body_text.setText(ret)

        font_metrics = QtGui.QFontMetrics(self.body_text.font())
        text_size = font_metrics.size(0, "a")
        self.setFixedSize(self.winwidth, max(self.winheight, int((len(ret) * text_size.width()) // self.winwidth * text_size.height() + self.layout.sizeHint().height())))

w = MainWin()
app.exec_()
