import os
import time
from tkinter import*
from datetime import datetime
from OptimalAlgorithm import*
from PysatSupport import*
from Backtracking import*
from Brute_Force import*

class GUI:
    def __init__(self, window):
        self.window = window
        self.window.title

        # Thiết lặp kích thước cho cửa sổ
        window_width = 1080
        window_height = 720
        self.window.geometry(f"{window_width}x{window_height}")

        # Gọi hàm center_window để đặt cửa sổ vào trung tâm của màn hình
        self.center_window(window_width, window_height)

        # Thiết lập thuộc tính hiện thị, hiển thị chồng lên các cửa sổ khác
        self.window.attributes("-topmost", TRUE)

        # Tải hình ảnh để thiết lập background
        self.image_bg = PhotoImage(file="photo/back_ground5.png")
        self.image_moon = PhotoImage(file="photo/moon.png")
        self.image_earth = PhotoImage(file="photo/earth.png")
        self.image_bg_board = PhotoImage(file="photo/main_bg.png")

        # Tạo label hiển thị background 
        self.back_ground = Label(self.window, image=self.image_bg)

        # Đặt kích thước và vị trí hiển thị của bg
        self.back_ground.place(x=0, y=0, relheight=1, relwidth=1)

        # Vẽ các nút bắt đầu và kết thúc
        self.start_button = Button(self.window, font=("Courier New", 40, "bold"), text="START",bg="#192847", fg="white", command=self.show_levels)
        self.start_button.place(x=370, y=270, width=300, height=100)

        # Nút kết thúc
        self.exit_button = Button(self.window, font=("Courier New", 40, "bold"), text="EXIT", bg="#192847", fg="white", command=self.exit_window)
        self.exit_button.place(x=370, y=380, width=300, height=100)

        # Tạo các danh sách
        self.level_buttons = []
        self.map_buttons = []
        self.grid = []
        self.box_maps = []
        self.size = 0
        self.transfer_speed = 5
        self.size_cell = 0

        # Biến lưu trạng thái chạy thuật toán
        self.is_running = False
        self.start_time = 0

        # Lưu thông số thống kê chạy thuật toán của từng loại
        self.time_for_optimal_algorithm = 0
        self.time_for_pysat_lib = 0
        self.time_for_brute_force = 0
        self.time_for_backtracking = 0


        for i in range(5):
            level_button = Button(self.window, font=("Courier New", 35, "bold"), text="LEVEL {}".format(i+1),bg="#192847", fg="white", command=lambda level=i+1: self.show_maps(level))
            self.level_buttons.append(level_button)

    def set_background_board(self):
        # Tạo label hiển thị background 
        self.back_ground_board = Label(self.window, image=self.image_bg_board)
        self.back_ground_moon = Label(self.window, image=self.image_moon, bg="#192847")
        self.back_ground_earth = Label(self.window, image=self.image_earth, bg="#192847")

        # Đặt kích thước và vị trí hiển thị của bg
        self.back_ground_board.place(x=500, y=0, relheight=1, relwidth=1)

        self.tranfer_background()

    def tranfer_background(self):
        self.transfer_speed += 1
        if(self.transfer_speed < 720): 
            self.back_ground_board.place(x= 0, y= 720 - self.transfer_speed, relheight=1, relwidth=1)
            self.back_ground.place(x=0, y= 0 - self.transfer_speed, relheight=1, relwidth=1)
            self.window.after(1, self.tranfer_background)
        elif (self.transfer_speed < 1500):
            self.transfer_speed -= 0.5
            self.back_ground_earth.place(x=-1100 + self.transfer_speed, y= 200)
            self.back_ground_moon.place(x=2200 - self.transfer_speed, y=100)
            self.window.after(1, self.tranfer_background)
        else: 
            time.sleep(0.5)
            self.board()

    def draw_board_game(self):
        print("Draw board in Game")
        self.set_background_board()
        
    def board(self):
        row, col = self.size

        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.size_cell = (min(self.width, self.height) - 200) // row
        self.start_x = (self.width - self.size_cell * row) // 2
        self.start_y = (self.height - self.size_cell * row) // 2

        for i in range(row):
            for j in range(col):
                if (isinstance(self.grid[i][j], int)): color = "#547FAF"
                else: color = "#EBE0EA"

                # Tạo label cho ô vuông với nền màu xám và viền màu đen
                button = Button(self.window, font=("Courier New", 10, "bold"), text=str(self.grid[i][j]), bg=color, fg="white")
                button.place(x=self.start_x + self.size_cell * j, y=  self.start_y + self.size_cell * i, width=self.size_cell, height=self.size_cell)
                self.box_maps.append(button)

        # Vẽ nút giải
        self.button_solve = Button(self.window, font=("Courier New", 20, "bold"), text="SOLVE", bg="grey", fg="white", command=self.board_solved)
        self.button_solve.place(x=self.width//2 - 50, y=self.height - 80, width=100, height=50)

        self.button_menu = Button(self.window, font=("Courier New", 20, "bold"), text="MENU", bg="grey", fg="white", command=self.menu_button)
        self.button_menu.pack(padx=5, pady=5)

        # Hiển thị bộ đếm thời gian
        self.timer_label = Label(self.window, text="00:00:000", font=("Courier New", 18, "bold"))
        self.timer_label.pack()
        
    def menu_button(self):
        self.window.destroy()
        self = None
        main()

    def format_timer(self, elapsed_time):
        milliseconds = int(elapsed_time.total_seconds() * 1000)
        time_str = "{:02d}:{:02d}:{:03d}".format((milliseconds // 60000) % 60, (milliseconds // 1000) % 60, milliseconds % 1000)
        return time_str
    
    def update_timer(self):
        current_time = datetime.now()
        elapsed_time = current_time - self.start_time
        time_str = self.format_timer(elapsed_time)
        self.timer_label.config(text=time_str)
        self.time_for_pysat_lib = time_str # Lưu lại thông số thời gian xử lý

    def board_solved(self):
        # Xóa các vị trí cũ
        self.button_solve.place_forget()
        for element in self.box_maps:
            element.place_forget()
        self.box_maps.clear

        row, col = self.size
        grid_pysat = self.grid.copy()
        grid_optimal = self.grid.copy()
        grid_backtracking = self.grid.copy()
        grid_brute = self.grid.copy()
        # Sử dụng Pysat để minh họa cho kết quả
        # Bắt đầu đếm thời gian
        self.start_time = datetime.now()

        # Giải bài toán
        size = self.size
        self.output_grid = Pysat_Solution(grid_pysat, size)
        self.update_timer()
        
        # Xuất kết quả
        if self.output_grid is not None:
            for i in range(row):
                for j in range(col):
                    # Màu mặc định
                    color_text = "white"
                    color = "#506465"

                    # Tô màu khác biệt cho mỗi ô Gem và Trap
                    if(self.output_grid[i][j] == "G") : 
                        color, color_text = "#5FCAD8", "#547FAF"
                    elif(self.output_grid[i][j] == "T") : 
                        color = "#EF6C62"

                    # Tạo label cho ô vuông
                    button = Button(self.window, font=("Courier New", 10, "bold"), text=str(self.output_grid[i][j]), bg=color, fg=color_text)
                    button.place(x=self.start_x + self.size_cell * j, y= self.start_y + self.size_cell * i, width=self.size_cell, height=self.size_cell)
                    self.box_maps.append(button)

        # Nếu không giải được kết quả
        else :
            print("No solution found is returned by Brute_Force_Solution.")

        # Chạy các thuật toán còn lại để so sánh các thông số
        # Thuật toán chạy bằng Brute_Force
        size, grid = read_input_file(self.file_name)
        self.start_time = datetime.now()
        Brute_Force_Solution(grid.copy(), size)
        elapsed_time = datetime.now() - self.start_time 
        self.time_for_brute_force = self.format_timer(elapsed_time)

        # Thuật toán chạy bằng Backtracking DPLL
        size, grid = read_input_file(self.file_name)
        self.start_time = datetime.now()
        Backtracking_Solution(grid.copy(), size)
        elapsed_time = datetime.now() - self.start_time 
        self.time_for_backtracking = self.format_timer(elapsed_time)

        # Thuật toán chạy bằng Optimal Algorithm - sử dụng phương pháp Backtracking CDCL, để giải SAT
        size, grid = read_input_file(self.file_name)
        self.start_time = datetime.now()
        Optimal_Algorithm_Solution(grid.copy(), size)
        elapsed_time = datetime.now() - self.start_time 
        self.time_for_optimal_algorithm = self.format_timer(elapsed_time)

        self.button_statistic = Button(self.window, font=("Courier New", 20, "bold"), text="STATISTIC", bg="#97D76D", fg="white", command=self.statistic)
        self.button_statistic.place(x=self.width//2 - 100, y=self.height - 80, width=200, height=60)

    def statistic(self):
        self.table_frame = Frame(self.window, width=300, height=400)
        self.table_frame.pack(padx=50, pady=50)

        # Tạo tiêu đề cho các cột
        self.algorithm_label = Label(self.table_frame, text="Thuật toán", font=("Courier New", 10))
        self.algorithm_label.grid(row=0, column=0)

        self.map_type_label = Label(self.table_frame, text="Loại map", font=("Courier New", 10))
        self.map_type_label.grid(row=0, column=1)

        self.processing_time_label = Label(self.table_frame, text="Thời gian xử lý", font=("Courier New", 10))
        self.processing_time_label.grid(row=0, column=2)

        # Hiển thị thời gian cho thuật toán A
        self.algorithm_pysat_label = Label(self.table_frame, text="Pysat Library", font=("Courier New", 10))
        self.algorithm_pysat_label.grid(row=1, column=0)

        self.map_type_pysat_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_pysat_label.grid(row=1, column=1)

        self.time_pysat_label = Label(self.table_frame, text=self.time_for_pysat_lib, font=("Courier New", 10))
        self.time_pysat_label.grid(row=1, column=2)

        # Hiển thị thời gian cho thuật toán B
        self.algorithm_optimal_label = Label(self.table_frame, text="Optimal", font=("Courier New", 10))
        self.algorithm_optimal_label.grid(row=2, column=0)

        self.map_type_optimal_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_optimal_label.grid(row=2, column=1)

        self.time_optimal_label = Label(self.table_frame, text=self.time_for_optimal_algorithm, font=("Courier New", 10))
        self.time_optimal_label.grid(row=2, column=2)

        # Hiển thị thời gian cho thuật toán C
        self.algorithm_backtracking_label = Label(self.table_frame, text="Backtracking", font=("Courier New", 10))
        self.algorithm_backtracking_label.grid(row=3, column=0)

        self.map_type_backtracking_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_backtracking_label.grid(row=3, column=1)

        self.time_backtracking_label = Label(self.table_frame, text=self.time_for_backtracking, font=("Courier New", 10))
        self.time_backtracking_label.grid(row=3, column=2)

        # Hiển thị thời gian cho thuật toán D
        self.algorithm_brute_force_label = Label(self.table_frame, text="Brute Force", font=("Courier New", 10))
        self.algorithm_brute_force_label.grid(row=4, column=0)

        self.map_type_brute_force_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_brute_force_label.grid(row=4, column=1)

        self.time_brute_force_label = Label(self.table_frame, text=self.time_for_brute_force, font=("Courier New", 10))
        self.time_brute_force_label.grid(row=4, column=2)

        self.button_statistic.place_forget()

    def center_window(self, width, height):
        # Lấy chiều rộng và chiều cao của màn hình
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Tính toán vị trí x và y để đặt cửa sổ vào trung tâm
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Đặt vị trí của cửa sổ
        self.window.geometry(f"{width}x{height}+{x}+{y}")

# Hàm xử lý khi nhấn vào nút "EXIT"
    def exit_window(self):
        self.window.destroy()  # Đóng cửa sổ

    # Hàm xử lý sự kiện nút bắt đầu
    def show_levels(self):
        # Xóa vị trí nút START và EXIT
        self.exit_button.place_forget()
        self.start_button.place_forget()

        # Hiển thị các nút LEVEL
        distance = 0
        for button in self.level_buttons:
            button.place(x=370, y=200 + distance, width=300, height=80)
            distance += 90

    def show_maps(self, level):
        # Xóa các vị trí của nút level
        for button in self.level_buttons:
            button.place_forget()

        # Đọc danh sách các file map trong thư mục tương ứng với level
        map_folder = "maps/Level{}".format(level)
        maps = [f for f in os.listdir(map_folder) if os.path.isfile(os.path.join(map_folder, f))]
        
        # Hiển thị danh sách các map
        distance = 0
        for map_name in maps:
            map_button = Button(self.window, font=("Courier New", 16, "bold"), bg="#192847", fg="white", 
                                text=map_name, command=lambda  name=map_folder + "/" + map_name: self.select_map(name, map_name))
            map_button.place(x=370, y=200 + distance, width=350, height=50)
            distance += 60

            self.map_buttons.append(map_button)
        
    def select_map(self, name, map_name):
        self.file_name = name
        self.map_name = map_name
        for button in self.map_buttons:
            button.place_forget()

        # Xử lý việc chọn map
        print("Selected map:", self.file_name)
        self.size, self.grid = read_input_file(self.file_name)
        self.print_initial_map()

    def print_initial_map(self):
        # Kiểm tra
        for row in self.grid:
            for element in row:
                print(element, end="|") if (isinstance(element, int)) else print("_", end="|")
            print("")

        self.draw_board_game()

def main():
    #  Tạo cửa sổ bắt đầu
    window = Tk()

    # Gọi Class GUI
    Gui = GUI(window)

    # Gọi vòng lặp - vòng lặp này giúp cho cửa sổ được hiển thị liên tục
    window.mainloop()

# Hàm main sẽ được gọi khi chạy chương trình
if __name__ == "__main__":
    main()





