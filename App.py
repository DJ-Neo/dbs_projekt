import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

df = px.data.iris()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("DBS Projekt"),

    #Graph
    dcc.Graph(id="scatter-plot"),
    
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
            html.P("Zeitraum"),
            dcc.RangeSlider(
            id='range-slider_zeitraum',
            min=1960, max=2019, step=1,
            marks={1960: '1960', 2019: '2019'},
            value=[1960, 2019]
            )    
        ]), 
        html.Div([
            html.P("Länder"),
            dcc.Dropdown(
            id="dropdown_laender",
            options=[
                {"label": "World", "value": "world"},
                {"label": "Germany", "value": "GER"},
                {"label": "France", "value": "FR"},
                ],
            value="normal",
            )
        ]),
        html.Div([
            html.P("BIP (* 1.000.000.000)"),
            dcc.RangeSlider(
            id='range-slider_BIP',
            min=0, max=30000, step=0.1,
            marks={0: '0$', 30000: '30.000$'},
            value=[0, 30000]
            )
        ]),
        html.Div([
            html.P("CO2 Emission"),
            dcc.RangeSlider(
            id='range-slider_emission',
            min=0, max=2.5, step=0.1,
            marks={0: '0', 2.5: '2.5'},
            value=[0.5, 2]
            )
        ]),
        html.Div([
            html.P("Anteil erneuerbarer Energien"),
            dcc.RangeSlider(
            id='range-slider_ern-energien',
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
    #html.Button('START', id='btn-start', n_clicks=0),
])

""" @app.callback(Output("scatter-plot", "figure"),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('btn-nclicks-2', 'n_clicks'),
              Input('btn-nclicks-3', 'n_clicks')) """

""" def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn1' in changed_id:
        msg = 'Do plot1 (BIP -> erneuerbare Energie)'
    elif 'btn-nclicks-2' in changed_id:
        msg = 'Do plot2 (BIP(Kopf) -> erneuerbare Energie)'
    elif 'btn-nclicks-3' in changed_id:
        msg = 'Do plot3 (Auswirkung auf CO2 Belastung)'
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div(msg) """

""" def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (df.petal_width > low) & (df.petal_width < high)

    fig = px.scatter_3d(df[mask], 
        x='sepal_length', y='sepal_width', z='petal_width',
        color="species", hover_data=['petal_width'])
    return fig """

if __name__ == '__main__':
    app.run_server(debug=True)
