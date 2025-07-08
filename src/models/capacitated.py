from gurobipy import Model, GRB

def capacitated_model(instance_data):
    """
    Gurobi model for the capacitated p-center problem.
    """

    model = Model("capacitated-p-center")

    model.setParam("Timelimit", 3600)
    model.setParam('Threads', 1)

    # Extract data
    distances = instance_data['distances']
    num_nodes = instance_data['num_nodes']
    num_edges = instance_data['num_edges']
    num_centers = instance_data['num_centers']
    demands = instance_data['demands']
    capacities = instance_data['capacities']

    # Decision variables
    x = model.addVars(num_nodes, num_nodes, vtype=GRB.BINARY, name="x")  # Client-to-center assignment
    y = model.addVars(num_nodes, vtype=GRB.BINARY, name="y")             # Center opened
    max_distance = model.addVar(vtype=GRB.CONTINUOUS, name="max_distance")

    # Objective: minimize max distance
    model.setObjective(max_distance, GRB.MINIMIZE)

    # Constraints

    # Exactly p centers are opened
    model.addConstr(y.sum() == num_centers, "num_centers")

    # Each client is assigned to exactly one center
    model.addConstrs((x.sum(i, '*') == 1 for i in range(num_nodes)),name="client_assignment")

    # Clients can only be assigned to opened centers
    model.addConstrs((x[i, j] <= y[j] for i in range(num_nodes) for j in range(num_nodes)),name="assign_if_open")

    # Respect capacity constraints
    model.addConstrs((sum(x[i, j] * demands[i] for i in range(num_nodes)) <= capacities[j] for j in range(num_nodes)),name="capacity_limit")

    # Maximum distance constraint
    model.addConstrs((x[i, j] * distances[i][j] <= max_distance for i in range(num_nodes) for j in range(num_nodes)),name="distance_limit")

    return model, x, y
