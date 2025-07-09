from gurobipy import Model, GRB

def failure_model(instance_data):
    """
    Gurobi model for the capacitated p-center problem with Failure Foresight.
    """

    model = Model("Capacitated p-Center with Failure Foresight")

    model.setParam("Timelimit", 3600)
    model.setParam('Threads', 1)

    # Extract data
    distances = instance_data['distances']
    num_nodes = instance_data['num_nodes']
    num_edges = instance_data['num_edges']
    num_centers = instance_data['num_centers']
    demands = instance_data['demands']
    capacities = instance_data['capacities']
    alpha = instance_data['alpha']
    

    # Decision variables
    x = model.addVars(num_nodes, num_nodes, vtype=GRB.BINARY, name="x")  # Client-to-center (primary)
    w = model.addVars(num_nodes, num_nodes, vtype=GRB.BINARY, name="w")  # Client-to-backup-center
    y = model.addVars(num_nodes, vtype=GRB.BINARY, name="y")             # Center opened
    max_distance = model.addVar(vtype=GRB.CONTINUOUS, name="max_distance")

    # Objective: minimize max distance (primary or backup)
    model.setObjective(max_distance, GRB.MINIMIZE)

    # Constraints

    # Exactly p centers are opened
    model.addConstr(y.sum() == num_centers, "num_centers")

    # Each client assigned to one primary center
    model.addConstrs((x.sum(i, '*') == 1 for i in range(num_nodes)), name="primary_assignment")

    # Each client assigned to one backup center
    model.addConstrs((w.sum(i, '*') == 1 for i in range(num_nodes)), name="backup_assignment")

    # Can't assign to unopened centers
    model.addConstrs((x[i, j] <= y[j] for i in range(num_nodes) for j in range(num_nodes)), name="assign_if_open_primary")
    model.addConstrs((w[i, j] <= y[j] for i in range(num_nodes) for j in range(num_nodes)), name="assign_if_open_backup")

    # Capacity constraints
    model.addConstrs((sum(x[i, j] * demands[i] for i in range(num_nodes)) <= capacities[j] for j in range(num_nodes)),name="capacity_limit_primary")

    # Capacity constraints in case of failure (all clients go to their backups)
    model.addConstrs((sum(x[i, j] * demands[i] for i in range(num_nodes)) + sum(w[i, j] * demands[i] for i in range(num_nodes)) <= ((1+alpha)*capacities[j]) for j in range(num_nodes)),name="capacity_limit_backup")

    # No same center as both primary and backup for a client
    model.addConstrs((x[i, j] + w[i, j] <= 1 for i in range(num_nodes) for j in range(num_nodes)),name="primary_backup_different")

    # A backup center is at least as far as the primary center
    model.addConstrs((w[i, j] * distances[i][j] >= x[i, j] * distances[i][j] for i in range(num_nodes) for j in range(num_nodes)), name="backup_distance_greater_than_primary")

    # Distance limits
    model.addConstrs((x[i, j] * distances[i][j] <= max_distance for i in range(num_nodes) for j in range(num_nodes)), name="primary_distance_limit")
    model.addConstrs((w[i, j] * distances[i][j] <= max_distance for i in range(num_nodes) for j in range(num_nodes)), name="backup_distance_limit")

    return model, x, w, y
