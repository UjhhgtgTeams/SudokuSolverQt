# This Python file uses the following encoding: utf-8
from datetime import datetime
import sys
import os
import threading
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from math import floor

sudoku = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
x = 0
y = 0
xP = 0
yP = 0
btEnd = False
stepTime = 0
possibilities = "123456789"
stopBasic = False
noSolution = False
solutedNumbers = 0


def cls():
    sys.system('cls' if os.name == 'nt' else 'clear')


def formatList():
    global sudoku
    for a in range(9):
        for b in range(9):
            sudoku[a][b] = int(sudoku[a][b])


def stepGrid(stepType):
    global xP, yP, stepTime, sudoku
    stepTime += 1
    if stepType == "n":
        if yP != 8:
            yP += 1
            if sudoku[xP][yP] > 0:
                stepGrid("n")
            else:
                sudoku[xP][yP] = 0
        else:
            if xP != 8:
                xP += 1
                yP = 0
                if sudoku[xP][yP] > 0:
                    stepGrid("n")
                else:
                    sudoku[xP][yP] = 0
            else:
                showRight()
    elif stepType == "b":
        if yP != 0:
            yP -= 1
            if sudoku[xP][yP] > 0:
                stepGrid("b")
            else:
                sudoku[xP][yP] = 0
        else:
            if xP != 0:
                xP -= 1
                yP = 8
                if sudoku[xP][yP] > 0:
                    stepGrid("b")
                else:
                    sudoku[xP][yP] = 0


def calcPos(xN, yN, sN=0, calcT=True):
    global possibilities, sudoku
    k = floor(xN / 3) * 3
    while k < floor(xN / 3) * 3 + 3:
        m = floor(yN / 3) * 3
        while m < floor(yN / 3) * 3 + 3:
            if calcT is True:
                possibilities = possibilities.replace(str(sudoku[k][m]), "")
            else:
                if abs(sN) == abs(sudoku[k][m]):
                    return False
            m += 1
        k += 1
    for i in range(9):
        for j in range(9):
            if calcT is True:
                possibilities = possibilities.replace(str(sudoku[xN][i]), "")
                possibilities = possibilities.replace(str(sudoku[j][yN]), "")
            else:
                if abs(sN) == abs(sudoku[xN][i]):
                    return False
                if abs(sN) == abs(sudoku[j][yN]):
                    return False


def showRight():
    global sudoku, stepTime, btEnd
    for fx in range(9):
        for fy in range(9):
            sudoku[fx][fy] = abs(sudoku[fx][fy])
    btEnd = True
    exit()


def backtrack():
    global sudoku, xP, yP
    if xP == 8 and yP == 8 and sudoku[xP][yP] > 0:
        showRight()
    if sudoku[xP][yP] == 0:
        for testNum in range(1, 10):
            testNum = 0 - testNum
            if calcPos(xP, yP, testNum, False) is False:
                continue
            sudoku[xP][yP] = testNum
            if xP == 8 and yP == 8:
                showRight()
            stepGrid("n")
            backtrack()
        stepGrid("b")
    else:
        stepGrid("n")
        backtrack()


def basic():
    global x, y, sudoku, possibilities, solutedNumbers, noSolution, stopBasic
    while stopBasic is False:
        for x in range(9):
            for y in range(9):
                if sudoku[x][y] == 0:
                    calcPos(x, y)
                    if len(possibilities) == 1:
                        sudoku[x][y] = int(possibilities)
                        solutedNumbers += 1
                possibilities = "123456789"
        if solutedNumbers == 0:
            noSolution = True
            pass
            break
        solutedNumbers = 0
        stopBasic = True
        for n in range(9):
            for p in range(9):
                if sudoku[n][p] == 0:
                    stopBasic = False


class SSGui(QWidget):
    def __init__(self):
        super(SSGui, self).__init__()
        ## Init layout
        # layout = QGridLayout()
        self.setWindowTitle(r"*** Sudoku Solver GUI ***   |   By: Ujhhgtg")
        self.setGeometry(0, 0, 800, 700)
        ## Buttons!!!
        # Run Button
        self.btnRun = QPushButton("RUN!!!", self)
        self.btnRun.setGeometry(310, 640, 170, 40)
        self.btnRun.setFont(QFont("Noto Sans", 14))
        self.btnRun.clicked.connect(self.runSolver)
        ## Tables!!!
        # Sudoku Table
        self.tblSudoku = QTableWidget(9, 9)
        self.tblSudoku.setGeometry(100, 20, 600, 600)
        self.tblSudoku.setFont(QFont("Noto Sans", 14, QFont.Bold))
        self.tblSudoku.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblSudoku.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblSudoku.setHorizontalHeaderLabels(["0", "1", "2", "3", "4", "5", "6", "7", "8"])
        self.tblSudoku.setVerticalHeaderLabels(["A", "B", "C", "D", "E", "F", "G", "H", "I"])
        # self.tblSudoku.setVisible(True)
        ## Show Widgets
        # layout.addWidget(self.btnRun)
        # layout.addWidget(self.tblSudoku)
        # self.setLayout(layout)

    def runSolver(self):
        global btEnd
        self.btnRun.setEnabled(False)
        self.btnRun.setText("Calculating...")
        self.tblSudoku.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QApplication.processEvents()
        basic()
        subThread = threading.Thread(target = backtrack, name = "btFunction")
        subThread.start()
        while not btEnd:
            print(sep="", end="")
        btEnd = False
        self.btnRun.setEnabled(True)
        self.btnRun.setText("Finished!")
        QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SSGui()
    widget.show()
    sys.exit(app.exec())
