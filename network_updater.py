import os
import pandas as pd
import networkx as nx


def network_updater(timestep, interaction, infected, lat, longg):
    if os.path.getsize("data/user_input.csv") == 0:
        return []

    data = pd.read_csv("data/user_input.csv")
    data.columns = data.columns.str.replace(' ', '')
    data = data[(data['timestep'] >= timestep[0]) & (data['timestep'] <= timestep[1])]
    
    #filter by latitude and longitude    
    data = data[(data['loc_lat'] >= lat[0]) & (data['loc_lat'] <= lat[1])]
    data = data[(data['loc_long'] >= longg[0]) & (data['loc_long'] <= longg[1])]

    elements = []
    graph = nx.Graph()

    person1 = data['person1'].tolist()
    person2 = data['person2'].tolist()
    persons = set(person1 + person2)

    # Add all nodes
    for p in persons:
        graph.add_node(p)
        elements.append({'data': {'id': 'node' + str(p), 'label': 'Person ' + str(p)}})

    # If interactions is toggled
    if interaction:
        connections = data[['person1', 'person2']].values.tolist()

        unique_list = []
        for co in connections:
            if co not in unique_list:
                unique_list.append(co) 

        # Add all edges
        for edge in unique_list:
            graph.add_edge(edge[0], edge[1])
            elements.append({'data': {'source': 'node' + str(edge[0]), 'target': 'node' + str(edge[1]),
                                      'label': 'Person ' + str(edge[0]) + ' to ' + str(edge[1])}})

    # If infected is toggled
    if infected:
        infected_data = data[data.infected1.eq(1) | data.infected2.eq(1)]
        connections = infected_data[['person1', 'person2']].values.tolist()

        unique_list = []
        for co in connections:
            if co not in unique_list:
                unique_list.append(co)

        # Add all edges
        for edge in unique_list:
            graph.add_edge(edge[0], edge[1])
            elements.append({'data': {'source': 'node' + str(edge[0]), 'target': 'node' + str(edge[1]),
                                      'label': 'Person ' + str(edge[0]) + ' to ' + str(edge[1])},
                             'classes': 'edge_infected'})

    nx.write_gexf(graph, 'data/nx_user.gexf')
    return elements
