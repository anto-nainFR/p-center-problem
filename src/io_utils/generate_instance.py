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

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    coords = generate_clients(args.n_clients, args.space_type, args.seed, args.distribution)

    base_name = f"pc_{args.n_clients}_{args.p_centers}_{args.space_type}_{args.seed}"

    if args.output_format == 'csv':
        save_to_csv(coords, os.path.join(args.output_dir, base_name + "_clients.csv"))
    else:
        save_to_json(coords, os.path.join(args.output_dir, base_name + "_clients.json"))

    if args.compute_distances:
        dist_matrix = compute_distance_matrix(coords)
        txt_path = os.path.join(args.output_dir, base_name + "_instance.txt")
        save_distance_matrix_txt(coords, args.p_centers, txt_path, integer=args.integer_distances)

    print(f"Instance generated: {base_name}")

    if args.show_plot:
        plot_instance(coords, title=base_name)


if __name__ == "__main__":
    main()
