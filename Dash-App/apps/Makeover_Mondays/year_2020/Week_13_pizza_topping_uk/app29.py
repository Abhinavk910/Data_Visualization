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
DATA_PATH = PATH.joinpath('../Week_13_pizza_topping_uk/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("PizzaWeek.xlsx"))

hovertext = list()
for i, j in enumerate(df.Male):
    hovertext.append('<b><Span style="color:#A3A3A3;font-size:15px;">{}</span><br><Span style="color:#A3A3A3;font-size:15px;">Total-{}%</span><br><Span style="color:#70ED2F;font-size:15px;">{}</span> | <Span style="color:#677DE0;font-size:15px;">{}</span> </b>'.format(
                df.iloc[i, 0],df.iloc[i, 1], df.iloc[i, 3], df.iloc[i, 2]))

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df.Male,
    y=df.Topping,
    marker = dict(color = "#677DE0"),
    text=hovertext,
    hovertemplate='%{text}<extra></extra>',
    orientation='h'))
fig.add_trace(go.Bar(
    x=df.Female,
    y=df.Topping,
    text=hovertext,
    hovertemplate='%{text}<extra></extra>',
    marker=dict(color = "#70ED2F"),
    orientation='h'))
annotations = []
for i, j, k in zip(df.Topping, df.Male, df.Female):
    if j > k:
        annotations.append(dict(xref='x', yref='y',
                                x=j+4, y=i,
                                text='<Span style="color:#70ED2F;font-size:12px;">{}</span> <Span style="color:#677DE0;font-size:12px;">| {}</span> </b>'.format(
                                        k, j),
                                font=dict(family='Arial', size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
    else:
        annotations.append(dict(xref='x', yref='y',
                                x=k+4, y=i,
                                text='<Span style="color:#70ED2F;font-size:12px;">{}</span> <Span style="color:#677DE0;font-size:12px;">| {}</span> </b>'.format(
                                        k, j),
                                font=dict(family='Arial', size=14,
                                          color='rgb(248, 248, 255)'),
                                showarrow=False))
annotations.append(dict(x=0.5, y=1.1, xref='paper', yref='paper',
                   text = '<Span style="color:#70ED2F;font-size:15px;">Women%</span> <Span style="color:#677DE0;font-size:15px;">| Man%</span>' ,
                        align = 'left',
            showarrow=False,
            font=dict(family="Raleway, monospace", size=35,color="#838383"),
            ))
        

annotations.append(dict(x=0.97, y=0.1, xref='paper', yref='paper',
                   text = '<Span style="color:#677DE0;font-size:15px;">Man</span> are much more <br>likely than<Span style="color:#70ED2F;font-size:15px;"> women</span><br>to like meat on their<br>pizza  <br><br>'+
                          '<Span style="color:#677DE0;font-size:15px;">Man</span> more likely to enjoy<br>chillies and jalapenos,<br>whilst<Span style="color:#70ED2F;font-size:15px;"> women</span> are noticeably<br>more likely to enjoy spinach',
                        align = 'center',
            showarrow=False,
            font=dict(family="Raleway, monospace", size=11,color="#838383"),
            ))
        

fig.add_hline(y=11.5,
              fillcolor="black", opacity=0.5,
              layer="above", line_width=1,
              annotation_font_size=11,
              annotation_font_color="#A3A3A3",
              annotation_text="Above seven pizza<br> toppings are enjoyed by <br>more than half of the country ", 
              annotation_position="bottom right",
              line_color='rgba(0, 0, 0, 1.0)',
              line_dash="dot")  # 'solid', 'dot', 'dash', 'longdash', 'dashdot','longdashdot'




fig.update_layout(annotations=annotations)
fig.update_layout(barmode='overlay', height=700,width = 800, plot_bgcolor = 'white', paper_bgcolor = '#fff',
                  title ='<b><Span style="color:#787878;font-size:25px;">Brits Favourite Pizza Topping</span></b>' +
    '<i><Span style="color:#A5A5A5;font-size:15px;"><br>Mushrooms is the UK`s most liked pizza topping</span>',

                 showlegend = False, hoverlabel=dict(bgcolor="white", font_size=13, font_family="Rockwell",),
                 xaxis=dict(showgrid=False,fixedrange = True, showline=False, showticklabels=False, zeroline=False,range = [0,80] ),
                 yaxis=dict( color='#A3A3A3', showgrid=False,fixedrange = True, showline=False, showticklabels=True, zeroline=False,ticksuffix = "  ",
                           categoryorder = 'array', categoryarray = df.iloc[:, [0, 1]].sort_values('Total', ascending=True).Topping.tolist()
                           ),
                 margin=dict(l=20, r=1, t=150, b=80))
fig.data[1]['width'] = 0.3
fig.data[0]['width'] = 0.8

heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]


mmw13_viz_2020 = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 13', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' Brits Favorite Pizza',href = 'http://thedailyviz.com/2016/09/17/how-common-is-your-birthday-dailyviz/',
                          style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig,
                      config={'displayModeBar': False})
        ], style={'width': "75%", 'margin': 'auto'})
    ], style={'background': 'white', 'width': '1200px', 'min-height': '80vh', 'margin':'auto',
              "border-radius": "50px"}, className='p-5 d-flex justify-content-center align-items-center '),
    html.Div([
        html.Div([
            html.P([
                'Created by ',html.A('Abhinav', href='http://www.linkedin.com/in/abhinavk910', style={'color': heading_color[0]}),
                html.A(' Kumar', href="https://twitter.com/abhinavk910", style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'Tool: ',
                html.Span('Plotly', style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4')], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})
