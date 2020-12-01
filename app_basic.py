import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from file_uploader import file_uploader
from network_updater import network_updater
from nw_metrics import get_metrics, modularity_click, edge_click, node_click, assortativity_click

cyto.load_extra_layouts()
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and add some padding.
CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "margin-top": "2rem",
    "padding": "2rem 1rem",
    "height": "95vh"
}

# the styles for the network.
CYTO_SHEET = [
    # Group Selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },

    # Class Selectors
    {
        'selector': '.edge_infected',
        'style': {
            'background-color': 'red',
            'line-color': 'red'
        }
    },
    {
        'selector': '.node_infected',
        'style': {
            'background-color': 'red',
        }
    },
]


def get_algorithms():
    algos = [{'label': 'Circle', 'value': 'circle'}, {'label': 'Concentric', 'value': 'concentric'},
             {'label': 'Random', 'value': 'random'}, {'label': 'Spread', 'value': 'spread'},
             {'label': 'Dagre', 'value': 'dagre'}, {'label': 'Klay', 'value': 'klay'}]
    return algos


sidebar = html.Div(
    [
        html.H2("COVID-19 Contact Tracing Dashboard", className="display-6"),
        html.Hr(),
        html.P('Pick a layout algorithm of your choice below.'),
        dbc.Select(
            id='algoselector',
            options=get_algorithms(),
            value='circle',
            style={"margin-bottom": "10px"}
        ),
        get_metrics(),
        dcc.Upload(
            id='upload-file',
            children=html.Div([
                dbc.Button("Upload File", outline=True, color="secondary", className="mr-1"),
                html.Div(id='error_message')
            ])
        ),
        html.P('By Julien Lamon (MOMA: 0806-20-00)')
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        cyto.Cytoscape(
            id='cytoscape-network',
            layout={'name': 'circle'},
            style={'width': '100%', 'height': '100%'},
            stylesheet=CYTO_SHEET
        )
        # dcc.Graph(id='graph', style={'width': '100%', 'height': '100%'})
    ],
    style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Callback for file uploader
@app.callback(Output('error_message', 'children'),
              [Input('upload-file', 'contents')],
              [State('upload-file', 'filename')])
def upload_file(file_content, filename):
    return file_uploader(file_content, filename)


# Callback for network
@app.callback(Output('cytoscape-network', 'elements'),
              [Input('algoselector', 'value')])
def update_nw(value):
    return network_updater()


# Callback for network
@app.callback(Output('cytoscape-network', 'layout'),
              [Input('algoselector', 'value')])
def update_nw_layout(layout):
    return {'name': layout}


# Callback for Modularity
@app.callback(
    Output("modularity_placeholder", "placeholder"), [Input("modularity", "n_clicks")]
)
def on_modularity_click(click):
    return modularity_click(click)


# Callback for # Edges
@app.callback(
    Output("edge_placeholder", "placeholder"), [Input("edge", "n_clicks")]
)
def on_edge_click(click):
    return edge_click(click)


# Callback for # Nodes
@app.callback(
    Output("node_placeholder", "placeholder"), [Input("node", "n_clicks")]
)
def on_node_click(click):
    return node_click(click)


# Callback for Assortativity
@app.callback(
    Output("assortativity_placeholder", "placeholder"), [Input("assortativity", "n_clicks")]
)
def on_assortativity_click(click):
    return assortativity_click(click)


if __name__ == '__main__':
    app.run_server(debug=True)
