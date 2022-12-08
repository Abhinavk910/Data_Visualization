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
DATA_PATH = PATH.joinpath('../Week_32_mortality_rate_uk/').resolve()

df = pd.read_csv(DATA_PATH.joinpath("Mortality Rates in England and Wales.csv"))
x_axis = [ i for i in range(2001, 2022)]

fig = make_subplots(rows=1, cols=2,
                   )

fig.add_trace(
    go.Scatter(
        x=x_axis,
        y=df['Males - England'],
        mode="lines+markers",
        line=dict(color='#3B6F96', width=3),
        marker=dict(size=7),
        text = ['June '+str(i) for i in x_axis],
        hovertemplate='<i>Mortality</i>: %{y}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=x_axis,
        y=df['Females - England'],
        mode="lines+markers",
        line=dict(color='#7FD8E1', width=3),
        marker=dict(size=7),
        text = ['June '+str(i) for i in x_axis],
        hovertemplate='<i>Mortality</i>: %{y}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
    row=1, col=1
)

fig.add_vrect(x0=2020, x1=2021, 
              annotation_text="COVID-19 Pendamic", annotation_position="top right",
              fillcolor="#FFCFA3", opacity=0.25, line_width=0, row=1, col=1)



fig.add_trace(
    go.Scatter(
        x=x_axis,
        y=df['Males - Wales'],
        mode="lines+markers",
        line=dict(color='#3B6F96', width=3),
        marker=dict(size=7),
        text = ['June '+str(i) for i in x_axis],
        hovertemplate='<i>Mortality</i>: %{y}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
    row=1, col=2
)
fig.add_trace(
    go.Scatter(
        x=x_axis,
        y=df['Females - Wales'],
        mode="lines+markers",
        line=dict(color='#7FD8E1', width=3),
        marker=dict(size=7),
        text = ['June '+str(i) for i in x_axis],
        hovertemplate='<i>Mortality</i>: %{y}'+
                    '<br><b>Year</b>: %{text}<br><extra></extra>'
    ),
    row=1, col=2
)

fig.add_vrect(x0=2020, x1=2021, 
              fillcolor="#FFCFA3", opacity=0.25, line_width=0, row=1, col=2)

fig.add_annotation(x=-0.01, y=1.04, xref='paper', yref='paper',text=f'England', showarrow=False,
                   font=dict( family="Lato",size=15, color="#746F6C"))
fig.add_annotation(x=0.56, y=1.04, xref='paper', yref='paper',text=f'Wales', showarrow=False,
                   font=dict( family="Lato",size=15, color="#746F6C"))
fig.add_annotation(x=-0.03, y=1.17, xref='paper', yref='paper',
                   text=f'Age-Standardised mortality rates per 100,000 people <Span style="color:#3B6F96;font-size:25px;">male</span> and'+
                         ' <Span style="color:#7FD8E1;font-size:25px;">female</span>, June 2001-2021',
                   showarrow=False,font=dict( family="Lato",size=20, color="#A89D95"))
fig.add_annotation(x=-0.03, y=1.3, xref='paper', yref='paper',
                   text=f'Monthly Mortality Rate for England and Wales, June',
                   showarrow=False,font=dict( family="Lato",size=30, color="#8B8078"))
fig.add_annotation(x=-0.03, y=-0.25, xref='paper', yref='paper',
                   text=f'Source: Office of National Statistic-Monthly mortality analysis',
                   showarrow=False,font=dict( family="Lato",size=12, color="#AFA49C"))
fig.add_annotation(x=-0.03, y=-0.3, xref='paper', yref='paper',
                   text=f'Design: Abhinav Kumar',
                   showarrow=False,font=dict( family="Lato",size=12, color="#AFA49C"))
fig.add_shape(type="rect",x0=-0.03, y0=1.35, x1=0.1, y1=1.33,xref='paper', yref='paper',
                    line=dict(color='black',width=1,),fillcolor='black',opacity = 1)
fig.update_layout(height=600, width=1000,plot_bgcolor='#FFF1E6', paper_bgcolor="#FFF1E6",showlegend=False,
                  font=dict(color='#AFA49C', family="Lato"),
                  margin=dict(t=150,l=30,b=120,r=30))
fig.update_yaxes(visible=True, fixedrange=True, range=[0,1600], ticksuffix = "  ",
                 tickvals = [0,250,500,750,1000,1250,1500],                
                 gridcolor='#EEE3D9', gridwidth=3, zeroline=True, zerolinecolor = '#AFA49C', zerolinewidth = 2,)
fig.update_xaxes(visible=True, fixedrange=True,showgrid=False, zeroline=False,
                 tickmode = 'array', range=[2000, 2022],
                 ticktext=["June 2001 ","June 2005 ","June 2010 ","June 2015 ","June 2020 "],
                 tickvals = [ 2001, 2005, 2010, 2015, 2020],
                ticks="outside",tickwidth=1.5,tickcolor='#AFA49C',ticklen=5,
                )
heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]
mmw32_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910",target="_blank", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 32', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' Monthly Mortality Rates in England and Wales',
                       href="https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/bulletins/monthlymortalityanalysisenglandandwales/june2021",
                       target="_blank",
                       style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig,
                      config={'displayModeBar': False})
        ], style={})
    ], style={'background': 'white', 'width': '1100px', 'min-height': '80vh',
              "border-radius": "50px"}, className='p-5 d-flex flex-columns align-items-center '),
    html.Div([
        html.Div([
            html.P([
                'Created by ',html.A('Abhinav', href='http://www.linkedin.com/in/abhinavk910',target="_blank", style={'color': heading_color[0]}),
                html.A(' Kumar', href="https://twitter.com/abhinavk910", target="_blank",style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'Tool: ',
                html.Span('Plotly', style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')], style={'background': '', 'width': '1200px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4'),
], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})





