import argparse
import json
import csv
import os
import random
import numpy as np

def generate_clients(n_clients, space_type, seed, distribution='uniform'):
    random.seed(seed)
    np.random.seed(seed)

    coord_max = np.sqrt(100 * n_clients)
    coord_min = 1

    if space_type == 'euclidean':
        if distribution == 'uniform':
            coords = np.random.uniform(coord_min, coord_max, size=(n_clients, 2))

        elif distribution == 'clustered':
            n_clusters = max(2, n_clients // 10)
            cluster_centers = np.random.uniform(coord_min, coord_max, size=(n_clusters, 2))
            coords = []
            for _ in range(n_clients):
                center = cluster_centers[random.randint(0, n_clusters - 1)]
                point = np.random.normal(loc=center, scale=0.05*coord_max, size=2)
                coords.append(point)
            coords = np.clip(coords, coord_min, coord_max)
        else:
            raise ValueError("Unsupported distribution type for euclidean space.")
    elif space_type == 'grid':
        grid_side = int(np.ceil(np.sqrt(n_clients)))
        spacing = (coord_max - coord_min) / (grid_side - 1) if grid_side > 1 else 0
        x, y = np.meshgrid(
            np.linspace(coord_min, coord_max, grid_side),
            np.linspace(coord_min, coord_max, grid_side)
        )
        coords = np.column_stack((x.ravel(), y.ravel()))[:n_clients]

    elif space_type == 'random':
        coords = np.random.uniform(coord_min, coord_max, size=(n_clients, 2))
    else:
        raise ValueError(f"Unsupported space type: {space_type}")

    return np.array(coords)

def generate_capacities(n_clients, n_centers, seed,
                        demand_distribution='uniform',
                        demand_range=(5, 20),
                        tau=0.9):
    random.seed(seed)
    np.random.seed(seed)

    # Generate client demands
    if demand_distribution == 'uniform':
        demands = np.random.randint(demand_range[0], demand_range[1] + 1, size=n_clients)
    elif demand_distribution == 'normal':
        mean = (demand_range[0] + demand_range[1]) / 2
        std_dev = (demand_range[1] - demand_range[0]) / 6  # approx 99.7% in range
        demands = np.clip(np.random.normal(mean, std_dev, size=n_clients), 
                          demand_range[0], demand_range[1]).astype(int)
    else:
        raise ValueError("Unsupported demand distribution.")

    # Generate center capacities
    total_demand = np.sum(demands)

    # Compute per-center capacity bounds
    cap_min = 0.8 * total_demand / (n_centers * tau)
    cap_max = 1.2 * total_demand / (n_centers * tau)

    # Sample capacities for each center in [cap_min, cap_max]
    capacities = np.random.uniform(cap_min, cap_max, size=n_clients).astype(int)

    return demands, capacities


def compute_distance_matrix(coords):
    from scipy.spatial.distance import cdist
    return cdist(coords, coords)

def save_to_csv(coords, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['client_id', 'x', 'y'])
        for i, (x, y) in enumerate(coords):
            writer.writerow([i, x, y])

def save_to_json(coords, file_path):
    data = [{'client_id': i, 'x': float(x), 'y': float(y)} for i, (x, y) in enumerate(coords)]
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def save_distance_matrix_txt(coords, p_centers, file_path, integer=False):
    from scipy.spatial.distance import cdist
    dist_matrix = cdist(coords, coords)
    num_nodes = len(coords)
    num_edges = num_nodes * (num_nodes - 1) // 2

    if integer:
        dist_matrix = np.rint(dist_matrix).astype(int)

    with open(file_path, 'w') as f:
        f.write(f"{num_nodes} {num_edges} {p_centers}\n")
        
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):  # upper triangle only (no duplicates)
                dist = dist_matrix[i][j]
                if integer:
                    f.write(f"{i} {j} {int(dist)}\n")
                else:
                    f.write(f"{i} {j} {dist:.2f}\n")

        # OLD FORMAT : print the full distance matrix
        # for row in dist_matrix:
        #     if integer:
        #         f.write(' '.join(str(d) for d in row) + '\n')
        #     else:
        #         f.write(' '.join(f"{d:.2f}" for d in row) + '\n')

def save_capacity(demands, capacities, txt_path):

    with open(txt_path, 'a') as f:
        for i in range(len(capacities)):
            f.write(f"{capacities[i]}\n")

        for i in range(len(demands)):
            f.write(f"{demands[i]}\n")


def plot_instance(coords, title="Generated Instance"):
    import matplotlib.pyplot as plt

    x, y = coords[:, 0], coords[:, 1]
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, c='blue', label='Clients')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Generate p-center problem instance.')
    parser.add_argument('--n_clients', type=int, required=True)
    parser.add_argument('--p_centers', type=int, required=True)
    parser.add_argument('--space_type', type=str, choices=['euclidean', 'grid', 'random'], required=True)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--distribution', type=str, choices=['uniform', 'clustered'], default='uniform')
    parser.add_argument('--output_format', choices=['csv', 'json'], default='csv')
    parser.add_argument('--output_dir', type=str, default='instances/generated', help='Directory to save the generated instance files. By default, it is "instances/generated".')
    parser.add_argument('--compute_distances', action='store_true')
    parser.add_argument('--integer_distances', action='store_true', help='If set, distances will be rounded to integers.')
    parser.add_argument('--show_plot', action='store_true', help='If set, displays a 2D scatter plot of the instance using matplotlib.')
    parser.add_argument('--capacitated', action='store_true', help='If set, generates a capacitated instance.')

    # Conditional arguments
    parser.add_argument('--tau', type=float, help='Load factor for capacities. Should be around 0.8 and 0.9 (only used if capacitated).')
    parser.add_argument('--dem_min', type=int, help='Minimum demand per client (only used if capacitated).')
    parser.add_argument('--dem_max', type=int, help='Maximum demand per client (only used if capacitated).')
    parser.add_argument('--demand_distribution', choices=['uniform', 'normal'], help='Demand distribution (only used if capacitated).')

    args = parser.parse_args()
    if args.n_clients <= 0:
        parser.error("Number of clients must be a positive integer.")
    if args.p_centers <= 0:
        parser.error("Number of centers must be a positive integer.")
    if args.p_centers > args.n_clients:
        parser.error("Number of centers cannot exceed number of clients.")
    if args.capacitated:
        missing = []
        if args.tau is None:
            missing.append('--tau')
        if args.dem_min is None:
            missing.append('--dem_min')
        if args.dem_max is None:
            missing.append('--dem_max')
        if args.demand_distribution is None:
            missing.append('--demand_distribution')

        if missing:
            parser.error(f"The following arguments are required when --capacitated is set: {', '.join(missing)}")

    os.makedirs(args.output_dir, exist_ok=True)

    coords = generate_clients(args.n_clients, args.space_type, args.seed, args.distribution)
    if args.capacitated:
        demands, capacities = generate_capacities(
            n_clients=args.n_clients,
            n_centers=args.p_centers,
            seed=args.seed,
            demand_distribution=args.demand_distribution,
            demand_range=(args.dem_min, args.dem_max),
            tau=args.tau
        )
        base_name = f"pc_{args.n_clients}_{args.p_centers}_{args.space_type}_{args.seed}_capacitated"
    else:
        base_name = f"pc_{args.n_clients}_{args.p_centers}_{args.space_type}_{args.seed}"

    if args.output_format == 'csv':
        save_to_csv(coords, os.path.join(args.output_dir, base_name + "_clients.csv"))
    else:
        save_to_json(coords, os.path.join(args.output_dir, base_name + "_clients.json"))

    if args.compute_distances:
        dist_matrix = compute_distance_matrix(coords)
        txt_path = os.path.join(args.output_dir, base_name + "_instance.txt")
        save_distance_matrix_txt(coords, args.p_centers, txt_path, integer=args.integer_distances)
        if args.capacitated:
            save_capacity(demands, capacities, txt_path)

    print(f"Instance generated: {base_name}")

    if args.show_plot:
        plot_instance(coords, title=base_name)


if __name__ == "__main__":
    main()
