import dash_bootstrap_components as dbc
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

    row1 = html.Tr([html.Td(node_metric), html.Td(edge_metric)])
    row2 = html.Tr([html.Td(modu_metric), html.Td(assortativity_metric)])

    table_body = [html.Tbody([row1, row2])]

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
