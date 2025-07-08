# p-center-problem/src/main.py

from src.io_utils.read_instance import read_instance
from src.io_utils.display_instance import display_instance
from src.io_utils.display_solution import display_solution
from src.solver.solve import solve
import sys

def main():

    # If there is an argument, use it as the instance file path
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # user input for instance file
        file_path = input("path to the instance file: ")

    # Instance reading
    instance_data = read_instance(file_path)

    # Problem solving
    solution = solve(instance_data, model_class='classical')

    # Instance informations display
    # display_instance(instance_data)
    
    # Solution display
    display_solution(solution)
    
if __name__ == "__main__":
    main()