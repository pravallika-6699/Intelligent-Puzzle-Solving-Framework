import tkinter as tk
from tkinter import messagebox
import random
import heapq
from itertools import count

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def manhattan(state):
    """Estimate remaining moves using Manhattan distance."""
    distance = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        goal_index = tile - 1
        row, col = divmod(index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        distance += abs(row - goal_row) + abs(col - goal_col)
    return distance


def get_neighbors(state):
    """Return all states reachable by moving the blank tile once."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    moves = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_index = nr * 3 + nc
            new_state = list(state)
            new_state[blank], new_state[new_index] = new_state[new_index], new_state[blank]
            moves.append(tuple(new_state))
    return moves


def is_solvable(state):
    """An 8-puzzle is solvable when its inversion count is even."""
    values = [x for x in state if x != 0]
    inversions = sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )
    return inversions % 2 == 0


def solve_astar(start):
    """A* search using f(n) = g(n) + h(n). Returns the solution path."""
    if not is_solvable(start):
        return None

    frontier = []
    tie_breaker = count()
    heapq.heappush(frontier, (manhattan(start), 0, next(tie_breaker), start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current_cost, _, current = heapq.heappop(frontier)

        if current == GOAL:
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            return list(reversed(path))

        if current_cost != cost_so_far[current]:
            continue

        for neighbor in get_neighbors(current):
            new_cost = current_cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + manhattan(neighbor)
                heapq.heappush(
                    frontier,
                    (priority, new_cost, next(tie_breaker), neighbor)
                )
    return None


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Puzzle Solving Framework")
        self.root.geometry("430x570")
        self.root.resizable(False, False)
        self.root.configure(bg="#eef2f7")

        self.state = GOAL
        self.solution = []
        self.step_index = 0
        self.buttons = []

        title = tk.Label(
            root, text="INTELLIGENT PUZZLE SOLVER",
            font=("Arial", 17, "bold"), bg="#eef2f7", fg="#17324d"
        )
        title.pack(pady=(18, 5))

        subtitle = tk.Label(
            root, text="8-Puzzle using A* Search Algorithm",
            font=("Arial", 10), bg="#eef2f7", fg="#526579"
        )
        subtitle.pack(pady=(0, 15))

        board = tk.Frame(root, bg="#eef2f7")
        board.pack()

        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(
                    board, text="", width=6, height=2,
                    font=("Arial", 22, "bold"),
                    relief="flat", bd=0,
                    command=lambda rr=r, cc=c: self.tile_click(rr, cc)
                )
                btn.grid(row=r, column=c, padx=5, pady=5, ipadx=5, ipady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.status = tk.Label(
            root, text="Click a tile next to the empty space to move it.",
            font=("Arial", 10), bg="#eef2f7", fg="#17324d",
            wraplength=380
        )
        self.status.pack(pady=14)

        controls = tk.Frame(root, bg="#eef2f7")
        controls.pack(pady=5)

        tk.Button(
            controls, text="New Puzzle", width=13, command=self.new_puzzle,
            bg="#2563eb", fg="white", activebackground="#1d4ed8",
            font=("Arial", 10, "bold"), relief="flat", padx=8, pady=8
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            controls, text="Solve with AI", width=13, command=self.solve,
            bg="#15803d", fg="white", activebackground="#166534",
            font=("Arial", 10, "bold"), relief="flat", padx=8, pady=8
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            controls, text="Next Step", width=13, command=self.next_step,
            bg="#d97706", fg="white", activebackground="#b45309",
            font=("Arial", 10, "bold"), relief="flat", padx=8, pady=8
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            controls, text="Reset", width=13, command=self.reset,
            bg="#475569", fg="white", activebackground="#334155",
            font=("Arial", 10, "bold"), relief="flat", padx=8, pady=8
        ).grid(row=1, column=1, padx=5, pady=5)

        note = tk.Label(
            root,
            text="Goal: arrange tiles from 1 to 8, with the blank space last.",
            font=("Arial", 9), bg="#eef2f7", fg="#526579",
            wraplength=380
        )
        note.pack(pady=15)

        self.update_board()

    def update_board(self):
        for i, tile in enumerate(self.state):
            r, c = divmod(i, 3)
            if tile == 0:
                self.buttons[r][c].configure(
                    text="", bg="#cbd5e1", activebackground="#cbd5e1",
                    state="normal"
                )
            else:
                self.buttons[r][c].configure(
                    text=str(tile), bg="#ffffff", fg="#17324d",
                    activebackground="#dbeafe", state="normal"
                )

    def tile_click(self, row, col):
        index = row * 3 + col
        blank = self.state.index(0)
        if abs(row - blank // 3) + abs(col - blank % 3) == 1:
            new_state = list(self.state)
            new_state[blank], new_state[index] = new_state[index], new_state[blank]
            self.state = tuple(new_state)
            self.solution = []
            self.update_board()
            self.status.config(text="Your move. Press Solve with AI to find a solution.")
            if self.state == GOAL:
                self.status.config(text="Congratulations! You solved the puzzle.")

    def new_puzzle(self):
        # Scramble by legal moves, so the generated puzzle is always solvable.
        state = GOAL
        previous = None
        for _ in range(25):
            choices = [s for s in get_neighbors(state) if s != previous]
            next_state = random.choice(choices)
            previous, state = state, next_state
        self.state = state
        self.solution = []
        self.step_index = 0
        self.update_board()
        self.status.config(text="New puzzle created. Try solving it or use Solve with AI.")

    def solve(self):
        self.status.config(text="AI is searching for the shortest solution...")
        self.root.update_idletasks()
        self.solution = solve_astar(self.state)
        self.step_index = 0
        if self.solution is None:
            self.status.config(text="No solution exists for this arrangement.")
        elif len(self.solution) == 1:
            self.status.config(text="Puzzle is already solved!")
        else:
            self.status.config(
                text=f"Solution found! {len(self.solution) - 1} moves. Click Next Step to view."
            )

    def next_step(self):
        if not self.solution:
            self.status.config(text="First click Solve with AI.")
            return
        if self.step_index < len(self.solution) - 1:
            self.step_index += 1
            self.state = self.solution[self.step_index]
            self.update_board()
            if self.step_index == len(self.solution) - 1:
                self.status.config(text="Puzzle solved successfully by the A* algorithm!")
            else:
                self.status.config(
                    text=f"AI solution: step {self.step_index} of {len(self.solution) - 1}"
                )
        else:
            self.status.config(text="Solution is complete. Click New Puzzle to play again.")

    def reset(self):
        if self.solution:
            self.state = self.solution[0]
        else:
            self.state = GOAL
        self.solution = []
        self.step_index = 0
        self.update_board()
        self.status.config(text="Board reset. Click New Puzzle to start another game.")


if __name__ == "__main__":
    window = tk.Tk()
    app = PuzzleApp(window)
    window.mainloop()