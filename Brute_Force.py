from PysatSupport import*

# Giải map
def Brute_Force_Solution(board, size):
    rows, cols = size
    solution = board.copy()
    while True:
        flag = False # Kiểm tra xem có thay đổi không
        non_zero_count = 0 

        # Tìm ô có số bom xung quanh lớn nhất
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == '_':
                    count = count_adjacent_bombs(size, board, r, c)
                    if count > non_zero_count:
                        non_zero_count = count
                        max_r, max_c = r, c

        if non_zero_count == 0:
            break
        
        board[max_r][max_c] = 'T'
        solution[max_r][max_c] = 'T'
        
        decrement_adjacent_bombs(size, board, max_r, max_c)
        flag = True

        if not flag:
            break
    
    # Tạo các ô Gems
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == '_':
                solution[r][c] = 'G'
    return solution

# Đếm số bom xung quanh ô (r, c)
def count_adjacent_bombs(size, board ,r, c):
    rows, cols = size
    
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and isinstance(board[nr][nc], int):
                if board[nr][nc] == '0':
                    return 0
                else:
                    count += int(board[nr][nc])
    return count

# Giảm số bom xung quanh ô (r, c)
def decrement_adjacent_bombs(size, board, r, c):
    rows, cols = size

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and isinstance(board[nr][nc], int):
                board[nr][nc] = str(max(0, int(board[nr][nc]) - 1))

