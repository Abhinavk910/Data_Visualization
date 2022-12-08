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
DATA_PATH = PATH.joinpath('../Week_22_sup_contribution/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("Plastic Waste Makers Index.xlsx"))

mean_assets = df['No. of assets'].mean()
mean_contribution = df['Total contribution to SUP waste'].mean()

color_pallete = ["#6EC1E4", "#A3A9AC"]
size_tobede = [20, 10]
final_color = df.apply(lambda x: color_pallete[0] if x[2]>mean_assets and x[6] > mean_contribution else color_pallete[1], axis=1)
final_size = df.apply(lambda x: size_tobede[0] if x[2]>mean_assets and x[6] > mean_contribution else size_tobede[1], axis=1)

fig1 = go.Figure(data=go.Scatter(y=df['No. of assets'],
                                x=df['Total contribution to SUP waste'],
                                mode='markers',
                                marker=dict(color = final_color, size = final_size, line_width=1,opacity =0.9, line_color = 'black'),
                                customdata=df.iloc[:,[1,4,5]],
                                hovertemplate =
                                            '<b>%{customdata[0]}</b>'+
                                            '<br>Number of Assets: %{y:.0f}'+
                                            '<br>Total SUP waste(MMT):-  %{x}'+
                                            '<br>Flexible SUP Waste(MMT) :-  %{customdata[1]:.1f}'+
                                            '<br>Rigit SUP Waste(MMT) :-  %{customdata[2]:.1f}<extra></extra>',
                               ))

fig1.add_vline(x=mean_contribution,
              fillcolor="#667175", opacity=0.5,
              layer="below", line_width=2,
              line_color = '#667175',
              line_dash="dash",#'solid', 'dot', 'dash', 'longdash', 'dashdot','longdashdot'
              annotation_text="Average",
              annotation_position="top left"
             )
fig1.add_hline(y=mean_assets,
              fillcolor="#667175", opacity=0.5,
              layer="below", line_width=2,
              line_color = '#667175',
              line_dash="dash",#'solid', 'dot', 'dash', 'longdash', 'dashdot','longdashdot'
              annotation_text="Average",
              annotation_position="bottom right",
             )
fig1.add_annotation(
        x=2,y=60,
        xref="x",yref="y",
        text="20",
        showarrow=False,
        font=dict(family="Rockwell, monospace",size=30,color="#6EC1E4"),
#         align="center",arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="#636363",
        ax=20, ay=-30,
        bordercolor="#667175",borderwidth=2,borderpad=4,bgcolor="#667175",opacity=0.8
        )

fig1.update_layout(
    plot_bgcolor = '#192930',
    paper_bgcolor = '#192930',
    hoverlabel=dict(
#         bgcolor="white",
        font_size=15,
        font_family="Rockwell",
        align = 'auto',
    ),
    title = dict(
        text = '<Span style="color:#6EC1E4;font-size:25px;">20 </span>'+
        "Companies account for the Heighest<br>Production and Heighest Number of Assets",
        font=dict(size=25,family='Rockwell, monospace', color='#C1C5C7'),
    ),
    xaxis = dict(
        title=dict(
            text = '2019,MMT Total contribution to SUP waste',
            font=dict(size=18, family='Rockwell, monospace', color='#8C8C8C'),
            standoff = 20
        ),
        showline=True,
        linecolor='#667175',
        color = "#667175",
        showgrid=False,
        zeroline =False,
        ticks='outside',
        tickwidth=1.5,


    ),
    yaxis = dict(
        title=dict(
            text = 'Number of assets',
            font=dict(size=18, family='Rockwell, monospace', color='#8C8C8C'),
            standoff = 20
        ),
        showline=True,
        linecolor='#667175',
        showgrid=False,
        zeroline =False,
        color = "#667175",
        ticks='outside',
        tickwidth=1.5,
    )
)


fig2 = go.Figure(data=go.Scatter(x=df['Flexible format contribution to SUP waste'],
                                y=df['Rigid format contribution to SUP waste'],
                                mode='markers',
                                marker=dict(color = final_color, size = final_size, line_width=1,opacity =0.9, line_color = 'black'),
                                customdata=df.iloc[:,[1,4,5]],
                                hovertemplate =
                                            '<b>%{customdata[0]}</b>'+
                                            '<br>Number of Assets: %{y:.0f}'+
                                            '<br>Flexible SUP Waste(MMT) :-  %{customdata[1]:.1f}'+
                                            '<br>Rigit SUP Waste(MMT) :-  %{customdata[2]:.1f}<extra></extra>',
                               ))

fig2.update_layout(
    plot_bgcolor = '#192930',
    paper_bgcolor = '#192930',
    hoverlabel=dict(
#         bgcolor="white",
        font_size=15,
        font_family="Rockwell",
        align = 'auto',
    ),
    title = dict(
        text = '<Span style="color:#6EC1E4;font-size:25px;">Top 20 </span>'+
               '<Span style="color:#C1C5C7;">polymer producers generating <br>single-use plastic waste</span>',
        font=dict(family='Rockwell, monospace', color='black', size=25),
    ),
    xaxis = dict(
        title=dict(
            text = 'MMT Flexible format contribution to SUP waste',
            font=dict(size=15, family='Rockwell, monospace', color='#8C8C8C'),
            standoff = 20
        ),
        showline=True,
        linecolor='#667175',
        color = "#667175",
        showgrid=False,
        zeroline =False,
        ticks='outside',
        tickwidth=1.5,


    ),
    yaxis = dict(
        title=dict(
            text = 'MMT Rigid format contribution to <br>SUP waste',
            font=dict(size=15, family='Rockwell, monospace', color='#8C8C8C'),
            standoff = 20
        ),
        showline=True,
        linecolor='#667175',
        showgrid=False,
        zeroline =False,
        color = "#667175",
        ticks='outside',
        tickwidth=1.5,
    )
)


heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

mmw22_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 22', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.Span(' Top companies Single Use Plastic contribution',
                          style={'color': heading_color[0]}),
                ' in 2019'
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    html.Div([
        html.H1('The Plastic Waste Makers Index', style={
                'color': "white", "text-align": "center"}, className='mb-5'),
        html.Div([
            html.Div([
                html.P('In 2019, just 20 polymer producers accounted for more than half of all single-use plastic \
                waste generated globally - and the top 100 accounted for 90 percent'
                       ,className="mt-4",style={'color': text_heading_color[0],'font-size':"25px" }),
                html.P("ExxonMobil and Dow - both based in the USA - top the list, followed by China-based Sinopec, \
                with these three companies together accounting for 16 percent of global single-use plastic waste. Of\
                approximately 300 polymer producers operating globally, a small fraction hold the fate of the world's\
                plastic crisis in their hands: their choice, to continue to produce virgin polymers rather than recycled \
                polymers, will have massive repercussions on how much waste is collected, managed and leaks into the environment.",
                       style={'color': text_color[0], }
                )
            ], style={'width': '500px'}),
            html.Div([
                dcc.Graph(id='mmw21_1', figure=fig1,
                          config={'displayModeBar': False})
            ], style={'width': "50%"})
        ], className='d-flex flex-row justify-content-between'),
        html.Div([
            html.Div([
                dcc.Graph(id='mmw21_2', figure=fig2,
                          config={'displayModeBar': False})
            ], style={'width': "50%"}),
            html.Div([
                html.P('Eleven of the top 20 polymer producers are based in Asia(five in China), with a further four in \
                Europe, three in North America, one in Latin America, and one in the Middle East.',
                      className="mt-4",style={'color': text_color[0],'font-size':"" }),
                html.P('Four of the top 20 companies produce exclusively PET, a polymer which is mainly used to make \
                bottles and other rigid plastics. These companies likely generate less plastic pollution than their \
                peers, as rigid plastic have higher rates of collecion and recycling than lower-value, flexible plastics.',
                       className="mt-4",style={'color': text_color[0],'font-size':"" })

            ], style={'width': "50%"}),

        ], className='d-flex flex-row justify-content-between mt-5')
    ], style={'background': '#192930', 'width': '1200px', 'min-height': '80vh',
              "border-radius": "50px","box-shadow": "15px 0px 15px -10px rgba(0,0,0,0.75)"}, className='p-5'),
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
