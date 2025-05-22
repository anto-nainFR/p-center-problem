# p-center-problem
Gurobi code example to solve the classical p-center problem.

## Project Structure
```
p-center-problem
├── src
│   ├── main.py
│   ├── io_utils
│   │   ├── read_instance.py
│   │   ├── display_solution.py
│   │   └── display_instance.py
│   └── solver
│       ├── solve.py
│       └── model.py
├── instances
│   ├── pmed1.txt
│   │    ...
│   └── pmed40.txt
├── requirements.txt
└── README.md
```

## Installation
To set up the project, ensure you have Python and Gurobi installed. Then, install the required packages using:

```
python -m venv .venv
source ./venv/bin/activate

pip install -r requirements.txt
```

## Usage
1. Place your p-center problem instances in a suitable format in the designated directory.
2. Run the main application:

```
python src/main.py
```

3. Follow the prompts to read instances, solve the problem, and display the results.

## Functions Overview
- **Reading Instances**: Use `read_instance.py` to load problem instances.
- **Displaying Solutions**: Use `display_solution.py` to show the results.
- **Displaying Instances**: Use `display_instance.py` to visualize the problem data.
- **Solving the Problem**: The `solve.py` file contains the logic to find the optimal solution using Gurobi.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests.
