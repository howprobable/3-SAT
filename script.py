import random
from itertools import product

def generate_3sat_problem(num_variables, num_clauses):
    variables = [f'x{i}' for i in range(1, num_variables + 1)]
    clauses = []

    for _ in range(num_clauses):
        selected_variables = random.sample(variables, 3)
        clause = [f'{random.choice(["", "¬"])}{v}' for v in selected_variables]
        clauses.append(clause)

    return clauses

def evaluate_clause(clause, assignment):
    return any(assignment[var] if var[0] != '¬' else not assignment[var[1:]] for var in clause)

def brute_force_3sat_solver(clauses, num_variables):
    variables = [f'x{i}' for i in range(1, num_variables + 1)]
    for assignment in product([False, True], repeat=num_variables):
        assignment_dict = dict(zip(variables, assignment))
        if all(evaluate_clause(clause, assignment_dict) for clause in clauses):
            return assignment_dict
    return None

def all_solutions_brute_force_3sat(clauses, num_variables):
    variables = [f'x{i}' for i in range(1, num_variables + 1)]
    solutions = []

    for assignment in product([False, True], repeat=num_variables):
        assignment_dict = dict(zip(variables, assignment))
        if all(evaluate_clause(clause, assignment_dict) for clause in clauses):
            solutions.append(assignment_dict)

    return solutions

def calc_val_table(clauses, num_variables):
    value_table = {}
    for i in range(1, num_variables+1): 
        value_table[f"x{i}"] = 0 
        value_table[f"¬x{i}"] = 0 

    for clause in clauses: 
        for var in clause: 
            value_table[var] = value_table[var]+1

    ret_table = {}
    for i in range(1, num_variables+1): 
        ret_table[f"{i}"] = float(f'{-max(value_table[f"¬x{i}"], value_table[f"x{i}"])}.{i}')

    print(ret_table)


    return ret_table

def sort_clause(clause, value_table):
    # Sort variables in a clause based on index only
    return sorted(clause, key=lambda var: value_table[var.strip('¬x')])

def sort_clauses(clauses, value_table):
    # Sort clauses based on the sorted order of variables within them
    return sorted(clauses, key=lambda clause: [var.startswith('¬') for var in sort_clause(clause, value_table)])

def pretty_print_3sat_problem(clauses, num_variables):
    value_table = calc_val_table(clauses, num_variables)
    sorted_clauses = sort_clauses(clauses, value_table)
    formatted_clauses = [' ∨ '.join(sort_clause(clause, value_table)) for clause in sorted_clauses]
    problem_str = ' ∧\n'.join(formatted_clauses)
    print(f"3-SAT Problem:\n{problem_str}\n")

def pretty_print_solutions(solutions):
    if not solutions:
        print("No solutions found.")
        return

    print("Solutions:")
    for i, solution in enumerate(solutions, start=1):
        formatted_solution = ', '.join(f'{var}={value}' for var, value in solution.items())
        print(f"Solution {i}: {formatted_solution}")

def main(): 
    # Example usage
    num_variables = 5
    num_clauses = 25

    problem = generate_3sat_problem(num_variables, num_clauses)
    solutions = all_solutions_brute_force_3sat(problem, num_variables)

    pretty_print_3sat_problem(problem, num_variables)
    pretty_print_solutions(solutions)

if __name__ == "__main__":
    main()
