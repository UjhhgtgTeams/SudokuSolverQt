# -*- encoding: utf-8 -*-
"""
@File    :   main.py
@Author  :   UjhhgtgTeams
@Version :   1.0
@Contact :   feyxiexzf@gmail.com
@License :   (C)Copyright 2020-2021, UjhhgtgTeams
@Desc    :   A sudoku solver, built on the Kivy Framework.
"""

import resc
from resc import locales
import threading
from math import floor
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

x = y = xP = yP = 0
sudoku = resc.sudoku
stepTime = 0
btEnd = False
fastMode = False
stopBasic = False
noSolution = False
solutedNumbers = 0
possibilities = "123456789"
ids = {}


# noinspection PyMethodMayBeStatic,PyUnusedLocal
def runNormalSolver(no=""):
    global ids
    ids["fastSolver"].disabled = True
    ids["normalSolver"].disabled = True
    solverThread = Solver()
    solverThread.setDaemon(True)
    solverThread.basic()
    solverThread.start()


# noinspection PyUnusedLocal
def runFastSolver(no=""):
    global fastMode, ids
    fastMode = True
    ids["fastSolver"].disabled = True
    ids["normalSolver"].disabled = True
    runNormalSolver()


# noinspection PyMethodMayBeStatic
def updTable(tbX, tbY, tbItem):
    global ids
    value = ''
    if tbItem != "0": value = str(tbItem)
    ids[f"btn{tbX}{tbY}"].text = value
    ids[f"btn{tbX}{tbY}"].color = (255, 255, 1, 1)


# noinspection PyAbstractClass
class KVLayoutWidget(GridLayout):
    # noinspection PyUnusedLocal
    def __init__(self):
        GridLayout.__init__(self, cols=9, rows=16)
        self.add_buttons()

    def add_buttons(self):
        global sudoku, ids
        # Add Sudoku
        for i in range(81):
            k = floor(i / 9)
            m = i - floor(i / 9) * 9
            value = ''
            if sudoku[k][m] != 0:
                value = str(sudoku[k][m])
            button = Button(
                text=value,
                font_size="14sp",
                background_color=(255, 255, 255, 255),
                color=(255, 255, 255, 1)
            )
            self.add_widget(button)
            ids["btn" + str(k) + str(m)] = button
        # Add Placeholders
        for i in range(2 * 9): self.add_widget(Label(text=""))
        # Add Run Buttons
        for i in range(9):
            if i != 4:
                self.add_widget(Label(text=""))
            else:
                tmpButton = Button(text=locales["btnRunName"], font_size="16sp", on_release=runNormalSolver)
                self.add_widget(tmpButton)
                ids["normalSolver"] = tmpButton
        # Add Placeholders
        for i in range(9): self.add_widget(Label(text=""))
        # Add Run Buttons
        for i in range(9):
            if i != 4:
                self.add_widget(Label(text=""))
            else:
                tmpButton = Button(text=locales["btnFastModeName"], font_size="16sp", on_release=runFastSolver)
                self.add_widget(tmpButton)
                ids["fastSolver"] = tmpButton
        # Add Placeholders
        for i in range(2 * 9): self.add_widget(Label(text=""))


class KivySolverApp(App):
    def build(self):
        return KVLayoutWidget()


# noinspection PyMethodMayBeStatic
class Solver(threading.Thread):
    def __init__(self):
        super().__init__()

    def calcPos(self, xN, yN, sN=0, calcT=True):
        global fastMode, possibilities, sudoku
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

    def stepGrid(self, stepType):
        global xP, yP, stepTime, sudoku
        stepTime += 1
        if stepType == "n":
            if yP != 8:
                yP += 1
                if sudoku[xP][yP] > 0:
                    self.stepGrid("n")
                else:
                    sudoku[xP][yP] = 0
                    if not fastMode: updTable(xP, yP, "0")
            else:
                if xP != 8:
                    xP += 1
                    yP = 0
                    if sudoku[xP][yP] > 0:
                        self.stepGrid("n")
                    else:
                        sudoku[xP][yP] = 0
                        if not fastMode: updTable(xP, yP, "0")
                else:
                    return self.showRight()
        elif stepType == "b":
            if yP != 0:
                yP -= 1
                if sudoku[xP][yP] > 0:
                    self.stepGrid("b")
                else:
                    sudoku[xP][yP] = 0
                    if not fastMode: updTable(xP, yP, "0")
            else:
                if xP != 0:
                    xP -= 1
                    yP = 8
                    if sudoku[xP][yP] > 0:
                        self.stepGrid("b")
                    else:
                        sudoku[xP][yP] = 0
                        if not fastMode: updTable(xP, yP, "0")

    def run(self):
        global fastMode, xP, yP, sudoku
        if xP == 8 and yP == 8 and sudoku[xP][yP] > 0:
            return self.showRight()
        if sudoku[xP][yP] == 0:
            for testNum in range(1, 10):
                testNum = 0 - testNum
                if self.calcPos(xP, yP, testNum, False) is False:
                    continue
                sudoku[xP][yP] = testNum
                if not fastMode: updTable(xP, yP, abs(testNum))
                if xP == 8 and yP == 8:
                    return self.showRight()
                self.stepGrid("n")
                self.run()
            self.stepGrid("b")
        else:
            self.stepGrid("n")
            self.run()

    def showRight(self):
        global fastMode, sudoku, stepTime, btEnd, ids
        for fx in range(9):
            for fy in range(9):
                sudoku[fx][fy] = abs(sudoku[fx][fy])
                if fastMode: updTable(fx, fy, abs(sudoku[fx][fy]))
        # Debug - Display the result
        # for dx in range(9):
        #     for dy in range(9):
        #         print(sudoku[dx][dy], sep="", end=" ")
        #     print()

        ids["fastSolver"].disabled = False
        ids["normalSolver"].disabled = False
        btEnd = True
        return True

    def basic(self):
        global fastMode, x, y, sudoku, possibilities, solutedNumbers, noSolution, stopBasic
        while stopBasic is False:
            for x in range(9):
                for y in range(9):
                    if sudoku[x][y] == 0:
                        self.calcPos(x, y)
                        if len(possibilities) == 1:
                            sudoku[x][y] = int(possibilities)
                            if not fastMode: updTable(x, y, int(possibilities))
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
