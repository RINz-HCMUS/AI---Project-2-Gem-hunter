from pysat.formula import CNF
from pysat.solvers import Solver
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

def solve_by_pysat(grid, size):
    num_r, num_c = size
    clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]

    cnf = CNF()
    for clause in clauses:
        cnf.extend(clause)

    with Solver(bootstrap_with=cnf) as solver:
        # Solve the SAT problem
        if solver.solve():
            # If satisfiable, get the satisfying assignment
            satisfying_assignment = solver.get_model()
            print('Formula is satisfiable')
            return satisfying_assignment
        else:
            # If unsatisfiable
            print('Formula is unsatisfiable')
            return None  # Or handle the unsatisfiable case accordingly

def ouput(list_result, grid, size):
    output = grid.copy()
    num_r, num_c = size
    for r in range(num_r):
        for c in range(num_c):
            if output[r][c] != '_':
                continue
            index = r * num_c + c
            if list_result[index] > 0:
                output[r][c] = 'T'
            else:
                output[r][c] = 'G'
    return output


size = 3,4
grid = [
    [3, '_', 2, '_'],
    ['_', '_', 2, '_'],
    ['_', 3, 1, '_']
]

num_r, num_c = size
clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]

print(clauses)

result = ouput(solve_by_pysat(grid,size), grid,size)
for row in result:
    print(row)

