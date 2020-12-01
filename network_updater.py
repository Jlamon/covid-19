import pandas as pd
import networkx as nx


def network_updater(timestep):
    # Load data from Toy Dataset
    data = pd.read_csv("data/scenario4.csv")
    data.columns = data.columns.str.replace(' ', '')
    data = data[(data['timestep'] >= timestep[0]) & (data['timestep'] <= timestep[1])]

    elements = []
    graph = nx.Graph()

    person1 = data['person1'].tolist()
    person2 = data['person2'].tolist()
    persons = set(person1 + person2)

    connections = data[['person1', 'person2']].values.tolist()

    unique_list = []
    for co in connections:
        if co not in unique_list:
            unique_list.append(co)

    # Add all nodes
    for p in persons:
        graph.add_node(p)
        elements.append({'data': {'id': 'node' + str(p), 'label': 'Person ' + str(p)}})

    # Add all edges
    for edge in unique_list:
        graph.add_edge(edge[0], edge[1])
        elements.append({'data': {'source': 'node' + str(edge[0]), 'target': 'node' + str(edge[1]),
                                  'label': 'Person ' + str(edge[0]) + ' to ' + str(edge[1])}})
    
    nx.write_gexf(graph, 'data/nx_user.gexf')
    return elements


if __name__ == '__main__':
    network_updater()