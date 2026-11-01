Intelligent Puzzle Solving Framework
A beginner-friendly 8-Puzzle game built with Python and Tkinter. It uses the A* search algorithm with Manhattan distance to find a shortest solution.
Requirements
Python 3.9 or newer
Visual Studio Code
Python extension for VS Code
Tkinter is included with most standard Python installations. No third-party packages are required.
Run in VS Code
Extract Intelligent_Puzzle_Solving_Framework.zip.
Open VS Code.
Select File > Open Folder and choose the extracted project folder.
Open main.py.
Open the VS Code terminal: Terminal > New Terminal.
Run:
python main.py
On some systems, use:
py main.py
How to use
New Puzzle: creates a random solvable board.
Solve with AI: runs A* and calculates a shortest solution.
Next Step: displays the next move in the AI solution.
Reset: returns to the starting state of the current solution, or the goal board if no solution has been calculated.
You can also click a tile next to the blank space to move it manually.
AI algorithm
A* uses:
f(n) = g(n) + h(n)
g(n): number of moves made so far.
h(n): Manhattan distance from each tile to its goal position.
f(n): estimated total path cost.
The program checks puzzle solvability using inversion parity. New puzzles are created by making legal random moves from the solved board, so they are always solvable.
Project files
main.py — complete application and A* solver.
README.md — setup and usage instructions.
