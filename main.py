import tkinter as tk
from tkinter import messagebox
import random
# Difficulty settings
DIFFICULTIES = {
    "Easy": (10, 10, 15),
    "Medium": (15, 15, 35),
    "Hard": (20, 20, 60),
    "Impossible": (30, 30, 150)
}

class Minesweeper:

    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.root.title("Minesweeper")

        self.buttons = {}
        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.game_finished = False

        # Main game frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Information label
        self.info = tk.Label(
            self.root,
            text=f"Mines: {self.total_mines} | Flags: 0",
            font=("Arial", 12)
        )
        self.info.pack()

        self.create_buttons()
        self.place_mines()

    def create_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):

                btn = tk.Button(
                    self.frame,
                    width=3,
                    height=1,
                    font=("Arial", 9),
                    command=lambda r=r, c=c: self.on_click(r, c)
                )

                btn.grid(row=r, column=c)

                # Right-click to flag
                btn.bind(
                    "<Button-3>",
                    lambda event, r=r, c=c: self.toggle_flag(r, c)
                )

                self.buttons[(r, c)] = btn

    def place_mines(self):
        all_cells = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
        ]

        self.mines = set(
            random.sample(all_cells, self.total_mines)
        )

    def toggle_flag(self, r, c):

        if self.game_finished:
            return

        if (r, c) in self.revealed:
            return

        btn = self.buttons[(r, c)]

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            btn.config(text="", bg="SystemButtonFace")

        else:
            self.flags.add((r, c))
            btn.config(text="🚩", bg="yellow")

        self.info.config(
            text=f"Mines: {self.total_mines} | Flags: {len(self.flags)}"
        )

    def on_click(self, r, c):

        if self.game_finished:
            return

        if (r, c) in self.flags:
            return

        if (r, c) in self.revealed:
            return

        if (r, c) in self.mines:
            self.reveal_mines()
            self.game_over(False)

        else:
            self.reveal_cell(r, c)

            if self.check_win():
                self.game_over(True)

    def reveal_mines(self):

        for r, c in self.mines:
            self.buttons[(r, c)].config(
                text="💣",
                bg="red",
                state="disabled"
            )

    def reveal_cell(self, r, c):

        if (r, c) in self.revealed:
            return

        if (r, c) in self.flags:
            return

        self.revealed.add((r, c))

        btn = self.buttons[(r, c)]

        count = self.count_adjacent_mines(r, c)

        btn.config(
            text=str(count) if count > 0 else "",
            bg="lightgray",
            state="disabled"
        )

        if count == 0:

            for nr, nc in self.neighbors(r, c):
                self.reveal_cell(nr, nc)

    def count_adjacent_mines(self, r, c):

        return sum(
            (nr, nc) in self.mines
            for nr, nc in self.neighbors(r, c)
        )

    def neighbors(self, r, c):

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):

                if dr == 0 and dc == 0:
                    continue

                nr = r + dr
                nc = c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def check_win(self):

        return len(self.revealed) == (
            self.rows * self.cols - self.total_mines
        )

    def game_over(self, won):

        self.game_finished = True

        if won:
            messagebox.showinfo(
                "Minesweeper",
                "Congratulations! You Win!"
            )
        else:
            messagebox.showinfo(
                "Minesweeper",
                "BOOM! Game Over!"
            )

        self.root.destroy()


class MinesweeperMenu:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Minesweeper Menu")
        self.root.geometry("300x250")

        tk.Label(
            self.root,
            text="MINESWEEPER",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Choose your difficulty:",
            font=("Arial", 12)
        ).pack(pady=5)

        self.difficulty = tk.StringVar(value="Easy")

        self.menu = tk.OptionMenu(
            self.root,
            self.difficulty,
            *DIFFICULTIES.keys()
        )
        self.menu.pack(pady=10)

        tk.Button(
            self.root,
            text="Start Game",
            width=15,
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Quit",
            width=15,
            command=self.root.destroy
        ).pack()

    def start_game(self):
        global restart
        difficulty = self.difficulty.get()

        rows, cols, mines = DIFFICULTIES[difficulty]

        self.root.destroy()

        game_root = tk.Tk()

        Minesweeper(
            game_root,
            rows,
            cols,
            mines
        )
        restart = tk.BooleanVar(value=True)
        game_root.mainloop()
def run_game():
    menu = MinesweeperMenu()
    menu.root.mainloop()

restart = True
text = False
while restart:
    run_game()
    while not text:
        user_inpt = input("Restart? (y/n): ")
        if user_inpt == "y":
            restart = True
            text = True
        elif user_inpt == "n":
            restart = False
            text = True
            print("Credits:\n"
                  "By Ishaan Nair\n"
                  "MineSweeper Remix")
        else:
            print("Invalid input!")
            text = False
