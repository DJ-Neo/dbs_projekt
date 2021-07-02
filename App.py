from logging import FATAL
import dash
import dash_html_components as html
import dash_core_components as dcc
from pandas._config.config import options
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import pandas as pd
import sql_wrangling as sw

#Ausgangsgraph erstellen

# ------------- CREATING SITE ---------------------#

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("DBS Projekt"),
    # Graph
    dcc.Graph(id="2d-graph"),
    
    # Filter Slider + Dropdown
    html.Div([
        html.Div([
            html.H2(children= "Auswahl des Graphens"),
            dcc.RadioItems(id= "graph-select",
                options=[
                    {"label": "Einfluss BIP auf erneuerbare Energien", "value": "gdp"},
                    {"label": "Einfluss BIP/Kopf auf erneuerbare Energien", "value": "gdp_c"},
                    {"label": "Auswirkung der Nutzung erneuerbarer Energien auf die CO2-Emission eines Landes", "value": "co2"}
                ],
                value="gdp")
        ]),
        html.Div([
            html.H2(children = "BIP"),
            dcc.RangeSlider(
                id='rs-bip',
                min=0, max=22000, step=0.1,
                marks={0: '0 USD', 22000: '22.000 * Milliarden USD'},
                value=[0, 22000]
            )
        ], id="div-bip-slider", hidden=False),
        html.Div([
            html.H2(children = "BIP/Kopf"),
            dcc.RangeSlider(
                id='rs-bip_c',
                min=0, max=1200, step=0.1,
                marks={0: '0 USD', 1200: '120.000 USD'},
                value=[0, 1200]
            )
        ], id="div-bip-pro-kopf-slider", hidden=True),
        html.Div([
            html.H2("CO2 Emission"),
            dcc.RangeSlider(
                id='rs-emission',
                min=0, max=11000, step=1,
                marks={0: '0.Mt', 11000: '11,000.Mt'},
                value=[0, 11000]
            )
        ], id="div-co2-slider", hidden=True),
        html.Div([
            html.H2("Anteil erneuerbarer Energien"),
            dcc.RangeSlider(
                id='rs-ernEnergie',
                min=0, max=150, step=0.1,
                marks={0: '0%', 150: '150%'},
                value=[0, 150]
            )
        ])
    ]
    ),
])


@app.callback(
    Output(component_id="2d-graph", component_property="figure"),
    Output(component_id="div-bip-slider",component_property="hidden"),
    Output(component_id="div-bip-pro-kopf-slider",component_property="hidden"),
    Output(component_id="div-co2-slider",component_property="hidden"),

    #Input als Liste, da mehrere
    [
        #Graph dient auch als Input, da falls Knopf nicht gedrückt wird, die Daten des Graphen ("figure") wieder an den Graphen ausgegeben werden
        Input("rs-bip", "value"),
        Input("rs-bip_c", "value"),
        Input("rs-emission", "value"),
        Input("rs-ernEnergie", "value"),
        Input("graph-select", "value")
        ]
)

#wird jedes Mal ausgeführt, falls neuer Input (also Regler verändert wurden) <- muss deshalb NICHT extra aufgerufen werden
def updateGraph(bip, bip_c, emission, ernEnergie, graph_select):
    #Check, welcher Parameter als letztes bedient wurde, falls einer der Knöpfe -> Veränderung des Graphens
    #global g_type
    hidden_bip_slider = False
    hidden_bip_pk_slider = True
    hidden_co2_slider = True

    # Einfluss BIP auf erneuerbare Energien
    # Funktion mit output df (dataframe) mit BIP, Anteil ern. Energien, Jahr -> Länder einfärben
    if graph_select == 'gdp':
        hidden_bip_slider = False
        hidden_bip_pk_slider = True
        hidden_co2_slider = True
        
        init_df = sw.get_df_for_button1()
        local_df = sw.mask_df_gdp(init_df, bip, ernEnergie, False)
        fig = px.scatter(local_df, 
                        x = "year", y = "perc_renen", 
                        size="gdp", color="countryname", 
                        range_x=[init_df["year"].min(),init_df["year"].max()], 
                        range_y=[local_df["perc_renen"].min(),local_df["perc_renen"].max()],
                        labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder')
                        )


    # Einfluss BIP/Kopf auf erneuerbare Energien
    # Funktion mit output df (dataframe) mit BIP/Kopf, Anteil ern. Energien, Jahr -> Länder einfärben
    
    #if graph_select == 'gdp_c':
    elif graph_select == 'gdp_c':
        hidden_bip_slider = True
        hidden_bip_pk_slider = False
        hidden_co2_slider = True

        init_df = sw.get_df_for_button2()
        local_df = sw.mask_df_gdp(init_df, bip_c, ernEnergie, True)
        fig = px.scatter(local_df, 
                        x = "year", y = "perc_renen", 
                        size="gdp_per_capita", color="countryname", 
                        range_x=[init_df["year"].min(),init_df["year"].max()], 
                        range_y=[local_df["perc_renen"].min(),local_df["perc_renen"].max()],
                        labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder')
                        )

    # Einfluss ern. Energien auf CO2 Emission
    # Funktion mit output df (dataframe) mit Anteil ern. Energien, CO2 Ausstoß, Jahr -> Länder einfärben
    
    #if graph_select == 'co2':
    else:
        hidden_bip_slider = True
        hidden_bip_pk_slider = True
        hidden_co2_slider = False
        
        init_df = sw.get_df_for_button3()
        local_df = sw.mask_df_emi(init_df, emission, ernEnergie)
        fig = px.scatter(local_df, 
                        x = "year", y = "perc_renen", 
                        size="annualemissions", color="countryname", 
                        range_x=[init_df["year"].min(),init_df["year"].max()], 
                        range_y=[local_df["perc_renen"].min(),local_df["perc_renen"].max()],
                        labels=dict(perc_renen = 'Anteil erneuerbarer Energien', year = 'Jahr', countryname = 'Länder')
                        )

    return fig, hidden_bip_slider, hidden_bip_pk_slider, hidden_co2_slider     #  Wenn True -> bip-slider = NOT hidden, bip-pro-kopf-slider = hidden

if __name__ == '__main__':
    updateGraph
    app.run_server(debug=True)