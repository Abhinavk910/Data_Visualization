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
DATA_PATH = PATH.joinpath('../Week_18_Ceos_compensation/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("CEO-Worker Compensation Ratio.xlsx"))

df['Rel - Gran'] = df['Realized CEO compensation'] - df['Granted CEO compensation']
maxormin = df['Rel - Gran'].apply(lambda x: True if x == df['Rel - Gran'].max() or x == df['Rel - Gran'].min() else False)

x = df.Year
y = df['Rel - Gran']
colors = df['Rel - Gran'].apply(lambda x: "crimson" if x> 0 else "#2DBDF3")


mmw18_wiz = dbc.Container([
                dbc.Row([
                    dbc.Col([
                    html.P(['REALIZED ',html.Span("VS.", style = {'font-size': '15px'}), ' GRANTED COMPENSATION FOR CEO',html.Span("S", style = {'font-size': '15px'})],id = 'mmw18_1',className = 'm-0 pt-3', style = {'background': '#DCD2C4',
                    'font-size': '30px','font-weight': 'bold', 'text-align': 'center'}),
                    html.P(["IN 45 OF LAST 55 YEARS, REALIZED COMPENSATION FOR CEO" ,html.Span("S", style = {'font-size': '10px'}),html.Span(" EXCEEDED ",style = {'color':'crimson','font-weight': 'bold'}), "GRANTED COMPENSATION"],className = 'm-0 pb-3', style = {'background': '#DCD2C4', 'text-align': 'center', 'font-size': '20px'}),
                    dcc.Graph(id='mmw18_2',
                                                config={'displayModeBar': False},
                                            )
                    ], md = 12)
                ], className = '', style = {'background': '#DCD2C4',}),
                dbc.Row([
                    dbc.Col([
                        html.P([html.Span('Note: ', style = {'font-weight' : 'bold'}),
                        "Average annual compensation for CEOs at the top 350 U.S. firms ranked by sales is measured in two ways. Both include salary, bonus, and long-term incentive payouts, but the “granted” measure includes the value of stock options and stock awards when they were granted, whereas the “realized” measure captures the value of stock-related components that accrues after options or stock awards are granted by including “stock options exercised” and “vested stock awards.”",
                        html.A('For more info.', href = "https://www.epi.org/publication/ceo-compensation-surged-14-in-2019-to-21-3-million-ceos-now-earn-320-times-as-much-as-a-typical-worker/", target = "_blank")],
                        style = {'background': '#DCD2C4','font-size': '10px'}, className = 'm-0 pb-3')
                    ], md = 8),
                    dbc.Col([
                        html.P([html.Span('Source: ', style = {'font-weight' : 'bold'}),
                        "Authors’ analysis of data from Compustat’s ExecuComp database, the Bureau of Labor Statistics’ Current Employment Statistics data series, and the Bureau of Economic Analysis NIPA tables."],
                        style = {'background': '#DCD2C4','font-size': '10px'}, className = 'm-0 pb-3')
                    ], md = 4)
                ],style = {'background': '#DCD2C4',}),
                dbc.Row([
                            html.Div([
                                html.P(['Makeover Monday Week 18']),
                                html.A(html.P('Get Data'), href='https://data.world/makeovermonday/2021w18', target = "_blank")
                            ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                            html.Div([
                                html.P("Developed By: "),
                                html.Div([
                                    html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                                    href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                                ])
                            ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
                    ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})


], fluid = False)

@app.callback(
    Output('mmw18_2','figure'),
    [Input('mmw18_1','children')]
)
def plotmmw18(text):

# Use the hovertext kw argument for hover text
    fig = go.Figure()
    # print('i am here')
    fig.add_trace(go.Bar(x=x,
                         y=y,
                         marker_color=colors,
                         showlegend=False,
                         text = [abs(int(i)) for i in y],
                         hovertemplate =
                            '&nbsp;<b> %{x}, %{text} </b>&nbsp;<extra></extra>',
                        ))

    for i in range(len(maxormin)):
        if maxormin[i]:
            fig.add_trace(go.Scatter(mode='markers', x=[df.iloc[i, 0]],
                                 y=[df.iloc[i, 3]], marker_symbol=0, marker_color=colors[i],#marker_line_color=,
                                 marker_line_width=0, marker_size=20,
                                     text=[abs(int(df.iloc[i, 3]))],
    #                                  textposition="top center",
                                      hovertemplate = '&nbsp;<b> %{x}, %{text} </b>&nbsp;<extra></extra>',
    #                                  hoverinfo='none', this will disable the hover text
                                     showlegend=True))

            if df.iloc[i, 3] > 0:
                yshift = 20
            else:
                yshift = -20
            fig.add_annotation(x=df.iloc[i, 0],
                               y=df.iloc[i, 3],
                               text=abs(int(df.iloc[i, 3])),
                               showarrow=False,
                               arrowhead=0,
                               yshift=yshift,
    #                            hoverinfo='skip'
                              )


    fig.add_hline(
        y = 0,
        fillcolor="black", opacity=1,
        layer="above", line_width=1,
        line_dash="solid",
        )


    fig.update_layout(title_text="",
                      height = 450,
    #                   width = 800,
                      bargap=0.4,

                      plot_bgcolor = '#DCD2C4',
                      paper_bgcolor = '#DCD2C4',
                      margin=dict(t=10, l=85, r=10, b=60, pad = 0),
                      showlegend = False,
                      xaxis=dict(title=dict(
                                  text = '',
    #                               font=dict(size=18, family='Courier', color='crimson'),
    #                               standoff = 20
                                  ),
                                 range=['1963','2022'],
    #                          mirror=False,
    #                          fixedrange=True,
    #                          tickformat="%b %d,%y",

                                 showticklabels=True,  # this is for toggling x axis label to show or not
                                 showline=False,        # this is for showing line in x axis, it different from zeroline
    #                              linecolor='black',
    #                              linewidth=3,
                                 showgrid=False,

                                 zeroline =False,
    #                              zerolinecolor = 'black',
    #                              zerolinewidth = 0.5,

                                 layer='above traces',

                                 tickmode = 'array',
                                 tickvals = [1970, 1980, 1990, 2000, 2010, 2020],
                                 ticks="",
                                 tickwidth=1.5,
                                 tickcolor='black',
                                 ticklen=10,
                                 fixedrange=True,  # Disabling Pan/Zoom on Axes
                                 tickprefix = "  ",
                                 ticksuffix = "  ",
                                ),
                      yaxis=dict(title=dict(
                                  text = '&#8592; GRANTED MORE     REALIZED MORE &#8594;',
                                  font=dict(size=18, family='Courier'),# color=''),
    #                               standoff = 20
                                  ),
                             range=[-190, 190],
                                 showline = False,
    #                              linecolor='#d9d9d9',
    #                              line_width = 3,
                                 showgrid=False,
                                 fixedrange=True,
                                 zeroline = False,
    #                              zerolinecolor = 'black',
    #                              zerolinewidth = 3,
    #                              ticklen=10,
    #                              layer='above traces',
                                 tickmode = 'array',
                                 ticktext=["0 ", "50 ", "100 ", "150 ", "50 ", "100 ", "150 "],
                                 tickvals = [0, 50, 100, 150, -50, -100, -150],
                                 ticks="",# inside outside " "
    #                              tickwidth=1,
    #                              tickcolor='black',
    #                              ticklen=10,
    #                              tickprefix = "  ",
                             mirror=False),
                       hoverlabel=dict(bgcolor="white",
                                       font_size=12,
                                       font_family="Rockwell")
                     )


    return fig
