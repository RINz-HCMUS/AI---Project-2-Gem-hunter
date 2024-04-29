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

# Giải quyết SAT bằng thuật toán DPLL - một phiên bản của backtracking
def Backtracking_Solution(grid, size):
    rows, cols = size

    # Generate CNF
    clauses = [generate_CNF((r, c), grid, size) for r in range(rows) for c in range(cols)]
    formula = []

    # Create Fomula
    for clause in clauses:
        for item in clause:
            formula.append(item)

    # Solve by using dpll
    satisfiable, assignments = dpll(formula)
    sorted_assignment = sorted(assignments, key=abs)
    if satisfiable:         
            # Trả về kết quả nếu giải thành công
            return output_for_backtracking(sorted_assignment, grid, size)
    else:
        # Hiển thị thông báo giải không thành công
        print("Unsatisfiable")
        return None



