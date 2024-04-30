from itertools import combinations
from PysatSupport import*

def unit_propagation(clauses, assignment):
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses[0][0]
        assignment[abs(literal)] = literal > 0
        clauses = [c for c in clauses if literal not in c]
        unit_clauses = [c for c in clauses if len(c) == 1]
    return clauses, assignment

def get_decision_literal(assignment, unassigned_variables):
    for var in unassigned_variables:
        if var not in assignment and -var not in assignment:
            return var
    return None

def find_conflict_clause(clauses, assignment):
    for clause in clauses:
        satisfied = False
        for literal in clause:
            if abs(literal) in assignment and (literal > 0) == assignment[abs(literal)]:
                satisfied = True
                break
        if not satisfied:
            return clause
    return None

def analyze_conflict(clauses, conflict_clause, assignment):
    learned_clause = []
    for literal in conflict_clause:
        if abs(literal) not in assignment:
            learned_clause.append(literal)
    return learned_clause

def CDCL(clauses):
    assignment = {}  # Lưu trữ phân nhóm của biến (True/False)
    decision_stack = []  # Ngăn xếp quyết định
    unassigned_variables = set(abs(literal) for clause in clauses for literal in clause)
    
    while True:
        clauses, assignment = unit_propagation(clauses, assignment)
        decision_literal = get_decision_literal(assignment, unassigned_variables)
        if decision_literal is None:
            return assignment  # Tất cả các biến đã được gán, nên trả về phân nhóm
        
        decision_stack.append((decision_literal, assignment.copy()))
        assignment[decision_literal] = True  # Thử gán biến là True
        unassigned_variables.remove(decision_literal)
        
        while True:
            clauses, assignment = unit_propagation(clauses, assignment)
            conflict_clause = find_conflict_clause(clauses, assignment)
            if conflict_clause is None:
                break
            learned_clause = analyze_conflict(clauses, conflict_clause, assignment)
            if not learned_clause:
                return None  # Không tìm thấy lời giải, bài toán không thể giải quyết
            clauses.append(learned_clause)
            assignment = {abs(literal): None for literal in learned_clause}
        
        assignment[decision_literal] = False  # Thử gán biến là False
        unassigned_variables.remove(decision_literal)

def Optimal_Algorithm_Solution(grid, size):
    num_r, num_c = size
    clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]
    flattened_clauses = [clause for sublist in clauses for clause in sublist]
    assignment = CDCL(flattened_clauses)
    if assignment is not None:
        return ouput_for_pysat(assignment, grid, size)
    else:
        print("No solution found.")
        return None

