import dash
# import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from file_uploader import file_uploader
from nw_metrics import get_metrics
from update_network import update_network

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def get_algorithms():
    algos = [{'label': 'Regular', 'value': 'regular'}, {'label': 'Complex', 'value': 'complex'}]
    return algos


sidebar = html.Div(
    [
        html.H2("COVID-19 Contact Tracing Dashboard", className="display-6"),
        html.Hr(),
        html.P('Pick a layout algorithm of your choice below.'),
        dbc.Select(
            id='algoselector',
            options=get_algorithms(),
            value='regular',
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
        # cyto.Cytoscape(
        #     id='cytoscape-two-nodes',
        #     layout={'name': 'random'},
        #     style={'width': '100%', 'height': '100%'},
        #     elements=[
        #         {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
        #         {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
        #         {'data': {'source': 'one', 'target': 'two'}}
        #     ]
        # )
        dcc.Graph(id='graph', style={'width': '100%', 'height': '100%'})
    ],
    style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Callback for file uploader
@app.callback(Output('error_message', 'children'),
              [Input('upload-file', 'contents')],
              [State('upload-file', 'filename')])
def upload_file(file_content, filename):
    message = file_uploader(file_content, filename)
    return message


# Callback for network
@app.callback(Output('graph', 'figure'),
              [Input('algoselector', 'value')])
def update_nw(value):
    fig = update_network(value)
    fig.layout.height = 850
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
