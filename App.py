import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import pandas as pd

#import test-csv
df = pd.read_csv("testing/p.csv")

#data
fig = px.scatter_3d(df, x='Year', y='CO2', z='CO2', color='CO2')


#tight layout
fig.update_layout(title ='3d figure', margin=dict(l=0, r=0, b=0, t=0))



# ------------- CREATING SITE ---------------------#

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("DBS Projekt"),

    #Graph
    dcc.Graph(id="3d-graph", figure=fig),
    
    #Eingabe Buttons
    html.Div([
        html.P("Einfluss BIP auf erneuerbare Energien"),
        html.Button('Button 1', id='btn-1'),
        html.P("Einfluss BIP/Kopf auf erneuerbare Energien"),
        html.Button('Button 2', id='btn-2'),
        html.P("Auswirkung der Nutzung erneuerbarer Energien auf die CO2-Emission eines Landes"),
        html.Button('Button 3', id='btn-3'),
        ],
        style={
                "backgroundColor": "#DDDDDD",
                "padding": "10px 20px",
                "display": "block"
        },
    ),

    #Filter Slider + Dropdown
    html.Div([
        html.Div([
            html.P("Länder"),
            dcc.Dropdown(
            id="dd_laender",
            options=[
                {"label": "World", "value": "world"},
                {"label": "Germany", "value": "GER"},
                {"label": "France", "value": "FR"},
                ],
            value="normal",
            )
        ]),
        html.Div([
            html.P("Zeitraum"),
            dcc.RangeSlider(
            id='rs-zeitraum',
            min=1960, max=2019, step=1,
            marks={1960: '1960', 2019: '2019'},
            value=[1960, 2019]
            )    
        ]), 
        html.Div([
            html.P("BIP (* 1.000.000.000)"),
            dcc.RangeSlider(
            id='rs-bip',
            min=0, max=30000, step=0.1,
            marks={0: '0$', 30000: '30.000$'},
            value=[0, 30000]
            )
        ]),
        html.Div([
            html.P("CO2 Emission"),
            dcc.RangeSlider(
            id='rs-emission',
            min=0, max=2.5, step=0.1,
            marks={0: '0', 2.5: '2.5'},
            value=[0.5, 2]
            )
        ]),
        html.Div([
            html.P("Anteil erneuerbarer Energien"),
            dcc.RangeSlider(
            id='rs-ernEnergien',
            min=0, max=30, step=0.1,
            marks={0: '0%', 30: '30%'},
            value=[0, 30]
            )
        ])
    ],
    style={
                "backgroundColor": "#DDDDDD",
                "marginTop": "10px",
                "padding": "10px 20px",
            },
    )
])

@app.callback(
    Output("3d-graph", "fig"),
    [
        Input("btn-1", "n_clicks"),
        Input("btn-2", "n_clicks"),
        Input("btn-3", "n_clicks"),

        Input("dd-laender", "value"),

        Input("rs-zeitraum", "value"),
        Input("rs-bip", "value"),
        Input("rs-emission", "value"),
        Input("rs-ernEnergie", "value")],
)

def updateGraph(btn1, btn2, btn3, laender, zeitraum, bip, emission, ernEnergie):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    #Einfluss BIP auf erneuerbare Energien
    if "btn-1" in changed_id:
        fig = px.scatter_3d(df, x='Year', y='CO2', z='CO2', color='CO2')
        fig.update_layout(title ='3d figure', margin=dict(l=0, r=0, b=0, t=0))
    elif "btn-2" in changed_id:
        fig = px.scatter_3d(df, x='Year', y='Year', z='Year', color='CO2')
        fig.update_layout(title ='3d figure', margin=dict(l=0, r=0, b=0, t=0))
    elif "btn-3" in changed_id:
        fig = px.scatter_3d(df, x='CO2', y='CO2', z='CO2', color='CO2')
        fig.update_layout(title ='3d figure', margin=dict(l=0, r=0, b=0, t=0))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)