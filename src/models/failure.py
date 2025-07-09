from gurobipy import Model, GRB, quicksum

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

    # There is exactly p centers
    model.addConstr(y.sum() == num_centers, "num_centers")

    # Each client must be assigned to exactly one center (main)
    model.addConstrs((x.sum(i, '*') == 1 for i in range(num_nodes)), "client_assignment")

    # Each client must be assigned to exactly one backup center
    model.addConstrs((w.sum(i, '*') == 1 for i in range(num_nodes)), "backup_assignment")

    # Each client must be assigned to an open center (main)
    model.addConstrs((x[i, j] <= y[j] for i in range(num_nodes) for j in range(num_nodes)), "assignment")

    # Each client must be assigned to an open backup center
    model.addConstrs((w[i, j] <= y[j] for i in range(num_nodes) for j in range(num_nodes)), "backup_assignment_open")

    # The maximum distance from any client to its assigned center must be less than or equal to max_distance
    model.addConstrs((x[i, j] * distances[i][j] <= max_distance for i in range(num_nodes) for j in range(num_nodes)), "max_distance_constraint")

    # The distance to the backup center must be at least superior or equal to the primary center distance
    model.addConstrs((quicksum(w[i, j] * distances[i][j] for j in range(num_nodes)) >= quicksum(x[i, j] * distances[i][j] for j in range(num_nodes)) for i in range(num_nodes)), name="backup_distance_constraint")

    # The backup center and the main center must be different
    model.addConstrs((x[i, j] + w[i, j] <= 1 for i in range(num_nodes) for j in range(num_nodes)), "different_centers")

    # Respect capacity constraints
    model.addConstrs((sum(x[i, j] * demands[i] for i in range(num_nodes)) <= capacities[j] for j in range(num_nodes)),name="capacity_limit")

    # Respect capacity constraints
    model.addConstrs((sum(x[i, j] * demands[i] for i in range(num_nodes)) + sum(w[i, j] * demands[i] for i in range(num_nodes)) <= (1+alpha)*capacities[j] for j in range(num_nodes)),name="capacity_limit")

    # Maximum distance constraint
    model.addConstrs((x[i, j] * distances[i][j] <= max_distance for i in range(num_nodes) for j in range(num_nodes)),name="distance_limit")




    return model, x, w, y
