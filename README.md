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
│   ├── models
│   │   └── classical.py
│   └── solver
│       └── solve.py
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
python -m src.main
```

3. Follow the prompts to read instances, solve the problem, and display the results.
or you can just 
```
python -m src.main <instance path>
```

### Instance Generator
This project includes a parameterizable generator for synthetic p-center problem instances.

#### Basic usage
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

#### Common arguments
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
$[1, \sqrt{100*nclients}]$ following the litterature 


#### Capacitated instances
In many real-world applications, facilities (centers) have **limited capacity** and cannot serve an unlimited number of clients. To model this more realistically, we extend the classical p-center problem by introducing:

- **Demands** for each client: how much service or resource they require.
- **Capacities** for each center: the maximum total demand a center can serve.

This transforms the problem into a **Capacitated p-Center Problem (CpCP)**, which is more challenging but better reflects logistics, emergency response, and distribution systems.

To generate a **capacitated** instance, you must include the `--capacitated` flag and provide demand-related options:
```
python src/io_utils/generate_instance.py \
    --n_clients 100 \
    --p_centers 5 \
    --space_type euclidean \
    --seed 42 \
    --capacitated \
    --tau 0.9 \
    --dem_min 5 \
    --dem_max 20 \
    --demand_distribution uniform
```
##### Additional Required Arguments for Capacitated Instances:
| Argument                | Description                                                                 |
| ----------------------- | --------------------------------------------------------------------------- |
| `--capacitated`         | Enables capacitated generation mode                                         |
| `--tau`                 | coefficient $\in$ [0, 1]. Generally around 0.8 and 0.9. |
| `--dem_min`             | Minimum client demand                                                       |
| `--dem_max`             | Maximum client demand                                                       |
| `--demand_distribution` | `uniform` or `normal` (for demand generation)                               |

As for distances, capacities are generated following the literature : 

$$\left[\frac{all\_dem\cdot0.8}{p\cdot \tau}, \frac{all\_dem\cdot1.2}{p\cdot \tau}\right]$$


## Functions Overview
- **Reading Instances**: Use `read_instance.py` to load problem instances.
- **Displaying Solutions**: Use `display_solution.py` to show the results.
- **Displaying Instances**: Use `display_instance.py` to visualize the problem data.
- **Solving the Problem**: The `solve.py` file contains the logic to find the optimal solution using Gurobi.
- **Modeling**: The `model.py` file is responsible for creating the Gurobi model based on the instance data.
- **Generator**: The `generate_instance.py` is used to generate instances according to different parameters

## Contributing
Feel free to contribute to the project by submitting issues or pull requests.
