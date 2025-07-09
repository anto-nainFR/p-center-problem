# p-center-problem/src/main.py

import argparse

from src.io_utils.read_instance import read_instance
from src.io_utils.display_instance import display_instance
from src.io_utils.display_solution import display_solution
from src.solver.solve import solve
import sys

def main():

    # If there is an argument, use it as the instance file path
    parser = argparse.ArgumentParser(description='p-center problem and its variants solver')
    parser.add_argument('--file', nargs='?', default=None, help='Path to the instance file. If not provided, it will prompt for input.')
    
    # if it is the capacitated version, add the argument
    parser.add_argument('--capacitated', action='store_true', help='If set, the solver will handle capacitated p-center problem instances.')
    parser.add_argument('--failure', action='store_true', help='If set, the solver will handle p-center problem instances with failure foresight.')
    args = parser.parse_args()
    
    if args.file:
        file_path = args.file
    else:
        # user input for instance file
        file_path = input("path to the instance file: ")

    # Instance reading
    is_capacitated = False
    is_failure = False
    model_class = "classical"
    if args.failure:
        # If the instance is with failure foresight, read the failure foresight instance
        is_failure = True
        model_class = "failure"
    elif args.capacitated:
        # If the instance is capacitated, read the capacitated instance
        is_capacitated = True
        model_class = "capacitated"
    
        
    instance_data = read_instance(file_path, capacitated=is_capacitated)

    # Problem solving
    solution = solve(instance_data, model_class=model_class)

    # Instance informations display
    # display_instance(instance_data)
    
    # Solution display
    display_solution(solution)
    
if __name__ == "__main__":
    main()