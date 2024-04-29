import tkinter as tk
from tkinter import messagebox
import os

"""
Bombs - (black)
Empty cells or Gems - (white)
"""

class MinesweeperEditor:
    def __init__(self, master):
        self.master = master
        self.rows = 0
        self.cols = 0
        self.file_name = ""
        self.buttons = []
        self.board = []

        self.create_input_widgets()
    
    # Create the input widgets
    def create_input_widgets(self):
        self.rows_label = tk.Label(self.master, text="Số hàng:")
        self.rows_label.grid(row=0, column=0)
        self.rows_entry = tk.Entry(self.master)
        self.rows_entry.grid(row=0, column=1)

        self.cols_label = tk.Label(self.master, text="Số cột:")
        self.cols_label.grid(row=1, column=0)
        self.cols_entry = tk.Entry(self.master)
        self.cols_entry.grid(row=1, column=1)

        self.file_label = tk.Label(self.master, text="Tên file (bao gồm đuôi .txt):")
        self.file_label.grid(row=2, column=0)
        self.file_entry = tk.Entry(self.master)
        self.file_entry.grid(row=2, column=1)

        self.continue_button = tk.Button(self.master, text="Tiếp tục", command=self.create_map)
        self.continue_button.grid(row=3, columnspan=2)

    # Check & Create the map  
    def create_map(self):
        # Check if the input is valid
        try:
            self.rows = int(self.rows_entry.get())
            self.cols = int(self.cols_entry.get())
            self.file_name = self.file_entry.get()
            # Check if the file name has .txt extension
            if not self.file_name.endswith('.txt'):
                self.file_name += '.txt'
            # Check if the rows and columns are valid
            if self.rows <= 0 or self.cols <= 0:
                raise ValueError("Kích thước không hợp lệ. Vui lòng nhập lại.")
            
            # Remove the input widgets
            for widget in (self.rows_label, self.rows_entry, self.cols_label, self.cols_entry, self.file_label, self.file_entry, self.continue_button):
                widget.grid_remove()

            # Create the map widgets
            self.create_map_widgets()
        
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    # Create the map widgets
    def create_map_widgets(self):
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                button = tk.Button(self.master, text='_', width=2, command=lambda r=r, c=c: self.toggle_cell(r, c))
                button.grid(row=r, column=c)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.ok_button = tk.Button(self.master, text='OK', command=self.save_board)
        self.ok_button.grid(row=self.rows, columnspan=self.cols)


    def toggle_cell(self, row, col):
        if self.buttons[row][col]['text'] == '_':
            self.buttons[row][col].config(text='T', bg='black')
        else:
            self.buttons[row][col].config(text='_', bg='white')

    # Save the board to a file
    def save_board(self):
        self.board = [['_' for _ in range(self.cols)] for _ in range(self.rows)]

        for r in range(self.rows):
            for c in range(self.cols):
                if self.buttons[r][c]['text'] == 'T':
                    self.board[r][c] = 'T'
        
        self.calculate_numbers()

        if not os.path.exists("map"):
            os.makedirs("map")

        file_path = os.path.join("map", self.file_name)
        with open(file_path, 'w') as f:
            f.write(f"{self.rows} {self.cols}\n")
            for row in self.board:
                row_data = ','.join(row)
                f.write(row_data + '\n')

    # Calculate the numbers for the board & encode the board 
    def calculate_numbers(self):
        # Calculate
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 'T':
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == 'T':
                                count += 1
                    self.board[r][c] = str(count)
        
        # Encode the board
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 'T' or self.board[r][c] == '0':
                    self.board[r][c] = '_'       

def main():
    root = tk.Tk()
    root.title('Minesweeper Map Editor')

    editor = MinesweeperEditor(root)

    root.mainloop()

if __name__ == "__main__":
    main()
