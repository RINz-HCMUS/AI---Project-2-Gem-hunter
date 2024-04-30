from PysatSupport import*

def output_for_backtracking(list_result, grid, size):
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

# Giải quyết SAT bằng thuật toán DPLL - một phiên bản của backtracking
def dpll_iterative(formula):
    stack = [(formula, set())]
    while stack:
        formula, assignments = stack.pop()
        formula, assignments = unit_propagate(formula, assignments)
        if any(not clause for clause in formula):
            continue
        if not formula:
            return True, assignments
        unassigned_literals = set()
        for clause in formula:
            unassigned_literals.update(literal for literal in clause if literal not in assignments and -literal not in assignments)
        if not unassigned_literals:
            continue
        literal = unassigned_literals.pop()
        stack.append(([clause for clause in formula if literal not in clause], assignments.union({literal})))
        stack.append(([clause for clause in formula if -literal not in clause], assignments.union({-literal})))
    return False, None

def Backtracking_Solution(grid, size):
    rows, cols = size

    # Generate CNF
    clauses = [generate_CNF((r, c), grid, size) for r in range(rows) for c in range(cols)]
    formula = []
    for clause in clauses:
        for item in clause:
            formula.append(item)

    # Solve by using iterative DPLL
    satisfiable, assignments = dpll_iterative(formula)
    if satisfiable and assignments is not None:
        sorted_assignment = sorted(assignments, key=abs)
        return output_for_backtracking(sorted_assignment, grid, size)
    else:
        print("Unsatisfiable")
        return None





