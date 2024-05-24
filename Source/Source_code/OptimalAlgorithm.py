from PysatSupport import*

# Function to generate the output grid based on the optimal algorithm result
def output_for_algorithm_optimal(result, flat_grid, size):
    """
    Generate the output grid based on the optimal algorithm result.

    Args:
        result (dict): The satisfying assignment.
        flat_grid (list): The flattened grid representing the Minesweeper game.
        size (tuple): The size of the grid.

    Returns:
        list of lists: The solution grid.
    """
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

# Function to perform SAT solving using backtracking
def SAT_solver(variables, clauses, assignment):
    """
    Perform SAT solving using backtracking.

    Args:
        variables (list): The list of variables.
        clauses (list of lists): The CNF clauses.
        assignment (dict): The current assignment.

    Returns:
        dict or None: The satisfying assignment if found, None otherwise.
    """
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

# Function to simplify clauses based on assigned literal
def simplify(clauses, literal):
    """
    Simplify clauses based on assigned literal.

    Args:
        clauses (list of lists): The CNF clauses.
        literal (int): The assigned literal.

    Returns:
        set: The simplified clauses.
    """
    new_clauses = set()
    for clause in clauses:
        if literal in clause:
            continue
        new_clause = frozenset(l for l in clause if -literal != l)
        if new_clause:
            new_clauses.add(new_clause)
    return new_clauses

# Function to calculate Jeroslow-Wang heuristic values for variables
def jeroslow_wang_heuristic(clauses, assignment):
    """
    Calculate Jeroslow-Wang heuristic values for variables.

    Args:
        clauses (list of lists): The CNF clauses.
        assignment (dict): The current assignment.

    Returns:
        int: The selected variable based on Jeroslow-Wang heuristic.
    """
    jw_values = {}
    for clause in clauses:
        for literal in clause:
            if literal not in assignment:
                jw_values[literal] = jw_values.get(literal, 0) + 2 ** -len(clause)
    return max(jw_values, key=jw_values.get)

# Function to solve SAT problem with Jeroslow-Wang heuristic
def solve_with_jw_heuristic(variables, clauses, assignment):
    """
    Solve SAT problem with Jeroslow-Wang heuristic.

    Args:
        variables (list): The list of variables.
        clauses (list of lists): The CNF clauses.
        assignment (dict): The current assignment.

    Returns:
        dict or None: The satisfying assignment if found, None otherwise.
    """
    if not clauses:
        return assignment

    while clauses:
        unassigned_literal = jeroslow_wang_heuristic(clauses, assignment)
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

# Function to solve SAT problem with Jeroslow-Wang heuristic
def solve_SAT_with_JW_heuristic(grid, size):
    """
    Solve SAT problem with Jeroslow-Wang heuristic.

    Args:
        grid (list of lists): The grid representing the Minesweeper game.
        size (tuple): The size of the grid.

    Returns:
        tuple: The satisfying assignment if found, None otherwise.
    """
    num_r, num_c = size
    clauses = [generate_CNF((r, c), grid, size) for r in range(num_r) for c in range(num_c)]
    flat_grid = [item for sublist in grid for item in sublist]
    num_variables = num_r * num_c

    # Flatten the list of clauses
    clauses = [clause for sublist in clauses for clause in sublist]
    assignment = {}
    result = solve_with_jw_heuristic(range(1, num_variables + 1), clauses, assignment)
    return result, flat_grid

# Function to solve Minesweeper problem using optimal algorithm with Jeroslow-Wang heuristic
def Optimal_Algorithm_Solution(grid, size):
    """
    Solve Minesweeper problem using optimal algorithm with Jeroslow-Wang heuristic.

    Args:
        grid (list of lists): The grid representing the Minesweeper game.
        size (tuple): The size of the grid.

    Returns:
        list of lists or None: The solution grid if found, None otherwise.
    """
    result, flat_grid = solve_SAT_with_JW_heuristic(grid, size)
    if result is not None:
        return output_for_algorithm_optimal(result, flat_grid, size)
    else:
        print("No solution found.")
        return None
