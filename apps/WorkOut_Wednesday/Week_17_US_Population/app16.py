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
DATA_PATH = PATH.joinpath('../Week_17_US_Population/').resolve()

df = pd.read_csv(DATA_PATH.joinpath("2019_Population_Estimates.csv"))
df['birth_year'] = 2019 - df.AGE
dff = df[df.SEX == 'Total']
dff = dff.sort_values('birth_year')



bins = [1918,1927, 1945, 1964, 1980, 1996, 2012, 2019]
labels = ["#00C3A9","#00AD90","#00C3A9","#00AD90","#00C3A9","#00AD90","#00C3A9"]
colors = pd.cut(dff.birth_year, bins=bins, labels=labels, ordered=False)




www17_wiz = dbc.Container([
                dbc.Row([
                    dbc.Col([
                    html.P(['BY BIRTH YEAR'],id = 'www17_2',className = 'm-0 pt-3', style = {'background': '#DCD2C4', 'text-align': 'center'}),
                    html.P(['GENERATION POPULATIONS'],className = 'm-0 p-0', style = {'background': '#DCD2C4', 'text-align': 'center', 'font-size': '25px'}),
                    html.P(["WITH RANKINGS BY MOST NUMBER OF PEOPLE ALIVE"],className = 'm-0 pb-3', style = {'background': '#DCD2C4', 'text-align': 'center', 'font-size': '15px'}),
                    dcc.Graph(id='www17_1',
                                                config={'displayModeBar': False},
                                            )
                    ], md = 12)
                ], className = ''),
                dbc.Row([
                            html.Div([
                                html.P(['Workour Wednesday Week 17']),
                                html.A(html.P('Get Data'), href='https://data.world/kcmillersean/2019-population-estimates', target = "_blank")
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
    Output('www17_1','figure'),
    [Input('www17_2','children')]
)
def plotbarnba(text):
    x = dff.birth_year
    y = dff['2019 Population']

# Use the hovertext kw argument for hover text
    fig = go.Figure()

    fig.add_trace(go.Bar(x=x,
                         y=y,
                         marker_color=colors,
                        ))
    datetoannote = [1927.5, 1945.5, 1964.5, 1980.5, 1996.5, 2012.5]
    for i in datetoannote:
        fig.add_vline(
                x=i,
                fillcolor="black", opacity=1,
                layer="above", line_width=2,
                line_dash="dot",
                )
        fig.add_annotation(text=str(int(i+1)),
                          xref="x", yref="y",textangle=270,
                          x=i+1, y=4800000, showarrow=False)



    # ranktoannote = {1928, }
    y_toadd = 6600000
    y_toadd2 = 100000
    fig.add_annotation(text="#7<br><b>GREATEST <br> GENERATION</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=1920, y=y_toadd, showarrow=False)
    fig.add_annotation(text="#6<br><b>SILENT <br> GENERATION</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=1937, y=y_toadd, showarrow=False)
    fig.add_annotation(text="#2<br><b>BOOMERS</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=1955, y=y_toadd+y_toadd2, showarrow=False)
    fig.add_annotation(text="#4<br><b>GENERATION X</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=1973, y=y_toadd+y_toadd2, showarrow=False)
    fig.add_annotation(text="#1<br><b>MILLENNIALS</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=1989, y=y_toadd+y_toadd2, showarrow=False)
    fig.add_annotation(text="#3<br><b>GENERATION Z</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=2005, y=y_toadd+y_toadd2, showarrow=False)
    fig.add_annotation(text="#5<br><b>GENERATION <br> ALPHA</b><br>",
                      xref="x", yref="y",textangle=0,font=dict(family="Courier",size=16,color = 'black'),align = 'center',
                      x=2020, y=y_toadd, showarrow=False)
    fig.add_annotation(text="1.7M  |  0.5%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=1920, y=5850000, showarrow=False)
    fig.add_annotation(text="23.2M  |  7.1%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=1937, y=5850000, showarrow=False)
    fig.add_annotation(text="71.6M  |  21.8%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=1955, y=5850000, showarrow=False)
    fig.add_annotation(text="65.2M  |  19.9%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=1973, y=5850000, showarrow=False)
    fig.add_annotation(text="72.1M  |  22.0%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=1989, y=5850000, showarrow=False)
    fig.add_annotation(text="66.9M  |  20.4%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=2005, y=5850000, showarrow=False)
    fig.add_annotation(text="27.6M  |  8.4%",
                      xref="x", yref="y",textangle=0,font=dict(family="Times New Roman",size=18,color = 'black'),
                      x=2020, y=5850000, showarrow=False)
    fig.add_annotation(text=" Total  %POP.",font=dict(family="Courier New, monospace",size=11,color = 'black'),
                      xref="x", yref="y",textangle=0,align="center",
                      x=1920, y=5500000, showarrow=False)
    fig.add_annotation(text="Those born before<br> 1920 were grouped<br> together",font=dict(family="Courier New, monospace",size=11,color = 'black'),
                      xref="x", yref="y",textangle=0,align="right",
                      x=1919, y=100322, showarrow=True)

    fig.update_layout(title_text="",
                      height = 650,
    #                   width = 800,
                      bargap=0.0001,

                      plot_bgcolor = '#DCD2C4',
                      paper_bgcolor = '#DCD2C4',
                      margin=dict(t=10, l=60, r=60, b=60, pad = 0),
                      showlegend = False,
                      xaxis=dict(title=dict(
                                  text = '',
                                  font=dict(size=18, family='Courier', color='crimson'),
                                  standoff = 20
                                  ),
                                 range=['1915','2020'],
    #                          mirror=False,
    #                          fixedrange=True,
    #                          tickformat="%b %d,%y",

                                 showticklabels=True,  # this is for toggling x axis label to show or not
                                 showline=True,        # this is for showing line in x axis, it different from zeroline
                                 linecolor='black',
                                 linewidth=3,
                                 showgrid=False,

                                 zeroline =False,
                                 zerolinecolor = 'black',
                                 zerolinewidth = 0.5,

                                 layer='above traces',

                                 tickmode = 'array',
                                 tickvals = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2019],
                                 ticks="outside",
                                 tickwidth=1.5,
                                 tickcolor='black',
                                 ticklen=10,
                                 fixedrange=True,  # Disabling Pan/Zoom on Axes
                                 tickprefix = "  ",
                                 ticksuffix = "  ",
                                ),
                      yaxis=dict(title='',
    #                          range=[0, 4500],
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
                                 ticktext=[0, "1 ", "2 ", "3 ", "4 "],
                                 tickvals = [0, 1000000, 2000000, 3000000, 4000000],
                                 ticks="inside",
                                 tickwidth=1,
                                 tickcolor='black',
                                 ticklen=10,
    #                              tickprefix = "  ",
                             mirror=False),
                       hoverlabel=dict(bgcolor="white",
                                       font_size=12,
                                       font_family="Rockwell")
                     )
    fig.update_traces( marker_line_color='#DCD2C4',
                      marker_line_width=0.05, opacity=0.5)

    fig.add_annotation(text="BIRTH YEAR",
                  xref="paper", yref="paper",
                  x=0.01, y=-0.09, showarrow=False)
    fig.add_annotation(text="MILLION PEOPLE",
                xref="paper", yref="paper",
                x=-0.02, y=0.65, showarrow=False)
    fig.add_annotation(text="Compiled from population estimates from the United States Census Bureau for July 2019",
                  xref="paper", yref="paper",font=dict(family="Courier",size=11,color = 'black'),
                  x=1.05, y=-0.12, showarrow=False)


    return fig
