# -*- coding: utf-8 -*-
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
import pandas as pd 
import numpy as np 
import utility 
from utility import getStockDataFiveYr, getStockDataYr


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

#title in the browser
app.title = "Data Visualized" 
#app.css.append_css({'external_url' : 'https://codepen.io/amyoshino/pen/jzXypZ.css' })

#get stock data
df = getStockDataYr('^gspc')

app.layout = html.Div(
    html.Div([

        html.Div([
            #Header
            html.H1(children='Viro-Economics'),

            html.Div(children='''
            A dashboard meant to provide digestible and meaningful information about the economic effects of the pandemic.
            ''')
        ], className = "row"), #end of first row

        html.Div([
            html.Div([
                # Graph 1
                dcc.Graph(
                    id = 'stock market',
                    figure = {
                        "data" : [
                            go.Ohlc(
                                x = df['Date'],
                                open = df['Open'],
                                high = df['High'],
                                low = df['Low'],
                                close = df['Close']),
                        ],
                        "layout" : go.Layout(
                            title = go.layout.Title(text = "A Graph of the S&P 500 since 01/01/2019")
                        )
                    }
                )
            ], className = "six columns"), #end of first graph
            html.Div([
                # Graph 2
                dcc.Graph(
                    id='industry decrease',
                    figure={
                        'data': [
                            {'x': [1], 'y': [-25], 'type': 'waterfall', 'name': 'Discretionary Spending'},
                            {'x': [2], 'y': [-33], 'type': 'waterfall', 'name': 'Finance and Banking'},
                            {'x': [3], 'y': [-30], 'type': 'waterfall', 'name': 'Industry and Manufacturing'},
                            {'x': [4], 'y': [-45], 'type': 'waterfall', 'name': 'Energy'},
                            {'x': [5], 'y': [-23], 'type': 'waterfall', 'name': 'Technology'},
                            # Energy  = -45%
                            # Finance and Banking = -33%
                            # Industry and Manufacturing = -30%
                            # Discretionary Spending  = -25%
                            # Technology = -23%
                        ],
                        'layout': {
                            'title': 'Percent DECREASE of Significant Sectors of the S&P 500',
                            'xaxis': dict(
                                title = 'Sectors',
                                titlefont = dict(
                                    family = "Helvetica, monospace",
                                    size = 14
                                )
                            ),
                            'yaxis': dict(
                                title = "Percent Decrease",
                                titlefont = dict(
                                    family = "Helvetica, monospace",
                                    size = 14
                                )
                            )
                        }
                    }
                )
            ], className = "six columns") #end of second graph

        ], className = "row"), #end of second row

        html.Div([
            html.H4("Stimulus Payment Check Calculator"),
            #calculator
            html.Div([
                html.Label("Enter Filing Status"),
                dcc.RadioItems(
                    id = 'status',
                    options = [
                        {'label' : "Single", 'value': "single"},
                        {'label' : "Married Filing Jointly", 'value' : "mj"},
                        {'label' : "Head of Household", 'value' : 'hh'},
                    ], 
                    value = "single"
                ),
                html.Label("Enter the # of Children you Have Who are 16 Yrs or Younger"),
                    dcc.Input(id = "children", value = 0, type = 'number'),
                html.Label("Enter Your Gross Income"),
                    dcc.Input(id = "income", value = 0, type = "number"),
                html.Label("Amount You Can Expect to Receive: "),
                    html.Div(id = "final")
            ])
            
            
            # dcc.Input(id = "numkids", value = '', type = "text"),
            # html.Div(id = "out-div")
        ], className = "row")

    ], className = "ten columns offset-by-one")
)

@app.callback(
    Output('final', 'children'),
    [Input('status', 'value'), Input('children', 'value'), Input('income', 'value')]
)
def compute_payment(status, children, income):
    if (status == "single"):
        cutoff = 75000
        base = 1200
    elif (status == "mj"):
        cutoff = 150000
        base = 2400
    else:
        cutoff = 110000
        base = 1200
    if (income > cutoff):
        multiplier = (income - cutoff)/1000
        total = base - int(50 * multiplier)
        if (total < 0):
            return 0
        return (str(total)) + " Dollars"
    else:
        return (str(base)) + " Dollars"


if __name__ == '__main__':
    app.run_server(debug=True)
