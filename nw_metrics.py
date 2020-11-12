import dash_bootstrap_components as dbc
import dash_html_components as html


def get_metrics():
    metric_input = dbc.InputGroup([
        dbc.InputGroupAddon(
            dbc.Button("Modularity"),
            addon_type="prepend",
        ),
        dbc.Input(placeholder="name", disabled=True),
    ])

    row1 = html.Tr([html.Td(metric_input), html.Td(metric_input)])
    row2 = html.Tr([html.Td(metric_input), html.Td(metric_input)])
    row3 = html.Tr([html.Td(metric_input), html.Td(metric_input)])
    row4 = html.Tr([html.Td(metric_input), html.Td(metric_input)])

    table_body = [html.Tbody([row1, row2, row3, row4])]

    table = dbc.Table(table_body, bordered=True)

    return html.Div(
        table
    )
