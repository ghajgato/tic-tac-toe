import tkinter as tk
from tkinter import font

from XOEnv import XOEnv

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.num_rows):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.num_cols):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    def _update_grid(self):
        for btn_id, btn_content in zip(self._cells.keys(), self._game.board):
            if btn_content == self._game.id_x:
                btn_id.config(text="X")
            elif btn_content == self._game.id_o:
                btn_id.config(text="O")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        idx_of_clicked_btn = row*self._game.num_cols + col
        if not self._game.terminal(self._game.board):
            _, _, done, _, info = self._game.step(idx_of_clicked_btn)
            self._update_grid()

            if done:
                if info['winner'] == self._game.id_x:
                    self._update_display(msg="You won!", color="red")
                elif info['winner'] == self._game.id_o:
                    self._update_display(msg="Machine won!", color="red")
                elif info['winner'] == self._game.id_draw:
                    self._update_display(msg="Draw!", color="red")

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset()
        self._update_grid()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = XOEnv(machine_policy='minimax')
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()
