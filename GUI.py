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

        # Set window size
        window_width = 1080
        window_height = 720
        self.window.geometry(f"{window_width}x{window_height}")

        # Call center_window function to place the window in the center of the screen
        self.center_window(window_width, window_height)

        # Set attributes to stay on top of other windows
        self.window.attributes("-topmost", TRUE)

        # Load images for background
        self.image_bg = PhotoImage(file="photo/back_ground5.png")
        self.image_moon = PhotoImage(file="photo/moon.png")
        self.image_earth = PhotoImage(file="photo/earth.png")
        self.image_bg_board = PhotoImage(file="photo/main_bg.png")

        # Create label to display background
        self.back_ground = Label(self.window, image=self.image_bg)

        # Set size and position to display the background
        self.back_ground.place(x=0, y=0, relheight=1, relwidth=1)

        # Draw start and exit buttons
        self.start_button = Button(self.window, font=("Courier New", 40, "bold"), text="START",bg="#192847", fg="white", command=self.show_levels)
        self.start_button.place(x=370, y=270, width=300, height=100)

        # Exit button
        self.exit_button = Button(self.window, font=("Courier New", 40, "bold"), text="EXIT", bg="#192847", fg="white", command=self.exit_window)
        self.exit_button.place(x=370, y=380, width=300, height=100)

        # Create lists
        self.level_buttons = []
        self.map_buttons = []
        self.grid = []
        self.box_maps = []
        self.size = 0
        self.transfer_speed = 5
        self.size_cell = 0

        # Variable to track algorithm running state
        self.is_running = False
        self.start_time = 0

        # Save statistics for each algorithm
        self.time_for_optimal_algorithm = 0
        self.time_for_pysat_lib = 0
        self.time_for_brute_force = 0
        self.time_for_backtracking = 0


        for i in range(5):
            level_button = Button(self.window, font=("Courier New", 35, "bold"), text="LEVEL {}".format(i+1),bg="#192847", fg="white", command=lambda level=i+1: self.show_maps(level))
            self.level_buttons.append(level_button)

    def set_background_board(self):
        # Create label to display background
        self.back_ground_board = Label(self.window, image=self.image_bg_board)
        self.back_ground_moon = Label(self.window, image=self.image_moon, bg="#192847")
        self.back_ground_earth = Label(self.window, image=self.image_earth, bg="#192847")

        # Set size and position to display the background
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

                # Create label for each square with gray background and black border
                button = Button(self.window, font=("Courier New", 10, "bold"), text=str(self.grid[i][j]), bg=color, fg="white")
                button.place(x=self.start_x + self.size_cell * j, y=  self.start_y + self.size_cell * i, width=self.size_cell, height=self.size_cell)
                self.box_maps.append(button)

        # Draw solve button
        self.button_solve = Button(self.window, font=("Courier New", 20, "bold"), text="SOLVE", bg="grey", fg="white", command=self.board_solved)
        self.button_solve.place(x=self.width//2 - 50, y=self.height - 80, width=100, height=50)

        self.button_menu = Button(self.window, font=("Courier New", 20, "bold"), text="MENU", bg="grey", fg="white", command=self.menu_button)
        self.button_menu.pack(padx=5, pady=5)

        # Display timer
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
        self.time_for_pysat_lib = time_str # Save processing time

    def board_solved(self):
        # Delete old label and button
        self.button_solve.place_forget()
        for element in self.box_maps:
            element.place_forget()
        self.box_maps.clear

        # Get information
        row, col = self.size

        # Solve SAT with Pysat Library
        self.start_time = datetime.now()  # Save the start time
        self.output_grid = Optimal_Algorithm_Solution(self.grid, self.size)
        self.update_timer()

        # Write the result to output file
        self.write_to_file()
        
        # Print the result
        if self.output_grid is not None:
            for i in range(row):
                for j in range(col):
                    # Default color
                    color_text = "white"
                    color = "#506465"

                    # Different color for Gem and Trap squares
                    if(self.output_grid[i][j] == "G") : 
                        color, color_text = "#5FCAD8", "#547FAF"
                    elif(self.output_grid[i][j] == "T") : 
                        color = "#EF6C62"

                    # Create label for each square
                    button = Button(self.window, font=("Courier New", 10, "bold"), text=str(self.output_grid[i][j]), bg=color, fg=color_text)
                    button.place(x=self.start_x + self.size_cell * j, y= self.start_y + self.size_cell * i, width=self.size_cell, height=self.size_cell)
                    self.box_maps.append(button)

        # If no solution found
        else :
            print("No solution found is returned by Brute_Force_Solution.")

        # Run other algorithms to compare the solving time
        # Brute_Force Algorithm
        size, grid = read_input_file(self.file_name)
        self.start_time = datetime.now()
        Brute_Force_Solution(grid.copy(), size)
        elapsed_time = datetime.now() - self.start_time 
        self.time_for_brute_force = self.format_timer(elapsed_time)

        # Backtracking DPLL Algorithm
        size, grid = read_input_file(self.file_name)
        self.start_time = datetime.now()
        Backtracking_Solution(grid.copy(), size)
        elapsed_time = datetime.now() - self.start_time 
        self.time_for_backtracking = self.format_timer(elapsed_time)

        # Optimal Algorithm - Backtracking CDCL
        size, grid = read_input_file(self.file_name)
        self.start_time = datetime.now()
        Optimal_Algorithm_Solution(grid.copy(), size)
        elapsed_time = datetime.now() - self.start_time 
        self.time_for_optimal_algorithm = self.format_timer(elapsed_time)

        # Create a button to display the statistic result
        self.button_statistic = Button(self.window, font=("Courier New", 20, "bold"), text="STATISTIC", bg="#97D76D", fg="white", command=self.statistic)
        self.button_statistic.place(x=self.width//2 - 100, y=self.height - 80, width=200, height=60)
    
    def write_to_file(self):
        # Create a new directory named "output" if it doesn't exist yet
        output_directory = "output"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Write the content of the output grid to a file in the "output" directory
        output_file_path = os.path.join(output_directory, self.map_name)
        with open(output_file_path, "w") as file:
            for row in self.output_grid:
                # Convert each element of row to a string and then join them together
                str_row = [str(item) for item in row]
                file.write(" ".join(str_row) + "\n")

        print(f"Output file has been written to the directory {output_directory}")

    def statistic(self):
        self.table_frame = Frame(self.window, width=300, height=400)
        self.table_frame.pack(padx=50, pady=50)

        # Name for columns
        self.algorithm_label = Label(self.table_frame, text="Algorithm", font=("Courier New", 10))
        self.algorithm_label.grid(row=0, column=0)

        self.map_type_label = Label(self.table_frame, text="Map Type", font=("Courier New", 10))
        self.map_type_label.grid(row=0, column=1)

        self.processing_time_label = Label(self.table_frame, text="Processing Time", font=("Courier New", 10))
        self.processing_time_label.grid(row=0, column=2)

        # Display solving time of Pysat Algorithm
        self.algorithm_pysat_label = Label(self.table_frame, text="Pysat Library", font=("Courier New", 10))
        self.algorithm_pysat_label.grid(row=1, column=0)

        self.map_type_pysat_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_pysat_label.grid(row=1, column=1)

        self.time_pysat_label = Label(self.table_frame, text=self.time_for_pysat_lib, font=("Courier New", 10))
        self.time_pysat_label.grid(row=1, column=2)

        # Display solving time of Optimal Algorithm
        self.algorithm_optimal_label = Label(self.table_frame, text="Optimal", font=("Courier New", 10))
        self.algorithm_optimal_label.grid(row=2, column=0)

        self.map_type_optimal_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_optimal_label.grid(row=2, column=1)

        self.time_optimal_label = Label(self.table_frame, text=self.time_for_optimal_algorithm, font=("Courier New", 10))
        self.time_optimal_label.grid(row=2, column=2)

        # Display solving time of Backtracking
        self.algorithm_backtracking_label = Label(self.table_frame, text="Backtracking", font=("Courier New", 10))
        self.algorithm_backtracking_label.grid(row=3, column=0)

        self.map_type_backtracking_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_backtracking_label.grid(row=3, column=1)

        self.time_backtracking_label = Label(self.table_frame, text=self.time_for_backtracking, font=("Courier New", 10))
        self.time_backtracking_label.grid(row=3, column=2)

        # Display solving time of Brute-Force
        self.algorithm_brute_force_label = Label(self.table_frame, text="Brute Force", font=("Courier New", 10))
        self.algorithm_brute_force_label.grid(row=4, column=0)

        self.map_type_brute_force_label = Label(self.table_frame, text=self.map_name, font=("Courier New", 10))
        self.map_type_brute_force_label.grid(row=4, column=1)

        self.time_brute_force_label = Label(self.table_frame, text=self.time_for_brute_force, font=("Courier New", 10))
        self.time_brute_force_label.grid(row=4, column=2)

        self.button_statistic.place_forget()

    def center_window(self, width, height):
        # Get screen information
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate the position to place window
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Place window to correct position
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    # Function to handle "EXIT" button click
    def exit_window(self):
        self.window.destroy()  # Close the window

    # Function to handle "START" button click
    def show_levels(self):
        # Remove position of START and EXIT buttons
        self.exit_button.place_forget()
        self.start_button.place_forget()

        # Display LEVEL buttons
        distance = 0
        for button in self.level_buttons:
            button.place(x=370, y=200 + distance, width=300, height=80)
            distance += 90

    def show_maps(self, level):
        # Remove position of LEVEL buttons
        for button in self.level_buttons:
            button.place_forget()

        # Read list of map files in the corresponding level folder
        map_folder = "maps/Level{}".format(level)
        maps = [f for f in os.listdir(map_folder) if os.path.isfile(os.path.join(map_folder, f))]
        
        # Display list of maps
        distance = 0
        for map_name in maps:
            map_name_without_extension = map_name.split('.')[0]
            map_button = Button(self.window, font=("Courier New", 16, "bold"), bg="#192847", fg="white", 
                                text=map_name_without_extension, command=lambda  name=map_folder + "/" + map_name: self.select_map(name, map_name))
            map_button.place(x=370, y=200 + distance, width=350, height=50)
            distance += 60

            self.map_buttons.append(map_button)
        
    def select_map(self, name, map_name):
        self.file_name = name
        self.map_name = map_name
        for button in self.map_buttons:
            button.place_forget()

        # Process map selection
        print("Selected map:", self.file_name)
        self.size, self.grid = read_input_file(self.file_name)
        self.print_initial_map()

    def print_initial_map(self):
        # Check
        for row in self.grid:
            for element in row:
                print(element, end="|") if (isinstance(element, int)) else print("_", end="|")
            print("")

        self.draw_board_game()

def main():
    # Create start window
    window = Tk()

    # Call GUI class
    Gui = GUI(window)

    # Main loop - this loop keeps the window displayed continuously
    window.mainloop()

# Main function will be called when running the program
if __name__ == "__main__":
    main()
