from sqlalchemy import create_engine
import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H3(children='Dashboard Lieferbot Status'),

    html.H6(children='Finished Orders'),

    html.Div(
        dash_table.DataTable(
            id='results-table',
            page_action='none',
            style_table={'height': '200px', 'overflowY': 'auto'}
        ),
        style={'width': '98%'}
    ),

    html.H6(children='Overview'),

    html.Div(
        dcc.Graph(
            id="overview-graph",
            figure=go.Figure(
                layout=go.Layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=250
                )
            )
        ),
        style={'width': '49%', 'display': 'inline-block', "vertical-align": "top"}
    ),

    html.Div(
        dash_table.DataTable(
            id='overview-table',
            page_action='none',
            style_table={'height': '250px', 'overflowY': 'auto'}
        ),
        style={'width': '49%', 'display': 'inline-block', "vertical-align": "top"}
    ),

    html.H6(children='Timeouts'),

    html.Div(
        dcc.Graph(
            id="timeouts-graph",
            figure=go.Figure(
                layout=go.Layout(
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=250
                )
            )
        ),
        style={'width': '49%', 'display': 'inline-block', "vertical-align": "top"}
    ),

    html.Div(
        dash_table.DataTable(
            id='timeouts-table',
            page_action='none',
            style_table={'height': '250px', 'overflowY': 'auto'}
        ),
        style={'width': '49%', 'display': 'inline-block', "vertical-align": "top"}
    ),

    dcc.Interval(
        id='interval-component',
        interval=5*1000
    )
])


@app.callback([Output('results-table', 'columns'),
               Output('results-table', 'data'),
               Output('overview-table', 'columns'),
               Output('overview-table', 'data'),
               Output('overview-graph', 'figure'),
               Output('timeouts-table', 'columns'),
               Output('timeouts-table', 'data'),
               Output('timeouts-graph', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    connection_str = 'postgresql+psycopg2://user:password@database:5432/lieferbot'
    connection = create_engine(connection_str)

    reports = pandas.read_sql(
        "select * from reports",
        con=connection
    )
    reports_columns = [{"name": i.upper(), "id": i} for i in reports.columns]
    reports_data = reports.to_dict('records')

    overviews = pandas.read_sql(
        "select * from overviews",
        con=connection
    )
    overview_columns = [{"name": i.upper(), "id": i} for i in overviews.columns]
    overview_data = overviews.to_dict('records')

    overview_figure = go.Figure(
        data=[
            go.Scatter(
                x=list(range(len(overviews[column]))),
                y=overviews[column].to_list(),
                name=column
            ) for column in overviews.columns
        ],
        layout=go.Layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=200
        )
    )

    timeouts = pandas.read_sql(
        "select * from timeouts",
        con=connection
    )
    timeouts_columns = [{"name": i.upper(), "id": i} for i in timeouts.columns]
    timeouts_data = timeouts.to_dict('records')

    states_dict = timeouts["status"].value_counts().to_dict()
    timeouts_figure = go.Figure(
        data=go.Bar(
            x=[i.upper()for i in states_dict.keys()],
            y=[states_dict[state] for state in states_dict.keys()]
        ),
        layout=go.Layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=200
        )
    )

    return reports_columns, reports_data, overview_columns, overview_data, overview_figure, \
        timeouts_columns, timeouts_data, timeouts_figure


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
