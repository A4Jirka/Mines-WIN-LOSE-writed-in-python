import tkinter as tk
from random import shuffle

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, size=100, corner_radius=15, padding=5, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.command = command
        self.corner_radius = corner_radius
        self.padding = padding
        self.size = size

        self.bg_color = "lightgray"
        self.text_color = "black"
        self.font = ("Arial", 12, "bold")

        self.shadow_id = self.create_rounded_rectangle(padding + 2, padding + 2, size - padding + 2, size - padding + 2, corner_radius, fill="gray", outline="")
        self.rect_id = self.create_rounded_rectangle(padding, padding, size - padding, size - padding, corner_radius, outline="black", fill=self.bg_color)
        self.text_id = self.create_text(size // 2, size // 2, text=text, font=self.font, fill=self.text_color)

        self.bind("<Button-1>", self.on_click)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def set_text(self, text):
        self.itemconfig(self.text_id, text=text)
        self.update()

    def set_color(self, color):
        self.itemconfig(self.rect_id, fill=color)
        self.update()

    def on_click(self, event):
        self.command()

class RectangleButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=50, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        self.command = command

        self.bg_color = "lightblue"
        self.text_color = "black"
        self.font = ("Arial", 14, "bold")

        self.rect_id = self.create_rectangle(0, 0, width, height, outline="black", fill=self.bg_color)
        self.text_id = self.create_text(width // 2, height // 2, text=text, font=self.font, fill=self.text_color)

        self.bind("<Button-1>", self.on_click)

    def set_text(self, text):
        self.itemconfig(self.text_id, text=text)

    def set_color(self, color):
        self.itemconfig(self.rect_id, fill=color)

    def on_click(self, event):
        self.command()

class MinesweeperGUI:
    def __init__(self, grid_size=5, win_cells=11):
        self.grid_size = grid_size
        self.win_cells = win_cells
        self.lose_cells = grid_size * grid_size - win_cells
        self.grid = self.create_grid(grid_size, win_cells)
        self.revealed_grid = [['?' for _ in range(grid_size)] for _ in range(grid_size)]
        self.win_count = 0
        self.lose_count = 0

        self.root = tk.Tk()
        self.root.title("Mines WIN/LOSE by A4Jirka")
        self.root.geometry("800x800")

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.buttons = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        for row in range(grid_size):
            for col in range(grid_size):
                button_text = str(row * grid_size + col + 1)
                button = RoundedButton(self.frame, text=button_text, size=100, corner_radius=15,
                                       command=lambda r=row, c=col: self.reveal(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

        self.reset_button = RectangleButton(self.root, text="Reset Game", command=self.reset_game, width=200, height=50)
        self.reset_button.pack(pady=10)

    def create_grid(self, grid_size, win_cells):
        cells = ['WIN'] * win_cells + ['LOSE'] * (grid_size * grid_size - win_cells)
        shuffle(cells)
        return [cells[i * grid_size:(i + 1) * grid_size] for i in range(grid_size)]

    def reveal(self, row, col):
        if self.revealed_grid[row][col] != '?':
            return

        cell_value = self.grid[row][col]
        if cell_value == 'WIN':
            self.buttons[row][col].set_color("green")
            self.buttons[row][col].set_text('WIN')
            self.revealed_grid[row][col] = 'WIN'
            self.win_count += 1
        else:
            self.buttons[row][col].set_color("red")
            self.buttons[row][col].set_text('LOSE')
            self.revealed_grid[row][col] = 'LOSE'
            self.lose_count += 1

    def reset_game(self):
        self.grid = self.create_grid(self.grid_size, self.win_cells)
        self.revealed_grid = [['?' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.win_count = 0
        self.lose_count = 0

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button_text = str(row * self.grid_size + col + 1)
                self.buttons[row][col].set_color("lightgray")
                self.buttons[row][col].set_text(button_text)

    def run(self):
        self.root.mainloop()
