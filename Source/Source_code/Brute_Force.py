def Brute_Force_Solution(grid, size):
    """
    Solves the Minesweeper game using a brute force approach.

    Args:
        grid (list of lists): The grid representing the Minesweeper game.
        size (tuple): A tuple containing the number of rows and columns in the grid.

    Returns:
        list of lists: The solution grid with 'T' for traps and 'G' for gems.
    """
    rows, cols = size
    solution = [[cell for cell in row] for row in grid]

    while True:
        flag = False
        non_zero_count = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '_':
                    count = count_adjacent_bombs(r, c, grid, size)
                    if count > non_zero_count:
                        non_zero_count = count
                        max_r, max_c = r, c

        if non_zero_count == 0:
            break

        grid[max_r][max_c] = 'T'
        solution[max_r][max_c] = 'T'

        decrement_adjacent_bombs(max_r, max_c, grid, size)
        flag = True

        if not flag:
            break

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '_':
                solution[r][c] = 'G'

    return solution

def count_adjacent_bombs(r, c, grid, size):
    """
    Counts the number of adjacent bombs around a given cell in the grid.

    Args:
        r (int): The row index of the cell.
        c (int): The column index of the cell.
        grid (list of lists): The grid representing the Minesweeper game.
        size (tuple): A tuple containing the number of rows and columns in the grid.

    Returns:
        int: The count of adjacent bombs.
    """
    rows, cols = size
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                cell = grid[nr][nc]
                if isinstance(cell, str) and cell.isdigit():
                    if cell == '0':
                        return 0
                    else:
                        count += int(cell)
                elif isinstance(cell, int) and cell != 0:
                    count += cell
    return count

def decrement_adjacent_bombs(r, c, grid, size):
    """
    Decrements the count of adjacent bombs around a given cell in the grid.

    Args:
        r (int): The row index of the cell.
        c (int): The column index of the cell.
        grid (list of lists): The grid representing the Minesweeper game.
        size (tuple): A tuple containing the number of rows and columns in the grid.
    """
    rows, cols = size
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and isinstance(grid[nr][nc], int):
                grid[nr][nc] = max(0, grid[nr][nc] - 1)
