import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
import pathlib
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_21_wildlife_population_changing/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("Wildlife Population Change.xlsx"))

df.sort_values('Increasing Populations', inplace = True)

# data cleaning
a = df['Increasing Populations']*100
increase = -1*a.astype(int)
increase = increase.tolist()

a = df['Stable']*100
a = a.astype(int)
stable_negative = -1*a/2
stable_negative = stable_negative.tolist()
stable_positive = a/2
stable_positive = stable_positive.tolist()

a = df['Decreasing Populations']*100
decrease = a.astype(int)
decrease = decrease.tolist()

# graph
Taxonomic_Group = df['Taxonomic Group'].tolist()

fig = go.Figure(data=[
    go.Bar(
        y=Taxonomic_Group,
        x=stable_negative,
        orientation='h',
        marker=dict(color='#C37C36', line=dict(
            color='rgba(0, 0, 0, 1.0)', width=0.5)),
        hovertemplate=None,
        hoverinfo='none',
    ),
    go.Bar(name='Increasing',
           y=Taxonomic_Group,
           x=increase,
           orientation='h',
           marker=dict(color='#AE565B', line=dict(
               color='rgba(0, 0, 0, 1.0)', width=0.5)),
           hoverinfo='none',
           ),

    go.Bar(name='LA Zoo2',
           y=Taxonomic_Group,
           x=stable_positive,
           orientation='h',
           marker=dict(color='#C37C36', line=dict(
               color='rgba(0, 0, 0, 1)', width=0.5)),
           hoverinfo='none',
           ),
    go.Bar(name='LA Zoo3',
           y=Taxonomic_Group,
           x=decrease,
           orientation='h',
           marker=dict(color='#555F76', line=dict(
               color='rgba(0, 0, 0, 1.0)', width=0.5)),
           hoverinfo='none',
           ),
])

fig.add_vline(x=0,
              fillcolor="black", opacity=1,
              layer="above", line_width=2,
              line_color='rgba(0, 0, 0, 1.0)',
              line_dash="solid")  # 'solid', 'dot', 'dash', 'longdash', 'dashdot','longdashdot'


annotations = []

for yd, inc, dec in zip(Taxonomic_Group, increase, decrease):
    annotations.append(dict(xref='x', yref='y',
                            x=inc / 2, y=yd,
                            text=str(-1*inc) + '%',
                            font=dict(family='Arial', size=14,
                                      color='rgb(248, 248, 255)'),
                            showarrow=False))
    annotations.append(dict(xref='x', yref='y',
                            x=dec / 2, y=yd,
                            text=str(dec) + '%',
                            font=dict(family='Arial', size=14,
                                      color='rgb(248, 248, 255)'),
                            showarrow=False))
annotations.append(dict(text='Increasing',
                        xref="x", yref="paper", textangle=0,
                        x=-30, y=1.1, showarrow=False,
                        font=dict(family='Arial', size=19,
                                  color='rgb(67, 67, 67)'),
                        ))
annotations.append(dict(text='Decreasing',
                        xref="x", yref="paper", textangle=0,
                        x=30, y=1.1, showarrow=False,
                        font=dict(family='Arial', size=19,
                                  color='rgb(67, 67, 67)'),
                        ))
annotations.append(dict(text='Stable',
                        xref="x", yref="paper", textangle=0,
                        x=0, y=1.1, showarrow=False,
                        font=dict(family='Arial', size=19,
                                  color='rgb(67, 67, 67)'),
                        ))
# Change the bar mode
# 'stack', 'group', 'overlay', 'relative'
fig.update_layout(barmode='relative')
fig.update_layout(annotations=annotations)
fig.update_layout(title=dict(
    text='<Span style="color:rgb(67, 67, 67);font-size:25px;">HOW ARE WILDLIFE POPULATION CHANGING </span>',
    font=dict(size=25, family='Rockwell, monospace', color='#C1C5C7'),
    x=0.5
),)
fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        domain=[0.15, 1]
    ),
    yaxis=dict(
        color='rgb(67, 67, 67)',
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
    ),
    paper_bgcolor='rgb(248, 248, 255)',
    plot_bgcolor='rgb(248, 248, 255)',
    margin=dict(l=10, r=10, t=140, b=80),
    showlegend=False,
)
fig.add_annotation(text="WWF (2020) Living Planet Report 2020 – Bending the curve of biodiversity loss.<br>Almond, R.E.A., Grooten M. and Petersen, T. (Eds). WWF, Gland, Switzerland",
                   xref="paper", yref="paper", font=dict(family="Rockwell, monospace", size=12, color='gray'),
                   x=0.5, y=-0.25, showarrow=False)




heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

mmw21_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 21', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' 2020 GLOBAL LIVING PLANET INDEX',href = 'https://ourworldindata.org/living-planet-index-understanding',
                          style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    html.Div([
        html.Div([
            dcc.Graph(id='mmw21_1', figure=fig,
                      config={'displayModeBar': False})
        ], style={'width': "100%"})
    ], style={'background': 'rgb(248, 248, 255)', 'width': '1200px', 'min-height': '80vh',
              "border-radius": "50px"}, className='p-5'),
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
    ], style={'background': '', 'width': '1200px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4'),
], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})
