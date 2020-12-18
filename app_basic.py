import pandas as pd
import os
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from file_uploader import file_uploader
from network_updater import network_updater
from nw_metrics import get_metrics, modularity_click, edge_click, node_click, assortativity_click, tapNode
import base64
import io


cyto.load_extra_layouts()
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv("data/user_input.csv")

lat_range = (round(data['loc_lat'].min(),3), round(data['loc_lat'].max(),3))
long_range = (round(data['loc_long'].min(),3), round(data['loc_long'].max(),3))

def file_uploader(file_content, filename):
    if file_content is not None:
        content_type, content_string = file_content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode()))
                df.columns = df.columns.str.replace(' ', '')

                #update the ranges
                lat_range = (round(df['loc_lat'].min(),3), round(df['loc_lat'].max(),3))
                long_range = (round(df['loc_long'].min(),3), round(df['loc_long'].max(),3))
                
                df.to_csv('data/user_input.csv', index=False)

        except Exception as e:
            print(e)
            return html.Div(['There was an Error.'])

        return html.Div(['The file has been uploaded'])

#to get the max

# the style arguments for the sidebar. We use position:fixed and a fixed width.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
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
             {'label': 'Random', 'value': 'random'}, {'label': 'Dagre', 'value': 'dagre'},
             {'label': 'Klay', 'value': 'klay'}, {'label': 'Cose', 'value': 'cose'}, {'label': 'Cola', 'value': 'cola'}]
    return algos


sidebar = html.Div(
    [
        html.H2("COVID-19 Contact Tracing Dashboard", className="display-6"),
        html.Hr(),
        html.P('Pick a layout algorithm of your choice below. Beware that some layout algorithms will take time to '
               'run considering your network size.'),
        dbc.Select(
            id='algoselector',
            options=get_algorithms(),
            value='circle',
            style={"margin-bottom": "10px"}
        ),
        dcc.RangeSlider(
            id="timestep-slider",
            min=0,
            max=100,
            step=1,
            value=[0, 100]
        ),
        html.P(id="timestep-value", style={"margin-left": "15px", "margin-top": "-1.5rem"}),
        dcc.RangeSlider(
            id="lat-slider",
            min=lat_range[0],
            max=lat_range[1],
            step=0.001,
            value=[lat_range[0], lat_range[1]]
        ),
        html.P(id="lat-value", style={"margin-left": "15px", "margin-top": "-1.5rem"}),
        dcc.RangeSlider(
            id="long-slider",
            min=long_range[0],
            max=long_range[1],
            step=0.001,
            value=[long_range[0], long_range[1]]
        ),
        html.P(id="long-value", style={"margin-left": "15px", "margin-top": "-1.5rem"}),
        get_metrics(),
        html.P(id='tapNodeData', style={"margin-top": "10px", "margin-bottom": "10px"}),
        dcc.Upload(
            id='upload-file',
            children=html.Div([
                dbc.Button("Upload File", id='upload-btn', outline=True, color="secondary", className="mr-1"),
                html.Div(id='error_message')
            ])
        ),
        html.P('By Julien Lamon (MOMA: 0806-20-00)', style={"margin-top": "10px"})
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
              [Input('timestep-slider', 'value'), Input('interaction', 'value'), Input('infected', 'value'), Input('lat-slider', 'value'), Input('long-slider', 'value')]
)
def update_nw(timestep, interaction, infected, lat, longg):
    return network_updater(timestep, interaction, infected, lat, longg)


# Callback for timestep slider
@app.callback(Output('timestep-slider', 'max'),
              [Input('algoselector', 'value')])
def update_max(content):
    if os.path.getsize("data/user_input.csv") == 0:
        return 100

    data = pd.read_csv("data/user_input.csv")
    data.columns = data.columns.str.replace(' ', '')
    return data['timestep'].max()


# Callback for timestep slider
@app.callback(Output('timestep-value', 'children'),
              [Input('timestep-slider', 'value')])
def update_value_slider(value):
    return 'You have selected this timestep range: {}'.format(value)


# Callback for latitude slider
@app.callback(Output('lat-slider', 'max'),
              [Input('algoselector', 'value')])
def update_max(content):
    if os.path.getsize("data/user_input.csv") == 0:
        return lat_range[1]

    data = pd.read_csv("data/user_input.csv")
    data.columns = data.columns.str.replace(' ', '')
    #return data['loc_lat'].max()
    return lat_range[1]


# Callback for latitude slider
@app.callback(Output('lat-value', 'children'),
              [Input('lat-slider', 'value')])
def update_value_slider(value):
    return 'You have selected this latitude range: {}'.format(value)


# Callback for long slider
@app.callback(Output('long-slider', 'max'),
              [Input('algoselector', 'value')])
def update_max(content):
    if os.path.getsize("data/user_input.csv") == 0:
        return long_range[1]

    data = pd.read_csv("data/user_input.csv")
    data.columns = data.columns.str.replace(' ', '')
    #return data['loc_lat'].max()
    return long_range[1]


# Callback for long slider
@app.callback(Output('long-value', 'children'),
              [Input('long-slider', 'value')])
def update_value_slider(value):
    return 'You have selected this long range: {}'.format(value)



# Callback for network
@app.callback(Output('cytoscape-network', 'layout'),
              [Input('algoselector', 'value')])
def update_nw_layout(layout):
    if layout == 'cose':
        return {
            'name': layout,
            'componentSpacing': 100,
            'nodeRepulsion': 40000000,
            'edgeElasticity': 10000,
            'numIter': 200
        }
    else:
        return {'name': layout}


# Callback for TapNode Data
@app.callback(Output('tapNodeData', 'children'),
              Input('cytoscape-network', 'tapNodeData'))
def displayTapNodeData(data):
    return tapNode(data)


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
