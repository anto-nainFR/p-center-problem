def read_instance_cap_fail(file_path, capacitated=False, failure=False, alpha=0.0):
    instance_data = {}
    with open(file_path, 'r') as file:
        # Only pmed instance are supported here, add other formats depending on the instance family
        # first line : number of nodes, number of edges, number of centers
        line = file.readline().strip()
        num_nodes, num_edges, num_centers = map(int, line.split())
        
        instance_data['num_nodes'] = num_nodes
        instance_data['num_edges'] = num_edges
        instance_data['num_centers'] = num_centers

        # edges reading : format (node1, node2, distance)
        edges = []
        for _ in range(num_edges):
            line = file.readline().strip()
            node1, node2, distance = map(int, line.split())
            edges.append((node1-1, node2-1, distance))
        
        distances = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            distances[i][i] = 0
        for node1, node2, distance in edges:
            distances[node1][node2] = distance
            distances[node2][node1] = distance

        # Floyd-Warshall algorithm to compute all pairs shortest paths (to avoid inf distances)
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if distances[i][j] > distances[i][k] + distances[k][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]

        instance_data['distances'] = distances

        if capacitated or failure:
            # Read capacities
            capacities = []
            for _ in range(num_nodes):
                line = file.readline().strip()
                capacities.append(int(line))
            instance_data['capacities'] = capacities

            # Read demands
            demands = []
            for _ in range(num_nodes):
                line = file.readline().strip()
                demands.append(int(line))
            instance_data['demands'] = demands

        if failure:
            # Read failure foresight alpha
            instance_data['alpha'] = alpha
        
    return instance_data


def read_instance_stratified(file_path):
    


def read_instance(file_path, capacitated=False, failure=False, alpha=0.0, stratified=False):
    if capacitated or failure:
        return read_instance_cap_fail(file_path, capacitated=capacitated, failure=failure, alpha=alpha)
    elif stratified:
        return read_instance_stratified(file_path)