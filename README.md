# SodukuSolver
This is a really useful sudoku solver with a Qt gui.

## USAGE
Enter the numbers in and click "RUN"!<br>
If you don't want to wait, simply press "FAST MODE" and there you go!<br>

## INSTALL
Download "Source Code (.zip)" from the repo and install PySide6 and PyQt6 with:<br>
Command: `pip install pyside6 pyqt6`<br>
Or Linux: `sudo pip install pyside6 pyqt6`<br>
Then, extract them all, and run main.py!<br>

## SCREENSHOTS
<img src="https://i.loli.net/2021/08/30/fcejxSH92iYEuvp.png" width="75%"/><br>
<img src="https://i.loli.net/2021/08/30/vGYPeEFjUzcACsl.png" width="75%"/><br>
<img src="https://i.loli.net/2021/08/30/cpjJhBqwoWDS1nu.png" width="75%"/><br>

## ROADMAP
1. Improve the algorithms<br>
|_ [Wikipedia](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms)

## FAQ
Q: What is the default sudoku it shows us?<br>
A: It is the hardest sudoku in the world, made by a mathematician in Finland.<br>

## KNOWN BUGS
[1] If the main window is closed by hitting the X button and the solver is still running, the program will may stay on until the solver finished.<br>
