import sys
import time
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import PyQt6.QtCore
import PyQt6.Qt
from math import floor

# from form import Ui_Form

# For Debug Purpose
sudokuSelection = 0  # Select the sudoku | Available options : 0, 1, 2
debugMessages = False  # Toggle if print debug messages | Available options : False, True
# END

if sudokuSelection == 0:
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
elif sudokuSelection == 1:
    sudoku = [
        [7, 4, 0, 2, 0, 9, 0, 0, 0],
        [0, 2, 0, 0, 8, 4, 0, 9, 0],
        [8, 0, 0, 0, 0, 3, 4, 0, 0],
        [5, 8, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 6, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 5, 0, 1, 9],
        [0, 0, 7, 5, 0, 0, 0, 0, 1],
        [0, 5, 0, 1, 4, 0, 0, 7, 0],
        [0, 0, 0, 9, 0, 2, 0, 5, 4]
    ]
elif sudokuSelection == 2:
    sudoku = [
        [0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 5, 0, 9, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 8, 1, 0, 0],
        [5, 0, 0, 3, 4, 0, 2, 0, 0],
        [1, 7, 0, 0, 0, 0, 0, 9, 4],
        [0, 0, 3, 0, 8, 9, 0, 0, 1],
        [0, 0, 9, 5, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 6, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 5, 0]
    ]
else:
    raise ValueError("Invalid sudoku selection.")
x = 0
y = 0
xP = 0
yP = 0
stepTime = 0
btEnd = False
possibilities = "123456789"
stopBasic = False
noSolution = False
solutedNumbers = 0


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


# noinspection PyUnresolvedReferences
# class SSGui(QWidget, Ui_Form):
class SSGui(QWidget):
    def __init__(self):
        super(SSGui, self).__init__()
        # self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        global sudoku
        # Init layout
        layout = QVBoxLayout()
        self.setWindowTitle(r"*** Sudoku Solver GUI ***   |   By: Ujhhgtg")
        self.resize(800, 700)
        # Buttons!!!
        # Run Button
        self.btnRun = QPushButton("RUN!!!", self)
        self.btnRun.setGeometry(220, 660, 361, 31)
        self.btnRun.setFont(QFont("Noto Sans", 14))
        self.btnRun.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnRun.clicked.connect(self.runSolver)
        # Tables!!!
        # Sudoku Table
        self.tblSudoku = QTableWidget(9, 9)
        self.tblSudoku.setGeometry(10, 10, 781, 641)
        self.tblSudoku.setFont(QFont("Noto Sans Arabic Light", 20))
        self.tblSudoku.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblSudoku.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblSudoku.horizontalHeader().setVisible(False)
        self.tblSudoku.verticalHeader().setVisible(False)
        # Set Initial Sudoku
        for ix in range(9):
            for iy in range(9):
                if sudoku[ix][iy] != 0:
                    tblItem = QTableWidgetItem(str(sudoku[ix][iy]))
                    tblItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
                    self.tblSudoku.setItem(ix, iy, tblItem)
                    QApplication.processEvents()
                else:
                    tblItem = QTableWidgetItem("")
                    tblItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
                    self.tblSudoku.setItem(ix, iy, tblItem)
                    QApplication.processEvents()
        # Show Widgets
        layout.addWidget(self.tblSudoku)
        layout.addWidget(self.btnRun)
        self.setLayout(layout)

    def runSolver(self):
        global btEnd, sudoku
        for ax in range(9):
            for ay in range(9):
                gotItem = self.tblSudoku.item(ax, ay).text()
                if gotItem != "":
                    sudoku[ax][ay] = int(self.tblSudoku.item(ax, ay).text())
                else:
                    sudoku[ax][ay] = 0
        self.btnRun.setEnabled(False)
        self.btnRun.setText("Calculating...")
        # noinspection PyTypeChecker
        self.tblSudoku.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QApplication.processEvents()
        subThread = calculate()
        subThread.updTblSignal.connect(updTable)
        subThread.updSttSignal.connect(updStatus)
        subThread.basic()
        subThread.start()
        while not btEnd:
            QApplication.processEvents()


# noinspection PyUnresolvedReferences
class calculate(PyQt6.QtCore.QThread):
    updTblSignal = PyQt6.QtCore.pyqtSignal(int, int, int)
    updSttSignal = PyQt6.QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        global sudoku, xP, yP, debugMessages
        if xP == 8 and yP == 8 and sudoku[xP][yP] > 0:
            return self.showRight()
        if sudoku[xP][yP] == 0:
            for testNum in range(1, 10):
                testNum = 0 - testNum
                if calcPos(xP, yP, testNum, False) is False:
                    continue
                sudoku[xP][yP] = testNum
                if debugMessages : print("Set ", xP, ", ", yP, " to ", testNum, ".", sep="")
                self.updTblSignal.emit(xP, yP, abs(testNum))
                time.sleep(0.00000000000000000000000000000000000000000000000001)
                if xP == 8 and yP == 8:
                    return self.showRight()
                self.stepGrid("n")
                self.run()
            self.stepGrid("b")
        else:
            self.stepGrid("n")
            self.run()

    def stepGrid(self, stepType):
        global xP, yP, stepTime, sudoku, debugMessages
        stepTime += 1
        if stepType == "n":
            if yP != 8:
                yP += 1
                if sudoku[xP][yP] > 0:
                    self.stepGrid("n")
                else:
                    sudoku[xP][yP] = 0
                    if debugMessages : print("Set ", xP, ", ", yP, " to 0.", sep="")
                    self.updTblSignal.emit(xP, yP, 0)
            else:
                if xP != 8:
                    xP += 1
                    yP = 0
                    if sudoku[xP][yP] > 0:
                        self.stepGrid("n")
                    else:
                        sudoku[xP][yP] = 0
                        if debugMessages : print("Set ", xP, ", ", yP, " to 0.", sep="")
                        self.updTblSignal.emit(xP, yP, 0)
                else:
                    return self.showRight()
        elif stepType == "b":
            if yP != 0:
                yP -= 1
                if sudoku[xP][yP] > 0:
                    self.stepGrid("b")
                else:
                    sudoku[xP][yP] = 0
                    if debugMessages : print("Set ", xP, ", ", yP, " to 0.", sep="")
                    self.updTblSignal.emit(xP, yP, 0)
            else:
                if xP != 0:
                    xP -= 1
                    yP = 8
                    if sudoku[xP][yP] > 0:
                        self.stepGrid("b")
                    else:
                        sudoku[xP][yP] = 0
                        if debugMessages : print("Set ", xP, ", ", yP, " to 0.", sep="")
                        self.updTblSignal.emit(xP, yP, 0)

    def showRight(self):
        global sudoku, stepTime, btEnd
        for fx in range(9):
            for fy in range(9):
                sudoku[fx][fy] = abs(sudoku[fx][fy])
        btEnd = True
        self.updSttSignal.emit()
        return True

    def basic(self):
        global x, y, sudoku, possibilities, solutedNumbers, noSolution, stopBasic
        while stopBasic is False:
            for x in range(9):
                for y in range(9):
                    if sudoku[x][y] == 0:
                        calcPos(x, y)
                        if len(possibilities) == 1:
                            sudoku[x][y] = int(possibilities)
                            self.updTblSignal.emit(x, y, int(possibilities))
                            QApplication.processEvents()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SSGui()
    widget.show()


    def updTable(uX, uY, uNum):
        global widget
        if uNum != 0:
            tblItem = QTableWidgetItem(str(uNum))
            tblItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
            tblItem.setForeground(QBrush(QColor(139, 129, 76)))
        else:
            tblItem = QTableWidgetItem("")
            tblItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter | Qt.AlignCenter)
        widget.tblSudoku.setItem(uX, uY, tblItem)


    def updStatus():
        global widget
        widget.btnRun.setText("Finished!")


    sys.exit(app.exec())
