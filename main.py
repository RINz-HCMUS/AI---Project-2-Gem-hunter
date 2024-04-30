from GUI import*
from OptimalAlgorithm import*
from PysatSupport import*
from Backtracking import*
from Brute_Force import*

def main():
    #  Create a window to start the game
    window = Tk()
    window.title("Gem Hunter")
    # Call the GUI class
    Gui = GUI(window)

    # Run the window loop to keep the window open
    window.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
