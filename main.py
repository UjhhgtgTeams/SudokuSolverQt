import time
import threading
from math import floor
from resc import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
Builder.load_file("KivyLayout.kv")


class KivySolverApp(App):
    def build(self):
        return ScreenManager()


# noinspection PyRedeclaration
class ScreenManager(ScreenManager):
    pass


class SolverScreen(Screen):
    def runSolver(self):
        basic()
        btThread = threading.Thread(name="backtrackSolver", target=backtrack)
        btThread.setDaemon(True)
        btThread.start()


class SettingScreen(Screen):
    pass


x = y = xP = yP = 0
stepTime = 0
btEnd = False
stopBasic = False
noSolution = False
solutedNumbers = 0
possibilities = "123456789"


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
                return showRight()
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


def backtrack():
    global xP, yP, sudoku
    if xP == 8 and yP == 8 and sudoku[xP][yP] > 0:
        return showRight()
    if sudoku[xP][yP] == 0:
        for testNum in range(1, 10):
            testNum = 0 - testNum
            if calcPos(xP, yP, testNum, False) is False:
                continue
            sudoku[xP][yP] = testNum
            if xP == 8 and yP == 8:
                return showRight()
            stepGrid("n")
            backtrack()
        stepGrid("b")
    else:
        stepGrid("n")
        backtrack()


def showRight():
    global sudoku, stepTime, btEnd
    for fx in range(9):
        for fy in range(9):
            sudoku[fx][fy] = abs(sudoku[fx][fy])
    btEnd = True
    for px in range(9):
        for py in range(9):
            print(sudoku[px][py], sep="", end="")
            print(" ", sep="", end="")
        print("\n", sep="", end="")
    return True


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


KivySolverApp().run()
