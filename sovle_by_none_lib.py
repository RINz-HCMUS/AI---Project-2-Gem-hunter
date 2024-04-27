from itertools import combinations

def convert_to_flatten(pos, size):
    num_r, num_c = size
    r, c = pos
    return (r*num_c + c + 1)

def convert_to_2D(flat, size):
    num_r, num_c = size
    c = (flat-1) % num_c
    r = (flat-1) // num_c
    return r,c

def generate_around(pos):
    r, c = pos
    for i in range(-1, 2):
        for j in range(-1, 2):
            yield r + i, c + j

def is_valid(pos, grid, size):
    num_r, num_c = size
    r, c = pos 
    return 0 <= r < num_r and 0 <= c < num_c and grid[r][c] == '_'  

def list_combination(n, k):
    comb_list = list(combinations(range(1, n + 1), k))
    return comb_list

def generate_CNF(pos, grid, size):
    if grid[pos[0]][pos[1]] == '_':
        return []
    
    list_cells = []
    for new_pos in generate_around(pos):
        if is_valid(new_pos, grid, size):
            list_cells.append(convert_to_flatten(new_pos, size))
    
    number = grid[pos[0]][pos[1]]
    num_valid = len(list_cells)
    clauses = []
    
    first_comb = list_combination(num_valid, number + 1)
    
    for comb in first_comb:
        clause = []
        for index in comb:
            clause.append(-list_cells[index - 1])
        clauses.append(clause)
    
    second_comb = list_combination(num_valid, num_valid - number + 1)
    for comb in second_comb:
        clause = []
        for index in comb:
            clause.append(list_cells[index - 1])
        clauses.append(clause)
    
    return clauses


#  Thuật giải áp dụng backtracking thông thường
def solve_SAT(num_variables, clauses):
    variables = set(abs(literal) for clause in clauses for literal in clause)
    variables = list(variables)
    assignment = {}

    return SAT_solver(variables, clauses, assignment)

def solve(grid, size):
    num_r, num_c = size
    clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]
    flat_grid = [item for sublist in grid for item in sublist]
    num_variables = num_r * num_c

    # Flatten the list of clauses
    clauses = [clause for sublist in clauses for clause in sublist]
    result = solve_SAT(num_variables, clauses)
    return result, flat_grid


def SAT_solver(variables, clauses, assignment):
    if not clauses:
        return assignment
    
    for clause in clauses:
        unassigned_literal = None
        for literal in clause:
            if literal not in assignment and -literal not in assignment:
                unassigned_literal = literal
                break
        
        if unassigned_literal is None:
            return None
        
        assignment[abs(unassigned_literal)] = unassigned_literal > 0
        new_clauses = simplify(clauses, unassigned_literal)
        result = SAT_solver(variables, new_clauses, assignment)
        if result is not None:
            return result
        
        assignment.pop(abs(unassigned_literal))
        assignment[abs(unassigned_literal)] = not (unassigned_literal > 0)
        new_clauses = simplify(clauses, -unassigned_literal)
        result = SAT_solver(variables, new_clauses, assignment)
        if result is not None:
            return result
        
        assignment.pop(abs(unassigned_literal))
        return None

def simplify(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue
        new_clause = [l for l in clause if -literal != l]
        if new_clause:
            new_clauses.append(new_clause)
    return new_clauses

def output(result, flat_grid, size):
    num_r, num_c = size
    output_grid = []
    if result is not None:
        for i in range(num_r):
            row = []
            for j in range(num_c):
                flat_index = i * num_c + j
                if flat_grid[flat_index] != '_':
                    row.append(flat_grid[flat_index])
                else:
                    variable = flat_index + 1
                    if variable in result:
                        row.append('T' if result[variable] else 'G')
                    else:
                        row.append('_')
            output_grid.append(row)
    return output_grid



size = 3, 4
grid = [
    [2, '_', 2, '_'],
    ['_', '_', 2, '_'],
    ['_', 3, 1, '_']
]

result, flat_grid = solve(grid, size)
if result is not None:
    output_grid = output(result, flat_grid, size)
    for row in output_grid:
        print(row)
else:
    print("No solution found.")
