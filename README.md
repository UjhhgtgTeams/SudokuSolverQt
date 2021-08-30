# SodukuSolver
This is a really useful sudoku solver with a qt gui.

## USAGE
Enter the numbers in and click "RUN"!<br>
If you don't want to wait, simply press "FAST RUN" and there you go!<br>

## INSTALL
Download main.py from the releases and install PySide6 and PyQt6.<br>
Command: `pip install pyside6 pyqt6`<br>
Or Linux: `sudo pip install pyside6 pyqt6`<br>
Then run main.py!<br>

## FAQ
Q: What is the default sudoku it shows us?<br>
A: It is the hardest sudoku in the world, made by a mathematician in Finland.<br>

## KNOWN BUGS
[1] If using fast mode, the program may state that there is no solution, but there actually is a VALID solution (and it will be shown).<br>
<b>FIX: v1.0.3</b><br>
[2] If the main window is closed (hit the X button) and the solver is still running, the program will may stay on until the solver finished.<br>
<b>FIX: v1.0.3</b><br>