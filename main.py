#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QCursor
app = QtWidgets.QApplication([])
import math
from math import *
import random
# import numpy as np
# import time
# import json
# import os
# import sys
import time
import json
import pyperclip

WIDTH = 50.0 # percent of the screen

#constants
Rearth = 6.4e6
Mearth = 6.0e24
Mmoon = 7.3e22
Rmoon = 1.7e6
G = 6.67e-11
c = 299_792_458.0
Melectron = 9.11e-31
Qelectron = -1.6e-19
Mneutron = 1.675e-27
Mproton = 1.673e-27
h = 6.63e-19
ħ = h/(2*pi)
E0 = 8.85e-12
U0 = 4*pi*10**-7
Ke=1/(4*pi*E0)

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1],
            a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])

dot = lambda a, b: sum([e * f for e, f in zip(a, b)]) 
mag = lambda v: sqrt(v[0]**2+v[1]**2+v[2]**2)
norm = lambda v: (v[0]/mag(v), v[1]/mag(v), v[2]/mag(v))

STYLE = """
QWidget, QLineEdit, QPlainTextEdit QLabel {
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

QLineEdit, QPlainTextEdit {
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
        self.input_line = QtWidgets.QPlainTextEdit(self.central)
        self.body_text = WrapLabel(self.central)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.body_text)

        self.input_line.textChanged.connect(self.onTextChange)
        self.resize_input()
        self.input_line.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.input_line.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        def keyPressEvent(event):
            if event.key() == Qt.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                # copy
                if self.input_line.textCursor().hasSelection():
                    # if selected, copy selected text
                    text = self.input_line.textCursor().selectedText().replace('\u2029', '\n')
                else:
                    # if not selected, copy the output
                    text, _ = self.run_code()
                pyperclip.copy(text)
            elif event.key() == Qt.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                # save
                name, extension = QtWidgets.QFileDialog.getSaveFileName(filter="Python scripts (*.py)")
                if not name.endswith(".py"):
                    name += ".py"
                with open(name, "w") as f:
                    f.write(self.input_line.toPlainText())
            else:
                QtWidgets.QPlainTextEdit.keyPressEvent(self.input_line, event)
        
        self.input_line.keyPressEvent = keyPressEvent
        self.central.setLayout(self.layout)

        self.setStyleSheet(STYLE)
        self.setCentralWidget(self.central)

        with open("/home/james/.config/popish/history.json", "r") as f:
            self.history = json.loads(f.read())["history"]
        
        # Calculating size and position for the window initially
        cursor_pos = QCursor.pos()
        screen = QtWidgets.QApplication.screenAt(cursor_pos)
        size = screen.size()
        geom = screen.geometry()
        sw, sh = size.width(), size.height()
        self.winwidth = int(sw / 100 * WIDTH)
        self.winheight = self.layout.sizeHint().height() + 2
        self.setGeometry(int(sw / 2 - self.winwidth / 2) + geom.x(),
                         int(sh / 2 - self.winheight / 2) + geom.y(),
                         self.winwidth, self.winheight)
        self.setWindowFlag(Qt.WindowType.Tool) 

        self.input_line.setFocus()
        self.show()

    def add_to_history(self, expression, result):
        val = (expression.strip(), result, time.time())
        for item in self.history:
            if item[0] == val[0] and item[1] == val[1]:
                return

        self.history.append(val)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.closeEvent(None)
        super().keyPressEvent(event)

    def closeEvent(self, event):
        with open("/home/james/.config/popish/history.json", "w") as f:
            f.write(json.dumps({"history": self.history}))
        QCoreApplication.quit()

    def resize_input(self):
        rows = len(self.input_line.toPlainText().split("\n"))
        font_metrics = QtGui.QFontMetrics(self.input_line.font())
        doc = self.input_line.document()
        margins = self.input_line.contentsMargins()
        row_height  = (font_metrics.lineSpacing() + 2) * rows + (doc.documentMargin() + self.input_line.frameWidth()) * 2 + margins.top() + margins.bottom()
        self.input_line.setFixedHeight(round(row_height))

    def run_code(self):
        text = self.input_line.toPlainText()
        try:
            smts = text.split("\n")
            # exec("\n".join([smt.strip() for smt in smts[:-1]]))
            globs = globals().copy()
            locs = locals().copy()
            exec("\n".join(smts[:-1]), globs, locs)
            # weird hack to make list comprehensions work: make locals global
            globs = {**locs, **globs}
            ret = str(eval(smts[-1], globs))
            was_error = False
        except Exception as e:
            ret = str(e)
            was_error = True
        return ret, was_error

    def onTextChange(self):
        ret, was_error = self.run_code()
        self.body_text.setText(ret)

        if not was_error:
            self.add_to_history(self.input_line.toPlainText(), ret)
        
        self.resize_input()
        font_metrics = QtGui.QFontMetrics(self.body_text.font())
        text_size = font_metrics.size(0, "a")
        self.setFixedSize(self.winwidth, max(self.winheight, int((len(ret) * text_size.width()) // self.winwidth * text_size.height() + self.layout.sizeHint().height())))

if __name__ == "__main__":
    w = MainWin()
    app.exec_()
