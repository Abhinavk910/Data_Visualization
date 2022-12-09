import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,  Input, Output, State
from plotly import graph_objs as go
import pathlib
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_20_beat_animal_unarmed_dumbbell_plot/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("Human vs Animal Fight.xlsx"))
df.Male = df.Male*100
df.Female = df.Female*100
df.sort_values('Male',ascending=False, inplace=True)

mmw20_wiz = dbc.Container([
                dbc.Row([
                    dbc.Col([
                    html.H1('Human vs beast'),
                    html.P([html.Span('Which animal could you beat in a fight? Compared to women, men feel most able to take on medium-sized dogs and geese',
                     style={'font-size': '1.5vw', 'background':''}),
                            ],id = 'mmw20_1',className = 'm-0 pt-1', style = {'background': '',
                    'font-size': '30px','font-weight': 'bold', 'text-align': 'center'}),])], className = 'mt-1'),
                html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
                dbc.Row([
                    dbc.Col([
                       dcc.Graph(id='mmw20_2',  config={'displayModeBar': False},)
                    ], className="d-flex flex-column align-items-center")

                ]),
                html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
                dbc.Row([
                            html.Div([
                                html.P(['Makeover Monday Week 20']),
                                html.A(html.P('Get Data'), href='https://data.world/makeovermonday/2021w20', target = "_blank")
                            ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                            html.Div([
                                html.P("Developed By: "),
                                html.Div([
                                    html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                                    href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                                ])
                            ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
                    ], className = ' d-flex justify-content-around align-content-center text-muted small mb-1', style = {'min-height': '30px'})


], fluid = False, className="d-flex flex-column justify-content-around", style= {'background':"white", 'height': "100vh"})


@app.callback(
    Output('mmw20_2','figure'),
    [Input('mmw20_1','children')]
)
def plotbarnba(text):
    labels = df.Animal.tolist()


    x_data = df.iloc[:, [2,3]].to_numpy()
    fig = go.Figure()
    for i in range(0, df.shape[0]):
    #     print(j, i)
        fig.add_trace(go.Scatter(x=x_data[i], y=[i+1, i+1], mode='lines',
            name=labels[i],
            line=dict(color='rgb(204, 204, 204)', width=10),
    #         connectgaps=True,
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[i+1, i+1],
            mode='markers',
            marker=dict(color=['rgb(137, 123, 211)','rgb(91, 171, 171)' ], size=10)
        ))

    fig.update_traces(
       # hovertemplate=None,
       hoverinfo='skip'
    )
    fig.update_layout(
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
        xaxis=dict(
        fixedrange = True,
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            linecolor='rgb(204, 204, 204)',
    #         linewidth=2,
    #         ticks='outside',
    #         tickfont=dict(
    #             family='Arial',
    #             size=12,
    #             color='rgb(82, 82, 82)',
    #         ),
        ),
        yaxis=dict(
        fixedrange = True,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor="#EBEBEB",
            showticklabels=True,
            gridcolor="#EBEBEB",
            tickmode = 'array',
            ticktext=df.Animal.tolist(),
            tickvals = [1,2, 3, 4, 5,6,7,8,9,10,11,12,13,14, 15],
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=120,
            r=0,
            t=0,
        ),
        showlegend=False,

    )

    annotations = []


    # Title
    annotations.append(dict(xref='paper', yref='paper', x=-0.2, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text='Which of the following animals, if any, do yo think you could beat in a fight if you were unarmed? %',
                                  font=dict(family='Arial',
                                            size=15,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    # Source
    for i in range(0, df.shape[0]):
        if x_data[i][0] > x_data[i][-1]:

            annotations.append(dict(
                    text=str(int(x_data[i][0])),
                    y = i+1,
                    x = x_data[i][0]+2.5,
                    showarrow=False,
                ))
            annotations.append(dict(
                    text=str(int(x_data[i][-1])),
                    y = i+1,
                    x = x_data[i][-1]-2.5,
                    showarrow=False,
                ))
        else:
            annotations.append(dict(
                    text=str(int(x_data[i][0])),
                    y = i+1,
                    x = x_data[i][0]-2.5,
                    showarrow=False,
                ))
            annotations.append(dict(
                    text=str(int(x_data[i][-1])),
                    y = i+1,
                    x = x_data[i][-1]+2.5,
                    showarrow=False,
                ))


    annotations.append(dict(xref='paper', yref='paper', x=0.01, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='YouGov',
                                  font=dict(family='Raleway',
                                            size=20,
    #                                         bold = True,
                                            color='#D87570'),
                                  showarrow=False))
    annotations.append(dict(xref='paper', yref='paper', x=0.9, y=-0.13,
                                  xanchor='center', yanchor='top',
                                  text='April 12-13,2021',
                                  font=dict(family='Raleway',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))

    annotations.append(dict(
            x=x_data[-1][-1], y = df.shape[0], xref="x", yref = 'y', text='Women', showarrow=True,
            font=dict(family="Courier New, monospace", size=15, color="rgb(91, 171, 171)"),
            align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="#636363",
            ax=-30, ay=-25, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))
    annotations.append(dict(
            x=x_data[-1][0], y = df.shape[0], xref="x", yref = 'y', text='Men', showarrow=True,
            font=dict(family="Courier New, monospace", size=12, color="rgb(137, 123, 211)"),
            align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="#636363",
            ax=+30, ay=-25, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))

    fig.update_layout(annotations=annotations)


    return fig
