import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from dash_table.Format import Format, Scheme
from datetime import datetime as dt
from utils import *
from data_man import ventas, total_nov, total_oct, unidades_oct,unidades_nov, static_up, cambio_porcentual

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = 'Finotex'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Más", href="#")),
    ],
    brand="Finotex",
    brand_href="#",
    color="#EF3A43",
    dark=True,
)

row = dbc.Container(
    [
        dbc.Row(
            [
                
                dbc.Col(
                [
                html.H5('Participación de clientes (%)'),
                dcc.Dropdown(id='year-dropdown',
                options=[{'label': i, 'value': i} for i in ventas.Year.sort_values().unique()],
                value=2020,
                ),
                dcc.RadioItems(
                id='radio-tipo',
                options=[{'label':i,'value':i} for i in ventas.TIPO.sort_values().unique()],
                value='PESOS',
                labelStyle={'display': 'inline-block'}
            ),
                dcc.Graph(id='dist-ventas'),
                ]
            ),
            dbc.Col(
                [
                html.H5('Serie de Ventas Mensual'),
                dcc.Dropdown(id='year-2-dropdown',
                options=[{'label': i, 'value': i} for i in ventas.Year.sort_values().unique()],
                value=2020,
                ),
                dcc.RadioItems(
                id='radio-2-tipo',
                options=[{'label':i,'value':i} for i in ventas.TIPO.sort_values().unique()],
                value='PESOS',
                labelStyle={'display': 'inline-block'}
            ),
                dcc.Graph(id='serie-ventas'),
                ]
            )
            ],
        ),
        
    ],
    # style={
    # 	"margin": "left",
	#     "width": "25%",
	#     "border": "3px solid green",
	#     "padding": "30px"
    # }
)


app.layout = html.Div([
	navbar,
    html.H1('Visualización de ventas',style={'textAlign':'center'}),
	row,
    dbc.Container(
        [
            html.H3(f'${total_nov:,}',style={'textAlign':'center'}),
            html.H4('Pesos en ventas',style={'textAlign':'center'}),
            html.H3(f'+{cambio_porcentual}%',style={'textAlign':'center'}),
            static_up,
            html.H4('Respecto al mes pasado',style={'textAlign':'center'}),
            
        ]
    )

	])

@app.callback(
    Output('dist-ventas','figure'),
    [Input('year-dropdown','value'),
    Input('radio-tipo','value'),]
)

def update_dist(year,tipo):
    mask = (ventas.Year==year)&(ventas.TIPO==tipo)
    data = ventas[mask]
    if tipo == 'DLS':
        tipo_serie = 'TOTAL_MX'
    else:
        tipo_serie = 'TOTAL_DLS'
    serie = data.groupby('LINEA')[['TIPO',tipo_serie]].agg({
    'TIPO':'count',
    tipo_serie:'sum'
    }).sort_values(by='TIPO').round()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=serie.index, y=serie['TIPO'],marker_color='#03fce3',name='Participación'))
    fig.add_trace(go.Scatter(x=serie.index,y=serie[tipo_serie],marker_color='#eb46d7',name='Monto Total'),
    secondary_y=True,)
    fig.update_layout(
        yaxis_nticks=10,
        xaxis_title="Cliente",
        yaxis_title="<em>Participación<em>",
        font=dict(
            size=10,
            family='Arial'
        ),
    )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig

@app.callback(
    Output('serie-ventas','figure'),
    [Input('year-2-dropdown','value'),
    Input('radio-2-tipo','value'),]
)

def update_serie(year,tipo):
    mask = (ventas.Year==year)&(ventas.TIPO==tipo)
    data = ventas[mask]
    serie = data.groupby('MES').TOTAL_MX.sum().round()
    fig = go.Figure(go.Scatter(x=serie.index, y=serie))
    fig.update_layout(
        yaxis_nticks=10,
        # yaxis=dict(tickformat=".0f"),
        xaxis_title="Mes",
        yaxis_title="<em>Total $ (Pesos) %<em>",
        font=dict(
            size=10,
            family='Arial'
        ),
    )
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)