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
│   │   ├── display_instance.py
│   │   └── generate_instance.py
│   └── solver
│       ├── solve.py
│       └── model.py
├── instances
│   ├── pmed
│   │   ├── pmed1.txt
│   │   ├── pmed2.txt
│   │   ├── ...
│   │   └── pmed40.txt
│   └── generated
│       └── ... (synthetic instances)
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

### Instance Generator
This project includes a parameterizable generator for synthetic p-center problem instances.

#### Generate a New Instance
You can generate test instances with custom size, layout, and options using the following command :
```
python src/io_utils/generate_instance.py \
    --n_clients 100 \
    --p_centers 5 \
    --space_type euclidean \
    --seed 42 \
    --compute_distances \
    --integer_distances \
    --show_plot
```

#### Arguments
| Argument              | Description                                                                              |
| --------------------- | ---------------------------------------------------------------------------------------- |
| `--n_clients`         | Number of demand points (**required**)                                                   |
| `--p_centers`         | Number of centers to place (**required**)                                                |
| `--space_type`        | Spatial layout: `euclidean`, `grid`, or `random` (**required**)                          |
| `--seed`              | Random seed for reproducibility                                                          |
| `--distribution`      | Spatial distribution: `uniform` (default) or `clustered` (**only for euclidean/random**) |
| `--output_format`     | Format to save client coordinates: `csv` or `json`                                       |
| `--output_dir`        | Directory to save the generated files (default: `instances/generated`)                   |
| `--compute_distances` | If set, generates and saves the distance matrix in `.txt` format                         |
| `--integer_distances` | If set, distances will be rounded to integers                                            |
| `--show_plot`         | If set, displays a 2D scatter plot of the instance using matplotlib                      |



#### Output
- Coordinates (optionally)
- Distance matrix saved in .txt format compatible with existing instance parsers
- Plots (if --show_plot is enabled)

#### Coordinate Range
All coordinates are automatically generated in the range:
$[1, \sqrt{100*n\_clients}]$ following the litterature 


## Functions Overview
- **Reading Instances**: Use `read_instance.py` to load problem instances.
- **Writing Solutions**: Use `write_solution.py` to save the results.
- **Displaying Instances**: Use `display_instance.py` to visualize the problem data.
- **Solving the Problem**: The `solve.py` file contains the logic to find the optimal solution using Gurobi.
- **Modeling**: The `model.py` file is responsible for creating the Gurobi model based on the instance data.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests.