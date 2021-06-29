import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

import pandas as pd

#import file
df = pd.read_csv("p.csv")

#data
fig = px.scatter_3d(
    df, x='Year', y='CO2', z='CO2',
    color='CO2', 
    #size = 'Year', size_max= 2,
    #symbol='CO2', opacity = 1
    )

#tight layout
fig.update_layout(
    title ='3d figure',
    margin=dict(l=0, r=0, b=0, t=0)
)

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