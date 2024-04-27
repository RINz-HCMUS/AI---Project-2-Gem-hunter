from pysat.formula import CNF
from pysat.solvers import Solver
from itertools import combinations

import copy

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
    # No number to work with => no clause
    if grid[pos[0]][pos[1]] == '_':
        return []

    # If grid[pos] is a number
    list_cells = []
    for new_pos in generate_around(pos):
        if is_valid(new_pos, grid, size):
            list_cells.append(convert_to_flatten(new_pos, size))

    number = grid[pos[0]][pos[1]]
    num_valid = len(list_cells)
    clauses = []

    # Cell that contains gem/trap
    first_comb = list_combination(num_valid, number + 1)

    for comb in first_comb:
        clause = []
        for index in comb:
            clause.append(-list_cells[index - 1])
        clauses.append(clause)

    # Cell that does not contain gem/trap
    second_comb = list_combination(num_valid, num_valid - number + 1)
    for comb in second_comb:
        clause = []
        for index in comb:
            clause.append(list_cells[index - 1])
        clauses.append(clause)

    return clauses

def output_map(list_result, grid, size):
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

# ---------------------------------------------------------------------------------------------------------------------------------------------------

def output_map_v2(list_result, grid, size):
    output = grid.copy()
    num_r, num_c = size
    for r in range(num_r):
        for c in range(num_c):
            if output[r][c] != '_':
                continue
            index = r * num_c + c + 1
            for item in list_result:
                if abs(item) == index:
                    if item > 0:
                        output[r][c] = 'T'
                    else:
                        output[r][c] = 'G'
                    break

    for r in range(num_r):
        for c in range(num_c):
            if output[r][c] == '_':
                output[r][c] = 'G'

    return output

def unit_propagate(formula, assignments):
    while True:
        unit_clause = None
        for clause in formula:
            unassigned_literals = [literal for literal in clause if literal not in assignments and -literal not in assignments]
            if len(unassigned_literals) == 1:
                unit_clause = unassigned_literals[0]
                break
        if unit_clause is None:
            break
        assignments.add(unit_clause)
        formula = [c for c in formula if unit_clause not in c]
    return formula, assignments

def dpll(formula, assignments=set()):
    formula, assignments = unit_propagate(formula, assignments)
    if not formula:
        return True, assignments  # Formula is satisfied
    if any(not clause for clause in formula):
        return False, None  # Formula is unsatisfiable

    # Choose an unassigned variable
    unassigned_literals = {literal for clause in formula for literal in clause} - assignments
    literal = unassigned_literals.pop() if unassigned_literals else None

    # Try assigning the variable as true and false recursively
    result, final_assignments = dpll([clause for clause in formula if literal not in clause], assignments.union({literal}))
    if result:
        return True, final_assignments
    else:
        return dpll([clause for clause in formula if -literal not in clause], assignments.union({-literal}))

# ---------------------------------------------------------------------------------------------------------------------------------------------------

def read_data_into_2d_list(file_path):
    try:
        # Open the file for reading
        with open(file_path, 'r') as file:
            # Read the first line to get dimensions
            dimensions = file.readline().strip().split()
            num_rows, num_cols = map(int, dimensions)

            # Initialize an empty 2D list
            data_2d_list = []

            # Read the remaining lines to get the data
            for _ in range(num_rows):
                # Read each line, strip any leading/trailing whitespace, and split by commas
                values = file.readline().strip().split(',')

                # Convert string values to integers if needed
                row = [int(value) if value.isdigit() else value for value in values]

                # Append the row to the 2D list
                data_2d_list.append(row)

    except FileNotFoundError:
        print("File not found.")
        return None

    return data_2d_list, (num_rows, num_cols)

# ---------------------------------------------------------------------------------------------------------------------------------------------------

def test_all():
    size = 3,4
    grid = [
        [3, '_', 2, '_'],
        ['_', '_', 2, '_'],
        ['_', 3, 1, '_']
    ]

    # Input from .txt file
    # grid, size = read_data_into_2d_list("map/10x10.txt")
    print("Map: ")
    for row in grid:
        print(row)
    num_r, num_c = size
    grid_1 = copy.deepcopy(grid)
    grid_2 = copy.deepcopy(grid)


    # Use Pysat to solve CNF
    print("Solve by Pysat")
    res = output_map(solve_by_pysat(grid_1, size), grid_1, size)
    for re in res:
        print(re)

    # Generate CNF
    clauses = [generate_CNF((r, c), grid_2, size) for r in range(num_r) for c in range(num_c)]
    formula = []

    for clause in clauses:
        for item in clause:
            formula.append(item)
    # print(formula)

    # Solve by using dpll
    satisfiable, assignments = dpll(formula)
    sorted_assignment = sorted(assignments, key=abs)
    if satisfiable:
            print("Solve by DPLL")
            print("Formula is satisfiable")
            # print("Satisfying Assignment:", sorted_assignment)
            res_2 = output_map_v2(sorted_assignment, grid_2, size)
            for re in res_2:
                print(re)
    else:
        print("Unsatisfiable")


    if res == res_2:
        print("Same")
    else:
        print("Not same")

def test_pysat():
    grid, size = read_data_into_2d_list("map/10x10.txt")
    res = output_map(solve_by_pysat(grid, size), grid, size)
    for r in res:
        print(r)

test_all()



# def test_dpll():
#     # Example usage
#     if __name__ == "__main__":
#         file_path = "map/10x10.txt"
#         data, size = read_data_into_2d_list(file_path)
#         # Example CNF formula: (a ∨ b) ∧ (¬a ∨ b ∨ ¬c) ∧ (¬b ∨ c)
#         # formula = [[2], [5], [6], [-2, -4, -6], [-2, -4, -8], [-2, -6, -8], [-4, -6, -8], [2, 4, 6], [2, 4, 8], [2, 6, 8], [4, 6, 8], [-2, -4, -6], [-2, -4, -8], [-2, -4, -12], [-2, -6, -8], [-2, -6, -12], [-2, -8, -12], [-4, -6, -8], [-4, -6, -12], [-4, -8, -12], [-6, -8, -12], [2, 4, 6, 8], [2, 4, 6, 12], [2, 4, 8, 12], [2, 6, 8, 12], [4, 6, 8, 12], [5], [6], [9], [-6, -8], [-6, -12], [-8, -12], [6, 8, 12]]
#         # formula = [[-1, -2], [-1, -7], [-2, -7], [1, 2, 7], [-1, -2], [-1, -3], [-1, -6], [-1, -7], [-1, -9], [-2, -3], [-2, -6], [-2, -7], [-2, -9], [-3, -6], [-3, -7], [-3, -9], [-6, -7], [-6, -9], [-7, -9], [1, 2, 3, 6, 7, 9], [-6, -7], [-6, -9], [-7, -9], [6, 7, 9]]
#         formula = [[12], [12], [12], [15], [15], [15], [18], [18], [-10, -18], [-10, -20], [-18, -20], [10, 18, 20], [12], [12], [15], [15], [18], [-10, 
# -18], [-10, -20], [-10, -30], [-18, -20], [-18, -30], [-20, -30], [10, 18, 20, 30], [-12, -31], [-12, -32], [-31, -32], [12, 31, 32], [-12, -31], [-12, -32], [-31, -32], [12, 31, 32], [-12, -32, -34], [12, 32], [12, 34], [32, 34], [15], [34], [15], [34], [15], [37], [18], [37], [-18, -37, -39], [18, 37], [18, 39], [37, 39], [-18, -20], [-18, -30], [-18, -39], [-18, -40], [-20, -30], [-20, -39], [-20, -40], [-30, -39], [-30, -40], [-39, -40], [18, 20, 30, 39, 40], [-32, -34], [32, 34], [34], [37], [-37, -39], [-37, -49], [-39, -49], [37, 39, 49], [-31, -32], [-31, -41], [-31, -51], [-31, -53], [-32, -41], [-32, -51], [-32, -53], [-41, -51], [-41, -53], [-51, -53], [31, 32, 41, 51, 53], [-32, -34, -53], [32, 34], [32, 53], [34, 53], [34], [53], [34], [56], [37], [56], [37], [56], [-37, -39], [-37, -49], [-37, -59], [-39, -49], [-39, -59], [-49, -59], [37, 39, 49, 59], [-41, -51], [-41, -53], [-41, -61], [-51, -53], [-51, -61], [-53, 
# -61], [41, 51, 53, 61], [53], [56], [56], [67], [-49, -59], [-49, -67], [-49, -69], [-59, -67], [-59, -69], [-67, -69], [49, 59, 67, 69], [-51, -53], [-51, -61], [-51, -71], [-53, -61], [-53, -71], [-61, -71], [51, 53, 61, 71], [53], [53], [75], [56], [75], [56], [67], 
# [75], [-59, -67], [-59, -69], [-67, -69], [59, 67, 69], [-61, -71], [-61, -81], [-61, -83], [-71, -81], [-71, -83], [-81, -83], [61, 71, 81, 83], [83], [75], [83], [67], [75], [67], [-67, -69, -89], [67, 69], [67, 89], [69, 89], [-69, -70], [-69, -89], [-70, -89], [69, 
# 70, 89], [-69, -70], [-69, -89], [-70, -89], [69, 70, 89], [-71, -81], [-71, -83], [-71, -91], [-81, -83], [-81, -91], [-83, -91], [71, 81, 83, 91], [-75, -83, -95], [75, 83], [75, 95], [83, 95], [-75, -95], [75, 95], [-75, -95, -97], [75, 95], [75, 97], [95, 97], [97], [89], [97], [89], [-81, -83], [-81, -91], [-83, -91], [81, 83, 91], [83], [-83, -95], [83, 95], [-95, -97], [95, 97], [89], [97], [89], [89]]
#         satisfiable, assignments = dpll(formula)
#         sorted_list = sorted(assignments, key=abs)
#         if satisfiable:
#             print("Satisfiable")
#             print("Satisfying Assignment:", sorted_list)
#         else:
#             print("Unsatisfiable")

#         res = output_map_v2(sorted_list, data, size)
#         for r in res:
#             print(r)