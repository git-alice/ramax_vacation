import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd


def switch_month(x):
    return {
        1: ['2021-01-01', '2021-01-30'],
        2: ['2021-02-01', '2021-02-28'],
        3: ['2021-03-01', '2021-03-30'],
        4: ['2021-04-01', '2021-04-30'],
        5: ['2021-05-01', '2021-05-30'],
        6: ['2021-06-01', '2021-06-30'],
        7: ['2021-07-01', '2021-07-30'],
        8: ['2021-08-01', '2021-08-30'],
        9: ['2021-09-01', '2021-09-30'],
        10: ['2021-10-01', '2021-10-30'],
        11: ['2021-11-01', '2021-11-30'],
        12: ['2021-12-01', '2021-12-30']
    }[x]


def add_employers(input_df):
    df = pd.DataFrame()
    for index, row in input_df.iterrows():
        start = switch_month(row['month'])[0]
        finish = switch_month(row['month'])[1]
        qty_hour = row['rest_size']
        application = row['application']
        task = int(row['id'])
        df = df.append([dict(Task=task, Start=start, Finish=finish, Complete=application,
                             Description = qty_hour)], ignore_index=True)
    return df

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP,
    'https://codepen.io/chriddyp/pen/brPBPO.css',
    'https://dash-gallery.plotly.host/dash-oil-and-gas/assets/styles.css',
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Планированию расписания отпусков крупной компании.'),
    html.Label([
        html.Div(
            "Выберете номер квалификации",
            style={
                'margin-right': '20px'
            }
        ),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': f'Q{i}', 'value': f'./data/res_v.0.03_Q{i}.csv'} for i in range(1, 11)
            ],
            value='./data/res_v.0.03_Q9.csv'
        ),
    ],
        style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        }
    ),
    html.Hr(),

    dcc.Graph(
        id='graph',
        figure={}
    )
])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    excel_df = pd.read_csv(value)
    height_window = len(excel_df) * 15

    df = add_employers(excel_df)

    fig = ff.create_gantt(
        df,
        title="График отпусков",
        colors='Viridis', index_col='Complete', showgrid_x=True,
        height=height_window)
    fig.layout.xaxis.rangeselector = None
    fig.update_yaxes(autorange="reversed")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
