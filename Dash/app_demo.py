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
from dash_table.Format import Format, Scheme
from datetime import datetime as dt
from utils import *

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = 'Finotex'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Más", href="#")),
        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("More pages", header=True),
        #         dbc.DropdownMenuItem("Page 2", href="#"),
        #         dbc.DropdownMenuItem("Page 3", href="#"),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Finotex Analytics",
    brand_href="#",
    color="#EF3A43",
    dark=True,
)

row = html.Div(
    [
        dbc.Row(
            [
                html.Div(
                [
                html.H5('Fases de negociación'),
                dcc.Dropdown(id='fases-dropdown',
                options=[{'label': i, 'value': i} for i in fases],
                value='Prospecto',
                style={'height': '30px', 'width': '330px'},
                ),
                ]
            )
            ],
            align="start",
        ),
        html.Br(),
        dbc.Row(
            [
            	html.Div(
        		[
        		html.H5('Fecha de facturación'),
        		dcc.DatePickerRange(
			    start_date_placeholder_text="Fecha inicio",
			    end_date_placeholder_text="Fecha fin",
			    calendar_orientation='vertical',
			    start_date='2020-01-01',
			    end_date='2020-08-01',
			    display_format='MMMM Y',
			    id = 'picker-fecha',
			    style={'height': '30px',
			    	 'width': '330px',
			    	  'fontSize':4}
			)

        		]

            		),
            ],
            align="center",
        ),
        html.Br(),
        dbc.Row(
            [
            	html.Div(
        		[
        		html.H5('Región'),
        		dcc.Dropdown(id='region-dropdown',
                options=[{'label': i, 'value': i} for i in regiones],
                value='Todas',
                style={'height': '30px', 'width': '330px'},
                )

        		]

            		),
            ],
            align="center",
        )
    ],
    style={
    	"margin": "left",
	    "width": "25%",
	    "border": "3px solid green",
	    "padding": "30px"
    }
)


app.layout = html.Div([
	navbar,
	row

	])





if __name__ == '__main__':
    app.run_server(debug=True)