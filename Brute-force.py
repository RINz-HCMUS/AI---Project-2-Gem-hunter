import tkinter as tk
from tkinter import filedialog
import os 

class MinesweeperSolver:
    def __init__(self, master):
        self.master = master
        self.file_path = ""
        self.rows = 0
        self.cols = 0
        self.board = []
        self.solution = []
        self.create_widgets()
    
    # Tạo các widget
    def create_widgets(self):
        self.file_label = tk.Label(self.master, text="Chọn file map:")
        self.file_label.grid(row=0, column=0)
        self.file_entry = tk.Entry(self.master, state="disabled", width=30)
        self.file_entry.grid(row=0, column=1)
        self.browse_button = tk.Button(self.master, text="Chọn", command=self.select_file)
        self.browse_button.grid(row=0, column=2)

        self.solve_button = tk.Button(self.master, text="Giải Map", command=self.solve_map)
        self.solve_button.grid(row=1, columnspan=3)

    # Chọn file
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            self.file_entry.config(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)
            self.file_entry.config(state="disabled")
    
    # Đọc file map
    def load_map(self):
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                self.rows, self.cols = map(int, lines[0].split())
                self.board = [list(line.strip().split(',')) for line in lines[1:]]
                self.solution = [[cell for cell in row] for row in self.board]
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
            return False
        return True

    # Giải map
    def solve_map(self):
        if not self.file_path:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn file map.")
            return

        if not self.load_map():
            return

        # 
        while True:
            flag = False # Kiểm tra xem có thay đổi không
            non_zero_count = 0 

            # Tìm ô có số bom xung quanh lớn nhất
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.board[r][c] == '_':
                        count = self.count_adjacent_bombs(r, c)
                        if count > non_zero_count:
                            non_zero_count = count
                            max_r, max_c = r, c

            if non_zero_count == 0:
                break
            
            self.board[max_r][max_c] = 'T'
            self.solution[max_r][max_c] = 'T'
            
            self.decrement_adjacent_bombs(max_r, max_c)
            flag = True

            if not flag:
                break
        
        # Tạo các ô Gems
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '_':
                    self.solution[r][c] = 'G'

        self.display_solution()

    # Đếm số bom xung quanh ô (r, c)
    def count_adjacent_bombs(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc].isdigit():
                    if self.board[nr][nc] == '0':
                        return 0
                    else:
                        count += int(self.board[nr][nc])
        return count

    # Giảm số bom xung quanh ô (r, c)
    def decrement_adjacent_bombs(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc].isdigit():
                    self.board[nr][nc] = str(max(0, int(self.board[nr][nc]) - 1))

    # Hiển thị kết quả
    def display_solution(self):
        window = tk.Toplevel(self.master)
        window.title("Gems Hunter")

        cell_size = 20  # Kích thước mỗi ô

        canvas = tk.Canvas(window, bg="white", width=self.cols*cell_size, height=self.rows*cell_size)
        canvas.pack()

        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c*cell_size, r*cell_size
                x2, y2 = (c+1)*cell_size, (r+1)*cell_size

                # Tạo màu nền nhạt hơn cho ô
                if self.solution[r][c] == 'G':
                    background_color = "#B0C4DE"  # Màu xanh nhạt
                    text_color = "blue"
                    text = "G"
                elif self.solution[r][c] == 'T':
                    background_color = "#FFC0CB"  # Màu hồng nhạt
                    text_color = "red"
                    text = "T"
                else:
                    background_color = "#FFFFFF"  # Màu trắng
                    text_color = "black"
                    text = self.solution[r][c]

                # Tạo ô với màu nền nhạt
                canvas.create_rectangle(x1, y1, x2, y2, fill=background_color, outline="black")

                # Tạo văn bản trong ô với màu tương ứng
                canvas.create_text(c*cell_size + cell_size/2, r*cell_size + cell_size/2, text=text, fill=text_color)


def main():
    root = tk.Tk()
    root.title('Minesweeper Map Solver')

    solver = MinesweeperSolver(root)

    root.mainloop()

if __name__ == "__main__":
    main()
