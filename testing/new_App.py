import dash
import dash_html_components as html
import dash_core_components as dcc
from pandas._config.config import options
import plotly.express as px
from dash.dependencies import Input, Output

import pandas as pd
import sql_wrangling as sw



# importieren einer test-csv, später alle Daten via SQL-Query
df = pd.read_csv("testing/p.csv")

#Ausgangsgraph erstellen

init_df = sw.get_df_for_button1()
init_fig = px.line(init_df,  x='gdp', y='perc_renen', color='countryname',log_x = True)

dp_options = sw.getcountries()


# ------------- CREATING SITE ---------------------#

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("DBS Projekt"),

    # Graph
    dcc.Graph(id="3d-graph", figure=init_fig),

    # Filter Slider + Dropdown
    html.Div([
        html.Div([
            html.P("Länder"),
            dcc.Dropdown(
                id="dd-laender", options=dp_options
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
   

    #alle Variablen deklarieren
    country_code = laender
    
    zeit_min, zeit_max = zeitraum
    bip_min, bip_max = bip
    emission_min, emission_max = emission
    ernEn_min, ernEn_max = ernEnergie

    #Check, welcher Parameter als letztes bedient wurde, falls einer der Knöpfe -> Veränderung des Graphens
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    

    # Einfluss BIP auf erneuerbare Energien
    # Funktion mit output df (dataframe) mit BIP, Anteil ern. Energien, Jahr -> Länder einfärben
    if 'btn-1' in changed_id:
        local_df = sw.get_df_for_button1()
        fig = px.line(
            x = local_df[local_df['gdp']==zeitraum]['Value'],
            y = local_df[local_df['perc_renen'] == ernEnergie['Value']],
            color='countryname' )
        dcc.Slider(
            id='year--slider',
            min=local_df['Year'].min(),
            max=local_df['Year'].max(),
            value=local_df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        )

        

    # Einfluss BIP/Kopf auf erneuerbare Energien
    # Funktion mit output df (dataframe) mit BIP/Kopf, Anteil ern. Energien, Jahr -> Länder einfärben
    elif 'btn-2' in changed_id:
        local_df = sw.get_df_for_button2()
        fig = px.line(
            x = local_df[local_df['gdp']==zeitraum]['Value'],
            y = local_df[local_df['perc_renen'] == ernEnergie['Value']],
            color='countryname' )
        fig = px.line(local_df, x='gdp_per_capita', y='perc_renen', color='countryname')
        dcc.Slider(
            id='year--slider',
            min=local_df['Year'].min(),
            max=local_df['Year'].max(),
            value=local_df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        )

    # Einfluss ern. Energien auf CO2 Emission
    # Funktion mit output df (dataframe) mit Anteil ern. Energien, CO2 Ausstoß, Jahr -> Länder einfärben
    elif 'btn-3' in changed_id:
        local_df = sw.get_df_for_button3()
        fig = px.line(
            x = local_df[local_df['perc_renen'] == ernEnergie['Value']],
            y = local_df[local_df['annualemissions']== emission]['Value'],  
            color='countryname')
        dcc.Slider(
            id='year--slider',
            min=local_df['Year'].min(),
            max=local_df['Year'].max(),
            value=local_df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        )
    
    else: fig = fig #bedeutet, nur wenn Button gedrückt wird, verändert sich der Graph

    return fig

if __name__ == '__main__':

    app.run_server()

