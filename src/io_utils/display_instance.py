def display_instance(instance_data):
    
    # Display the instance data in a readable format
    print("Instance Data:")
    print(f"Number of nodes: {instance_data['num_nodes']}")
    print(f"Number of edges: {instance_data['num_edges']}")
    print(f"Number of centers: {instance_data['num_centers']}")
    print("Distances:")
    for i in range(instance_data['num_nodes']):
        print(f"Node {i+1}: ", end="")
        for j in range(instance_data['num_nodes']):
            if instance_data['distances'][i][j] == float('inf'):
                print("inf", end=" ")
            else:
                print(instance_data['distances'][i][j], end=" ")
        print()