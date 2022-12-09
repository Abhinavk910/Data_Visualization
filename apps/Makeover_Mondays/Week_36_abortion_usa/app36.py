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
DATA_PATH = PATH.joinpath('../Week_36_abortion_usa/').resolve()

df=pd.read_excel(DATA_PATH.joinpath("Abortion Support.xlsx"), parse_dates=['final_date'],
                     index_col='final_date')
df.sort_values('final_date', inplace=True)
df = df.resample('Y').mean()
df.interpolate(method='time', inplace=True)
df=df*100

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=np.arange(1975, 2021),
        y=df['Legal under any %'],
        mode="lines",
        line=dict(color='#046F12', width=3),
        marker=dict(size=7),
        line_shape='spline',
        text = [str(i) for i in list(pd.Series(df.index).dt.year)],
        hovertemplate='<i>Percentage</i>: %{y:.0f}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
)
fig.add_trace(
    go.Scatter(
        x=np.arange(1975, 2021),
        y=df['Legal only under certain %'],
        mode="lines",
        line=dict(color='#5EB35F', width=3),
        line_shape='spline',
        marker=dict(size=7),
        text = [str(i) for i in list(pd.Series(df.index).dt.year)],
        hovertemplate='<i>Percentage</i>: %{y:.0f}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
)

fig.add_trace(
    go.Scatter(
        x=np.arange(1975, 2021),
        y=df['Illegal in all %'],
        mode="lines",
        line=dict(color='#F252BA', width=3),
        line_shape='spline',
        marker=dict(size=7),
        text = [str(i) for i in list(pd.Series(df.index).dt.year)],
        hovertemplate='<i>Percentage</i>: %{y:.0f}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
)

fig.update_layout(width=500,plot_bgcolor='#F7F1F5', paper_bgcolor="#F7F1F5",showlegend=False,hovermode="x",
                  font=dict(color='#AFA49C', family="Lato"),
                  margin=dict(t=30,l=30,b=30,r=30)
)
fig.update_yaxes(visible=True, fixedrange=True,
                 range=[0,70],
                 ticksuffix = "  ",
#                  tickvals = [0,250,500,750,1000,1250,1500],                
                 gridcolor='rgba(0,0,0,0.1)', gridwidth=1, zeroline=True, zerolinecolor = '#AFA49C', zerolinewidth = 2,)
fig.update_xaxes(
    visible=True,
                 fixedrange=True,showgrid=False, zeroline=False,
#                  tickmode = 'array',
                 range=['1974', '2021'],
#                  ticktext=["June 2001 ","June 2005 ","June 2010 ","June 2015 ","June 2020 "],
#                  tickvals = [ 2001, 2005, 2010, 2015, 2020],
                ticks="outside",tickwidth=1.5,tickcolor='#AFA49C',ticklen=5,
                )

fig.add_annotation(x=0.01, y=0.95, xref='paper', yref='paper',text=f'Legal only under circumstances', showarrow=False,
                   font=dict( family="Lato",size=15, color="#5EB35F"))
fig.add_annotation(x=0.01, y=.495, xref='paper', yref='paper',text=f'Legal under any circumstances', showarrow=False,
                   font=dict( family="Lato",size=15, color="#046F12"))
fig.add_annotation(x=0.01, y=.075, xref='paper', yref='paper',text=f'Illegal in all circumstances', showarrow=False,
                   font=dict( family="Lato",size=15, color="#F252BA"))


heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

mmw36_viz = dbc.Row([
                dbc.Col([
                    
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                'Created by Abhinav, ',
                                html.A('@abhinavk910', href="https://twitter.com/abhinavk910",
                                       target="_blank", style={'color': "#BBBBBA"}),' for',
                                html.Span(' Makeover Monday Week 36', style={'color': heading_color[0]})],
                                style={'color': "#BBBBBA"}, className='m-0'),
                            html.P([
                                'This visualization highlights ',
                                html.A('Americans support abortion, but not in all cases',
                                       href="https://fivethirtyeight.com/features/why-texass-abortion-law-may-go-too-far-for-most-americans/",
                                       target="_blank",
                                       style={'color': heading_color[0]}),
                                ' in 2020'
                            ], style={'color': "#BBBBBA"}, className='m-0')
                        ])],style={'background': '', 'min-height': '100px'}, className='pt-4 pl-4'),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H1('Abortion In USA', style={'color':'#FFFBF7'}),
                                    html.P('New law bans abortion after cardiac activity can be detected, usually\
                                    about six weeks into a pregnancy. Eight other states have attempted to pass \
                                    similar bans, but the ban in Texas is the first to go into effect. As a result,\
                                    women in Texas still theoretically have a right to an abortion, but almost none \
                                    will be able to get one. A majority of americans have consistently said that\
                                    Roe v. Wade should not be overturned, But many also support a wide range of \
                                    specific restrictions. What do Americans think about Abortion?', style={'color':'#FFFBF7'})
                                    ])
                                ], style={'background':'#8C5388'}, className='m-0 p-2'),
                            
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(figure=fig,
                                              config={'displayModeBar': False})
                                    ]),
                                ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    html.H3('Abhinav Kumar',  style={'color':'RoyalBlue'})
                                ], sm=12, md=6),
                                dbc.Col([
                                    html.P('DATA SOURCE: Gallup')
                                ], sm=12, md=6)
                            ], style={'background':'#E9E5DF'}, className='m-0 p-2')
                        ]),
                    ], style={'background': 'rgba(0,0,0)'}, className='p-0 m-0'),
                    
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
                    
                ], sm=12, md=6, lg=6, xl=6)
            ], className='d-flex flex-column  align-items-center ')
