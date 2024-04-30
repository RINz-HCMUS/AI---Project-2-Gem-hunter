def Brute_Force_Solution_2(grid, size):
    rows, cols = size
    Grid = [[cell for cell in row] for row in grid]
    first_unkown = (0, 0)
    for r in range(rows):
        for c in range(cols):
            if Grid[r][c] == '_':
                first_unkown = (r, c)
                break

    solution = generate_solution(Grid, size, first_unkown, True)
    if solution is not None and check_solution(solution, size):
        print("Solution found")
        for row in solution:
            print(row)
        return solution
    
    solution = generate_solution(Grid, size, first_unkown, False)
    if solution is not None and check_solution(solution, size):
        print("Solution found")
        for row in solution:
            print(row)
        return solution
    print("Non solution found")
    return None


def generate_solution(grid, size, first_unkown, state):
    #print("generate_solution")
    rows, cols = size
    Grid = [[cell for cell in row] for row in grid]
    r, c = first_unkown
    Grid[r][c] = 'G' if state else 'T'

    # Tìm ô chưa xét tiếp theo
    next_unknown = None
    for i in range(rows):
        for j in range(cols):
            if Grid[i][j] == '_':
                next_unknown = (i, j)
                break
        if next_unknown:
            break

    # Nếu không còn ô chưa xét, trả về lưới hiện tại
    if not next_unknown:
        return Grid

    # Tiếp tục đệ quy
    solution = generate_solution(Grid, size, next_unknown, True)
    if solution is not None and check_solution(solution, size):
        return solution
    
    solution = generate_solution(Grid, size, next_unknown, False)
    if solution is not None and check_solution(solution, size):
        return solution
    
    
    return None


# Check if the solution is valid
def check_solution(grid, size):
    rows, cols = size
    Grid = [[cell for cell in row] for row in grid]
    for r in range(rows):
        for c in range(cols):
            if Grid[r][c] == '_':
                return False
            if Grid[r][c] == 'T' or Grid[r][c] == 'G':
                continue
            else:
                count = count_adjacent_traps(r, c, Grid, size)
                if count != int(Grid[r][c]):
                    return False
                
    return True

# Count the number of adjacent traps around a given cell (r, c)
def count_adjacent_traps(r, c, grid, size):
    rows, cols = size
    Grid = [[cell for cell in row] for row in grid]
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and Grid[nr][nc] == 'T':
                count += 1
    return count