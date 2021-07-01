import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import psycopg2

import pandas as pd

# importieren einer test-csv, später alle Daten via SQL-Query
df = pd.read_csv("testing/p.csv")

#Ausgangsgraph erstellen
fig = px.scatter_3d(df, x='Year', y='CO2', z='CO2', color='CO2')

def connect(sql_query):
    conn = psycopg2.connect(
    host="localhost",
    database="dbs_project",
    user="postgres",
    password="1234")

    cur = conn.cursor()

    cur.execute(sql_query)
    
    result = cur
    cur.close()
    return result


# ------------- CREATING SITE ---------------------#

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("DBS Projekt"),

    # Graph
    dcc.Graph(id="3d-graph", figure=fig),

    # Filter Slider + Dropdown
    html.Div([
        html.Div([
            html.P("Länder"),
            dcc.Dropdown(
                id="dd-laender",
                options=[
                    #Generieren eines Arrays mit allen Ländern + "World" und evtl. "Europa","Asia","North America","South America","Africa", etc. via SQL-Query
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
                id='rs-ernEnergie',
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
    ),
    
    # Eingabe Buttons
    html.Div([
        html.P("Einfluss BIP auf erneuerbare Energien"),
        html.Button('BIP / ern. E', id='btn-1'),
        html.P("Einfluss BIP/Kopf auf erneuerbare Energien"),
        html.Button('(BIP/Cap) / ern. E', id='btn-2'),
        html.P("Auswirkung der Nutzung erneuerbarer Energien auf die CO2-Emission eines Landes"),
        html.Button('ern. E / CO2', id='btn-3'),
    ],
        style={
        "backgroundColor": "#DDDDDD",
        "padding": "10px 20px",
        "display": "block"
    },
    ),
])


@app.callback(
    #Output ist nur der Graph
    Output("3d-graph", "figure"),
    
    #Input als Liste, da mehrere
    [
        #Graph dient auch als Input, da falls Knopf nicht gedrückt wird, die Daten des Graphen ("figure") wieder an den Graphen ausgegeben werden
        Input("3d-graph", "figure"),

        Input("btn-1", "n_clicks"),
        Input("btn-2", "n_clicks"),
        Input("btn-3", "n_clicks"),

        Input("dd-laender", "value"),

        Input("rs-zeitraum", "value"),
        Input("rs-bip", "value"),
        Input("rs-emission", "value"),
        Input("rs-ernEnergie", "value")],
)

#wird jedes Mal ausgeführt, falls neuer Input (also Regler verändert wurden) <- muss deshalb NICHT extra aufgerufen werden
def updateGraph(fig, btn1, btn2, btn3, laender, zeitraum, bip, emission, ernEnergie):

    #Check, welcher Parameter als letztes bedient wurde, falls einer der Knöpfe -> Veränderung des Graphens
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    

    # Einfluss BIP auf erneuerbare Energien
    if 'btn-1' in changed_id:
        #Funktion mit output df (dataframe) mit BIP, Anteil ern. Energien, Jahr -> Länder einfärben
        #SQL Query liefert Daten für dataframe
        fig = px.scatter_3d(df, x='Year', y='CO2', z='CO2', color='CO2')
        result = connect("SELECT * FROM project.commoncountries")
        for row in result:
            print(row)

    # Einfluss BIP/Kopf auf erneuerbare Energien
    elif 'btn-2' in changed_id:
        #Funktion mit output df (dataframe) mit BIP/Kopf, Anteil ern. Energien, Jahr -> Länder einfärben
        #SQL Query liefert Daten für dataframe
        fig = px.scatter_3d(df, x='Year', y='Year', z='Year', color='CO2')

    # Einfluss ern. Energien auf CO2 Emission
    elif 'btn-3' in changed_id:
        #Funktion mit output df (dataframe) mit Anteil ern. Energien, CO2 Ausstoß, Jahr -> Länder einfärben
        #SQL Query liefert Daten für dataframe
        fig = px.scatter_3d(df, x='CO2', y='CO2', z='CO2', color='CO2')
    
    else: fig = fig #bedeutet, nur wenn Button gedrückt wird, verändert sich der Graph

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
