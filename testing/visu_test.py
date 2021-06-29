import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

#import file
df = pd.read_csv("sisi_testing/p.csv")
x = df.Year
y = df.CO2
z = df.CO2

#data
trace = go.Scatter3d(
    x=x, 
    y=y, 
    z=z,
    )

#
layout = go.Layout(
    title = '3D')

fig = go.Figure(data = [trace],layout = layout)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
    html.H1('3D'),
        dcc.Graph(
            id='bubble',
            figure=fig, ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)