from sqlalchemy import create_engine
import flask
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div(children=[
    html.H1(children='Overview Completed Tours'),

    html.Div(
        id="table-placeholder"
    ),

    dcc.Interval(
        id='interval-component',
        interval=10*1000
    )
])


@app.callback(Output('table-placeholder', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    connection_str = 'postgresql+psycopg2://user:password@database:5432/lieferbot'
    connection = create_engine(connection_str)
    df = pandas.read_sql(
        "select * from reports",
        con=connection
    )
    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
    return table


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
