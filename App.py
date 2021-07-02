import dash
import dash_html_components as html
import dash_core_components as dcc
from pandas._config.config import options
import plotly.express as px
from dash.dependencies import Input, Output

import pandas as pd
import sql_wrangling as sw


#Ausgangsgraph erstellen
fig = px.line(sw.get_df_for_button1(), 
            x = 'year', y="perc_renen",
            color='countryname',
            labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder'))


# ------------- CREATING SITE ---------------------#

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("DBS Projekt"),


    # Graph
    dcc.Graph(id="2d-graph",figure=fig),
    
    # Filter Slider + Dropdown
    html.Div([
        html.Div([
            html.P("BIP"),
            dcc.RangeSlider(
                id='rs-bip',
                min=0, max=70000, step=0.1,
                marks={0: '0k.MUSD', 70000: '70,000k.MUSD'},
                value=[0, 70000]
            )
        ]),
        html.Div([
            html.P("CO2 Emission"),
            dcc.RangeSlider(
                id='rs-emission',
                min=0, max=11000, step=1,
                marks={0: '0.Mt', 11000: '11,000.Mt'},
                value=[0, 11000]
            )
        ]),
        html.Div([
            html.P("Anteil erneuerbarer Energien"),
            dcc.RangeSlider(
                id='rs-ernEnergie',
                min=0, max=150, step=0.1,
                marks={0: '0%', 150: '150%'},
                value=[0, 150]
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
    Output("2d-graph", "figure"),
    
    #Input als Liste, da mehrere
    [
        #Graph dient auch als Input, da falls Knopf nicht gedrückt wird, die Daten des Graphen ("figure") wieder an den Graphen ausgegeben werden
        #Input("2d-graph", "figure"),

        Input("btn-1", "n_clicks"),
        Input("btn-2", "n_clicks"),
        Input("btn-3", "n_clicks"),

        Input("rs-bip", "value"),
        Input("rs-emission", "value"),
        Input("rs-ernEnergie", "value")],
)

#wird jedes Mal ausgeführt, falls neuer Input (also Regler verändert wurden) <- muss deshalb NICHT extra aufgerufen werden
def updateGraph(btn1, btn2, btn3, bip, emission, ernEnergie):

    #alle Variablen deklarieren
    

    #Check, welcher Parameter als letztes bedient wurde, falls einer der Knöpfe -> Veränderung des Graphens
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    

    # Einfluss BIP auf erneuerbare Energien
    # Funktion mit output df (dataframe) mit BIP, Anteil ern. Energien, Jahr -> Länder einfärben
    if 'btn-1' in changed_id:
        local_df = sw.mask_df_gdp(sw.get_df_for_button1(), bip, ernEnergie, False)
        fig = px.scatter(local_df, 
                        x = "year", y = "perc_renen", 
                        size="gdp", color="countryname", 
                        range_x=[local_df["year"].min(), local_df["year"].max()], 
                        range_y=[local_df["perc_renen"].min(),local_df["perc_renen"].max()],
                        labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder'))


    # Einfluss BIP/Kopf auf erneuerbare Energien
    # Funktion mit output df (dataframe) mit BIP/Kopf, Anteil ern. Energien, Jahr -> Länder einfärben
    if 'btn-2' in changed_id:
        local_df = sw.mask_df_gdp(sw.get_df_for_button2(), bip, ernEnergie, True)
        fig = px.scatter(local_df, 
                        x = "year", y = "perc_renen", 
                        size="gdp_per_capita", color="countryname", 
                        range_x=[local_df["year"].min(), local_df["year"].max()], 
                        range_y=[local_df["perc_renen"].min(),local_df["perc_renen"].max()],
                        labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder'))

    # Einfluss ern. Energien auf CO2 Emission
    # Funktion mit output df (dataframe) mit Anteil ern. Energien, CO2 Ausstoß, Jahr -> Länder einfärben
    elif 'btn-3' in changed_id:
        local_df = sw.mask_df_emi(sw.get_df_for_button3(), emission, ernEnergie)
        fig = px.scatter(local_df, 
                        x = "year", y = "perc_renen", 
                        size="annualemissions", color="countryname", 
                        range_x=[local_df["year"].min(), local_df["year"].max()], 
                        range_y=[local_df["perc_renen"].min(),local_df["perc_renen"].max()],
                        labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder'))


    return fig

if __name__ == '__main__':

    app.run_server(debug=True)