from GUI import*
from OptimalAlgorithm import*
from PysatSupport import*
from Backtracking import*
from Brute_Force import*

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
