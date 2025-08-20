import tkinter as tk
import random

class MazeGame:
    def __init__(self, master, rows, cols, cell_size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.canvas = tk.Canvas(master, width=cols * cell_size, height=rows * cell_size, bg='black')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_click)

        self.start_pos = (0, 0)
        self.end_pos = (rows - 1, cols - 1)
        self.player_pos = self.start_pos
        self.player_path = [self.start_pos]
        self.restart_button = None

        self.generate_maze()
        self.draw_maze()
        self.draw_player()

    def generate_maze(self):
        self.grid = [[{'walls': {'top': True, 'right': True, 'bottom': True, 'left': True}, 'visited': False} for _ in range(self.cols)] for _ in range(self.rows)]
        stack = []
        current_cell = (0, 0)
        self.grid[current_cell[0]][current_cell[1]]['visited'] = True
        stack.append(current_cell)

        while stack:
            current_cell = stack[-1]
            unvisited_neighbors = self.get_unvisited_neighbors(current_cell)

            if unvisited_neighbors:
                direction, next_cell = random.choice(unvisited_neighbors)
                self.remove_walls(current_cell, next_cell, direction)
                self.grid[next_cell[0]][next_cell[1]]['visited'] = True
                stack.append(next_cell)
            else:
                stack.pop()

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        r, c = cell
        if r > 0 and not self.grid[r - 1][c]['visited']:
            neighbors.append(('top', (r - 1, c)))
        if c < self.cols - 1 and not self.grid[r][c + 1]['visited']:
            neighbors.append(('right', (r, c + 1)))
        if r < self.rows - 1 and not self.grid[r + 1][c]['visited']:
            neighbors.append(('bottom', (r + 1, c)))
        if c > 0 and not self.grid[r][c - 1]['visited']:
            neighbors.append(('left', (r, c - 1)))
        return neighbors

    def remove_walls(self, current_cell, next_cell, direction):
        r1, c1 = current_cell
        r2, c2 = next_cell
        
        if direction == 'top':
            self.grid[r1][c1]['walls']['top'] = False
            self.grid[r2][c2]['walls']['bottom'] = False
        elif direction == 'right':
            self.grid[r1][c1]['walls']['right'] = False
            self.grid[r2][c2]['walls']['left'] = False
        elif direction == 'bottom':
            self.grid[r1][c1]['walls']['bottom'] = False
            self.grid[r2][c2]['walls']['top'] = False
        elif direction == 'left':
            self.grid[r1][c1]['walls']['left'] = False
            self.grid[r2][c2]['walls']['right'] = False

    def draw_maze(self):
        self.canvas.delete('all')
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if self.grid[r][c]['walls']['top']:
                    self.canvas.create_line(x1, y1, x2, y1, fill='white')
                if self.grid[r][c]['walls']['right']:
                    self.canvas.create_line(x2, y1, x2, y2, fill='white')
                if self.grid[r][c]['walls']['bottom']:
                    self.canvas.create_line(x1, y2, x2, y2, fill='white')
                if self.grid[r][c]['walls']['left']:
                    self.canvas.create_line(x1, y1, x1, y2, fill='white')
        
        shrink = self.cell_size * 0.1
        start_x1 = self.start_pos[1] * self.cell_size + shrink
        start_y1 = self.start_pos[0] * self.cell_size + shrink
        start_x2 = (self.start_pos[1] + 1) * self.cell_size - shrink
        start_y2 = (self.start_pos[0] + 1) * self.cell_size - shrink
        self.canvas.create_rectangle(start_x1, start_y1, start_x2, start_y2, fill='green', outline='')
        
        end_x1 = self.end_pos[1] * self.cell_size + shrink
        end_y1 = self.end_pos[0] * self.cell_size + shrink
        end_x2 = (self.end_pos[1] + 1) * self.cell_size - shrink
        end_y2 = (self.end_pos[0] + 1) * self.cell_size - shrink
        self.canvas.create_rectangle(end_x1, end_y1, end_x2, end_y2, fill='red', outline='')

    def draw_player(self):
        r, c = self.player_pos
        x1 = c * self.cell_size + self.cell_size // 4
        y1 = r * self.cell_size + self.cell_size // 4
        x2 = x1 + self.cell_size // 2
        y2 = y1 + self.cell_size // 2
        self.canvas.create_oval(x1, y1, x2, y2, fill='blue', tags='player')

    def on_click(self, event):
        if self.player_pos == self.end_pos:
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        target_pos = (row, col)

        if target_pos == self.player_pos:
            return

        path = self.get_path_to_target(self.player_pos, target_pos)

        if path:
            self.player_pos = target_pos
            self.player_path.extend(path)
            self.draw_player_path()
            self.draw_player()
            self.check_win()

    def get_path_to_target(self, start, end):
        r1, c1 = start
        r2, c2 = end
        
        dr = r2 - r1
        dc = c2 - c1
        
        if dr != 0 and dc != 0:
            return None

        path = []
        if dr != 0:
            step_r = 1 if dr > 0 else -1
            for r in range(r1, r2, step_r):
                if step_r == 1 and self.grid[r][c1]['walls']['bottom']:
                    return None
                if step_r == -1 and self.grid[r][c1]['walls']['top']:
                    return None
                path.append((r + step_r, c1))
            return path
        
        if dc != 0:
            step_c = 1 if dc > 0 else -1
            for c in range(c1, c2, step_c):
                if step_c == 1 and self.grid[r1][c]['walls']['right']:
                    return None
                if step_c == -1 and self.grid[r1][c]['walls']['left']:
                    return None
                path.append((r1, c + step_c))
            return path
        
        return None

    def draw_player_path(self):
        self.canvas.delete('player')
        self.canvas.delete('path')
        if len(self.player_path) > 1:
            points = []
            for r, c in self.player_path:
                x = c * self.cell_size + self.cell_size // 2
                y = r * self.cell_size + self.cell_size // 2
                points.append(x)
                points.append(y)
            self.canvas.create_line(points, fill='cyan', width=2, tags='path')

    def check_win(self):
        if self.player_pos == self.end_pos:
            self.canvas.create_text(self.cols * self.cell_size / 2, self.rows * self.cell_size / 2, text='Kazandın!', fill='gold', font=('Arial', 24, 'bold'))
            self.show_restart_button()

    def show_restart_button(self):
        if self.restart_button:
            self.restart_button.destroy()
        
        win_text_y = self.rows * self.cell_size / 2
        button_y = win_text_y + self.cell_size * 1.5

        self.restart_button = tk.Button(self.master, text="Tekrar Oyna", command=self.reset_game)
        self.canvas.create_window(self.cols * self.cell_size / 2, button_y, window=self.restart_button)

    def reset_game(self):
        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None
        
        self.player_pos = self.start_pos
        self.player_path = [self.start_pos]
        self.generate_maze()
        self.draw_maze()
        self.draw_player()

def main():
    root = tk.Tk()
    root.title("Labirent Oyunu")
    MazeGame(root, rows=10, cols=10, cell_size=40)
    root.mainloop()

if __name__ == "__main__":
    main()