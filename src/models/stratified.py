from gurobipy import Model, GRB, quicksum
import numpy as np

# This function creates a mapping of the decision variables for the stratified p-center problem.
# It is very useful, because it reduces considerably the number of variables in the model.
def variables_mapping(instance_data):
    """
    Create a mapping of the decision variables for the stratified p-center problem.
    """
    num_nodes = instance_data['num_nodes']
    num_strata = instance_data['num_strata']
    stratum = instance_data['stratum']
    stratum_center = instance_data['stratum_center']
    
    mapping = np.zeros((num_strata, num_nodes, num_nodes))
    nb_variables = 0
    
    for s in range(num_strata):  # For each stratum
        for i in range(num_nodes):  # For each center
            for j in range(num_nodes):  # For each client
                if stratum[j, s] == 1 and stratum_center[i, s] == 1:
                    mapping[s, i, j] = nb_variables
                    nb_variables += 1
                else:
                    mapping[s, i, j] = -1
                    
    return mapping, nb_variables


def stratified_model(instance_data, ):
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
    stratum = instance_data['stratum']
    stratum_center = instance_data['stratum_center']

    mapping, nb_variables = variables_mapping(instance_data)

    # Decision variables
    x = model.addVars(nb_variables, vtype=GRB.BINARY, name="x")  # Client-to-center (primary)
    w = model.addVars(nb_variables, vtype=GRB.BINARY, name="w")  # Client-to-backup-center
    y = model.addVars(num_nodes, vtype=GRB.BINARY, name="y")      # Center opened
    max_distance = model.addVar(vtype=GRB.CONTINUOUS, name="max_distance")

    A = model.addVars(instance_data['num_strata'], vtype=GRB.CONTINUOUS, name="A")
    B = model.addVars(instance_data['num_strata'], vtype=GRB.CONTINUOUS, name="B")

    # Objective: minimize max distance (primary or backup)
    model.setObjective(max_distance, GRB.MINIMIZE)

    # Constraints

    # There is exactly p centers
    model.addConstr(y.sum() == num_centers, "num_centers")

    # Each client must be assigned to exactly one center (main)
    for s in range(instance_data['num_strata']):
        for i in range(num_nodes):
            if stratum[i, s] == 1:
                expr = quicksum(x[mapping[s, j, i]] for j in range(num_nodes) if stratum_center[j, s] == 1)
                model.addConstr(expr == 1, f"assignationCentre1_{s}_{i}")

    # Each client must be assigned to exactly one backup center
    for s in range(instance_data['num_strata']):
        for i in range(num_nodes):
            if stratum[i, s] == 1:
                expr = quicksum(w[mapping[s, j, i]] for j in range(num_nodes) if stratum_center[j, s] == 1)
                model.addConstr(expr == 1, f"assignationCentre2_{s}_{i}")

    # Each client must be assigned to an open center (main)
    # Each client must be assigned to an open backup center
    # Main and backup centers must be different
    for s in range(instance_data['num_strata']):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if stratum[i, s] == 1 and stratum_center[j, s] == 1:
                    model.addConstr(x[mapping[s, j, i]] <= y[j], f"assignationCentre1_{s}_{i}_{j}")
                    model.addConstr(w[mapping[s, j, i]] <= y[j], f"assignationCentre2_{s}_{i}_{j}")
                    model.addConstr(x[mapping[s, j, i]] + w[mapping[s, j, i]] <= 1, f"assignationCentre2_{s}_{i}_{j}")
    
    # Maximum distance constraints
    for s in range(instance_data['num_strata']):
        for i in range(num_nodes):
            if stratum[i, s] == 1:
                expr = quicksum(distances[i][j] * x[mapping[s, j, i]] for j in range(num_nodes) if stratum_center[j, s] == 1)
                model.addConstr(expr <= A[s], f"max_distance_primary_{s}_{i}")

                expr = quicksum(distances[i][j] * w[mapping[s, j, i]] for j in range(num_nodes) if stratum_center[j, s] == 1)
                model.addConstr(expr <= B[s], f"max_distance_backup_{s}_{i}")

    # The distance to the backup center must be at least superior or equal to the primary center distance
    for s in range(instance_data['num_strata']):
        for i in range(num_nodes):
            if stratum[i, s] == 1:
                expr = quicksum(w[mapping[s, j, i]] * distances[i][j] for j in range(num_nodes) if stratum_center[j, s] == 1)
                expr2 = quicksum(x[mapping[s, j, i]] * distances[i][j] for j in range(num_nodes) if stratum_center[j, s] == 1)
                model.addConstr(expr >= expr2, f"backup_distance_constraint_{s}_{i}")
    
    # Respect capacity constraints
    for s in range(instance_data['num_strata']):
        for j in range(num_nodes):
            if stratum_center[j, s] == 1:
                expr = quicksum(demands[i, s] * x[mapping[s, j, i]] for i in range(num_nodes) if stratum[i, s] == 1)
                model.addConstr(expr <= capacities[j, s] * y[j], f"capacity_primary_{s}_{j}")

                expr = quicksum(demands[i, s] * (x[mapping[s, j, i]] + w[mapping[s, j, i]]) for i in range(num_nodes) if stratum[i, s] == 1)
                model.addConstr(expr <= (1 + alpha[s]) * capacities[j, s] * y[j], f"capacity_total_{s}_{j}")

    return model, x, w, y, A, B