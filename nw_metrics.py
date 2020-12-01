import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_html_components as html
import networkx as nx


def get_metrics():
    edge_metric = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("# Edges", id='edge'),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="", id="edge_placeholder", disabled=True),
    ])

    node_metric = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("# Nodes", id='node'),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="", id="node_placeholder", disabled=True),
    ])

    modu_metric = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("Modularity", id='modularity'),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="", id="modularity_placeholder", disabled=True),
    ])

    assortativity_metric = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("Assortativity", id='assortativity'),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="", id="assortativity_placeholder", disabled=True),
    ])

    interaction_edges = daq.ToggleSwitch(
        id='interaction',
        label='Interactions between people',
        value=True
    )

    infected_edges = daq.ToggleSwitch(
        id='infected',
        label='Infected people',
        value=False
    )

    row1 = html.Tr([html.Td(node_metric), html.Td(edge_metric)])
    row2 = html.Tr([html.Td(modu_metric), html.Td(assortativity_metric)])
    row3 = html.Tr([html.Td(interaction_edges), html.Td(infected_edges)])

    table_body = [html.Tbody([row1, row2, row3])]

    table = dbc.Table(table_body, bordered=True)

    return html.Div(
        table
    )


def modularity_click(click):
    if click:
        graph = nx.read_gexf('data/nx_user.gexf')
        return nx.algorithms.community.modularity(graph, nx.algorithms.community.label_propagation_communities(graph))


def edge_click(click):
    if click:
        graph = nx.read_gexf('data/nx_user.gexf')
        return graph.number_of_edges()


def node_click(click):
    if click:
        graph = nx.read_gexf('data/nx_user.gexf')
        return len(graph)


def assortativity_click(click):
    if click:
        graph = nx.read_gexf('data/nx_user.gexf')
        return nx.degree_assortativity_coefficient(graph)


def tapNode(data):
    if data:
        graph = nx.read_gexf('data/nx_user.gexf')
        clicked = "You recently clicked: " + data['label']
        br = html.Br()
        degree = "Node Degree: " + str(graph.degree[data['label'].split(' ')[1]])

        return [clicked, br, degree]
