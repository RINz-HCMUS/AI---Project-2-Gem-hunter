from itertools import combinations
from PysatSupport import*

def output_for_algorithm_optimal(result, flat_grid, size):
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
                        row.append('G')
            output_grid.append(row)
    return output_grid
#  Thuật giải áp dụng backtracking thông thường
def solve_with_optimal_algorithm(grid, size):
    num_r, num_c = size
    clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]
    flat_grid = [item for sublist in grid for item in sublist]
    num_variables = num_r * num_c

    # Flatten the list of clauses
    clauses = [clause for sublist in clauses for clause in sublist]
    result = solve_SAT(num_variables, clauses)
    return result, flat_grid

def solve_SAT(num_variables, clauses):
    variables = set(abs(literal) for clause in clauses for literal in clause)
    variables = list(variables)
    assignment = {}

    return SAT_solver(variables, clauses, assignment)

def SAT_solver(variables, clauses, assignment):
    if not clauses:
        return assignment
    
    while clauses:
        unassigned_literal = None
        for clause in clauses:
            for literal in clause:
                if literal not in assignment and -literal not in assignment:
                    unassigned_literal = literal
                    break
            if unassigned_literal is not None:
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
    new_clauses = set()
    for clause in clauses:
        if literal in clause:
            continue
        new_clause = frozenset(l for l in clause if -literal != l)
        if new_clause:
            new_clauses.add(new_clause)
    return new_clauses



# Áp dung Thuật toán Tối Ưu để giải bài toán SAT
def Optimal_Algorithm_Solution(grid, size):
    # Giải bài toán
    result, flat_grid = solve_with_optimal_algorithm(grid, size)

    # Xuất kết quả
    if result is not None:
        return output_for_algorithm_optimal(result, flat_grid, size)   
    else:
        print("No solution found.")
        return None

