def display_solution(solution):
    print("Solution:")
    print(f"Solving status: {solution['gurobi_status']}")
    print(f"Objective value: {solution['objective_value']}")
    print(f"Centers: {solution['centers']}")