import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
import pathlib
import numpy as np
import plotly.graph_objects as go
import datetime
from plotly.subplots import make_subplots
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_34_entry_level_job_uk/').resolve()

df = pd.read_csv(DATA_PATH.joinpath("Jobs.csv"))


fig = go.Figure()
fig.add_trace(go.Bar(
    y=df.Job,
    x=[100]*12,
    orientation='h',
    marker=dict(color="#E9E5DF"),
    hoverinfo='none'
))
fig.add_trace(go.Bar(
    y=df.Job,
    x=df.iloc[:, 1].str.split("%", expand=True).iloc[:, 0],
    orientation='h',
    marker=dict(color="#F99963"),
    hoverinfo='none'
    
))

for i,per in enumerate(df.iloc[:, 1].tolist()):
    fig.add_annotation(x=-9, y=11-i,
            text=str(per),
            showarrow=False)
    
fig.add_shape(type="line",
    x0=0, y0=12, x1=1, y1=12,xref='paper', yref='y',
    line=dict(color="#E9E5DF",width=2)
)
fig.add_shape(type="line",
    x0=0, y0=-1, x1=1, y1=-1,xref='paper', yref='y',
    line=dict(color="#E9E5DF",width=2)
)
fig.add_annotation(x=0.05, y=13,xref='paper', yref='y',
            text='Industry',
            showarrow=False)
fig.add_annotation(x=0.65, y=13,xref='paper', yref='y',
            text='"Entry-level" jobs on LinkedIn require 3+ years<br>of experience',
            showarrow=False)


fig.update_layout(uniformtext=dict(minsize=11, mode='show'),plot_bgcolor='#FFFBF7',
                 paper_bgcolor="#FFFBF7", barmode='overlay', bargap=0.5,
                  showlegend=False,
                  margin=dict(t=10, l=0, r=0, b=10, pad = 10),
                 yaxis=dict(categoryorder = 'total ascending', anchor='free',
                  position=0.02,fixedrange=True, side='right'),
                  xaxis=dict(domain=[0.3, 1], showticklabels=False, showgrid=False,
                    fixedrange=True, zeroline=False))

heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]
mmw34_viz = dbc.Row([
                dbc.Col([
                    
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                'Created by Abhinav, ',
                                html.A('@abhinavk910', href="https://twitter.com/abhinavk910",
                                       target="_blank", style={'color': "#BBBBBA"}),' for',
                                html.Span(' Makeover Monday Week 34', style={'color': heading_color[0]})],
                                style={'color': "#BBBBBA"}, className='m-0'),
                            html.P([
                                'This visualization highlights',
                                html.A(' “Entry-level” jobs on LinkedIn require 3+ years of experience',
                                       href="https://www.linkedin.com/pulse/hirings-new-red-line-why-newcomers-cant-land-35-jobs-george-anders/",
                                       target="_blank",
                                       style={'color': heading_color[0]}),
                                ' in 2020'
                            ], style={'color': "#BBBBBA"}, className='m-0')
                        ])],style={'background': '', 'min-height': '100px'}, className='pt-4 pl-4'),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H1('The entry level job mirage', style={'color':'#FFFBF7'}),
                                    html.P('A new analysis of LinkedIn job listings - from December 2017 \
                                    through August 2021 - shows "entry-level" position often demand years \
                                    of prior experience', style={'color':'#FFFBF7'})
                                    ])
                                ], style={'background':'#BB4701'}, className='m-0 p-2'),
                            
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(figure=fig,
                                              config={'displayModeBar': False})
                                    ]),
                                ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.H3('LinkedIN',  style={'color':'RoyalBlue'})
                                ], sm=12, md=4),
                                dbc.Col([
                                    html.P('Source :- LinkedIn Economic Graph Research')
                                ], sm=12, md=8)
                            ], style={'background':'#E9E5DF'}, className='m-0 p-2')
                        ]),
                    ],no_gutters=True, style={'background': 'rgba(0,0,0)'}, className='p-0 m-0'),
                    
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                'Created by ',
                                html.A('Abhinav', href='http://www.linkedin.com/in/abhinavk910',
                                                     target="_blank", style={'color': heading_color[0]}),
                                html.A(' Kumar', href="https://twitter.com/abhinavk910",
                                       target="_blank",style={'color': heading_color[0]})],
                                style={'color': "#BBBBBA"}, className='m-0'),
                            html.P([
                                'Tool: ',
                                html.Span('Plotly', style={'color': heading_color[0]}),
                            ], style={'color': "#BBBBBA"}, className='m-0')
                        ], className='')],style={'background': '', 'min-height': '100px', "text-align": "center"},
                        className='pt-4 pl-4'),
                    
                ], sm=12, md=11, lg=8, xl=6)
            ], no_gutters=True, className='d-flex flex-column  align-items-center ')
