import dash_bootstrap_components as dbc
import dash_html_components as html


def get_metrics():
    modu_metric = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("Modularity", id='modularity'),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="", id="modularity_placeholder", disabled=True),
    ])

    degree_metric = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("Degree", id='degree'),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="", id="degree_placeholder", disabled=True),
    ])

    row1 = html.Tr([html.Td(modu_metric), html.Td(degree_metric)])
    # row2 = html.Tr([html.Td(metric_input), html.Td(metric_input)])
    # row3 = html.Tr([html.Td(metric_input), html.Td(metric_input)])

    table_body = [html.Tbody([row1])]

    table = dbc.Table(table_body, bordered=True)

    return html.Div(
        table
    )
