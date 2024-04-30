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

# Thuật toán áp dụng CDCL
def solve_SAT_CDCL(variables, clauses):
    model = {}
    return CDCL(variables, clauses, model)

def CDCL(variables, clauses, model):
    if not clauses:
        return model
    
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses[0]
        literal = next(iter(unit))
        model[abs(literal)] = literal > 0
        new_clauses = simplify(clauses, literal)
        result = CDCL(variables, new_clauses, model)
        if result is not None:
            return result
        model.pop(abs(literal))
        new_clauses = simplify(clauses, -literal)
        result = CDCL(variables, new_clauses, model)
        if result is not None:
            return result
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

def Optimal_Algorithm_Solution_CDCL(grid, size):
    num_r, num_c = size
    clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]
    flat_grid = [item for sublist in grid for item in sublist]
    num_variables = num_r * num_c
    clauses = [clause for sublist in clauses for clause in sublist]

    result = solve_SAT_CDCL(range(1, num_variables + 1), clauses)
    return output_for_algorithm_optimal(result, flat_grid, size) if result is not None else None
