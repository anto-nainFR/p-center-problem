# p-center-problem/src/main.py

from io_utils.read_instance import read_instance
from io_utils.display_instance import display_instance
from io_utils.display_solution import display_solution
from solver.solve import solve

def main():
    # user input for instance file
    file_path = input("path to the instance file: ")

    # Instance reading
    instance_data = read_instance(file_path)

    # Problem solving
    solution = solve(instance_data)

    # Instance informations display
    # display_instance(instance_data)
    
    # Solution display
    display_solution(solution)
    
if __name__ == "__main__":
    main()