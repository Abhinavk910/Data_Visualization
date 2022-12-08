import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from plotly import graph_objs as go
import pathlib
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_19_1gb_data_price/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("Cost of 1GB of Data.xlsx"))
df = df.dropna()

mmw19_wiz = dbc.Container([
                dbc.Row([
                    dbc.Col([
                    html.P([html.Span('The Price of 1GB Data in every Country', style={'font-size': '2.5vw', 'background':''}),
                            ],id = 'mmw19_1',className = 'm-0 pt-2', style = {'background': '',
                    'font-size': '30px','font-weight': 'bold', 'text-align': 'center'}),])], className = 'mt-1'),
                html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
                dbc.Row([
                    dbc.Col([
                       dcc.Graph(id='mmw19_2',  config={'displayModeBar': False},)
                    ], className="d-flex flex-column align-items-center")

                ]),
                dbc.Row([
                    dbc.Col([
                        html.P([html.Span('Note: ', style = {'font-weight' : 'bold'}),
                        "Data considers countries with a population above 1M. All currency in USD. Some Countries and \
                        territories also lack data around mobile infrastructure, or present unreliable currency conversion.",
                               ],style = {'background': '','font-size': '15px'}, className = 'm-0 pb-3')
                    ], md = 8),
                    dbc.Col([
                        html.P([html.Span('Source: ', style = {'font-weight' : 'bold'}),
                        "Cable.co.uk - Worldwide Mobile Data Pricing"],
                        style = {'background': '','font-size': '15px'}, className = 'm-0 pb-3')
                    ], md = 4)
                ],style = {'background': '',}),
                dbc.Row([
                            html.Div([
                                html.P(['Makeover Monday Week 19']),
                                html.A(html.P('Get Data'), href='https://data.world/makeovermonday/2021w19', target = "_blank")
                            ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                            html.Div([
                                html.P("Developed By: "),
                                html.Div([
                                    html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                                    href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                                ])
                            ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
                    ], className = ' d-flex justify-content-around align-content-center text-muted small mb-1', style = {'min-height': '30px'})


], fluid = False, className="d-flex flex-column justify-content-around", style= {'background':"#F7F7F7", 'height': "100vh"})


@app.callback(
    Output('mmw19_2','figure'),
    [Input('mmw19_1','children')]
)
def plotbarnba(text):
    fig = go.Figure()

    fig.add_traces(go.Scatter(x=df.col, y = df.row, text=[", ".join(["$"+str(j), i]) for i, j in zip(df.Country, df['Avg Price of 1GB (USD)'])],marker_symbol=1,
                              marker_line_color="white",
                              marker_color=df['Avg Price of 1GB (USD)'],
                              hovertemplate = '&nbsp; %{text}</b>&nbsp;<extra></extra>',
                              marker_colorscale=[[0, 'rgb(211, 234, 231)'], [0.5, 'rgb(57, 121, 173)'], [1, 'rgb(7, 69, 117)']],
                              marker_line_width=0.5, marker_size=20, mode='markers'))

    fig.update_layout(yaxis = dict(autorange="reversed",fixedrange=True,showgrid=False, showticklabels=False, showline=False,
                                  zeroline = False),
                      xaxis = dict(fixedrange = True,showgrid = False,showticklabels=False, showline=False,zeroline = False),
                      hoverlabel=dict(bgcolor="white",font_size=15,  font_family="Rockwell"),
                      margin=dict(t=0, l=0, r=0, b=0, pad = 0),
                     clickmode='event+select', height=475, width=600,plot_bgcolor='#F7F7F7',paper_bgcolor='rgb(255,255,255, 0)', )

    return fig
