import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,  Input, Output, State
import plotly.express as px
from plotly import graph_objs as go
import pathlib

from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_15_NBA_Fouls/').resolve()

df = pd.read_csv(DATA_PATH.joinpath('NBA Referee Stats processed.csv'))
to_retain = ['Total fouls', 'Shooting', 'Loose ball', 'Offensive charge', 'Technical', 'Defensive goaltending', 'Defensive 3 seconds', 'Offensive'  ]




nba_layout = dbc.Container(
    [

        dbc.Row(
            [
                dbc.Col([
                        html.H2(["Fouls Called By NBA Referee"], className = "mt-1"),
                        html.Hr(),
                        html.P(['Referees in the NBA are trained professionals. Sure, like all humans they make some mistakes, but they do not call fouls because they think it is one. They know the rule book inside and out so they look for key events that indicate a foul has been made. Lets check Foul Called by Referee in last 4 Seasons.'], className = 'lead small'),
                        html.Hr(),
                        html.Div([
                            html.Div([
                                html.P('Select Season',style = {'font-size': '20px', 'text-align': 'center'}),
                                dcc.Dropdown(
                                    id='nba_dropdown1',
                                    options=[{'label': i, 'value': i} for i in df.Season.unique()],
                                    value='2016-17',
                                    style = {'width': '150px'},
                                    clearable=False
                    #                 placeholder = 'Select Season'
                                ),
                            ], className = "d-flex flex-column m-1 p-1 align-content-center"),
                            html.Div([
                                html.P('Select Refree', style = {'font-size': '20px', 'text-align': 'center'}),
                                dcc.Dropdown(
                                    id='nba_dropdown2',
                                    options=[{'label': i, 'value': i} for i in df.Referee.unique()],
                                    value='Eric Lewis',
                                    style = {'width': '200px'},
                                    clearable=False
                    #                 placeholder = 'Select Referee'
                                ),
                            ], className = 'd-flex flex-column m-1 p-1 justify-content-center')
                        ], className = "d-flex justify-content-around", style = {}),
                        html.Hr(),
                         dcc.Graph(id='nba-foul_2',config={'editable': False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','sendDataToCloud','ditInChartStudio','zoom2d','select2d','drawclosedpath', 'eraseshape','zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d','toggleSpikelines']})
                ], md=4),
                dbc.Col(children=dcc.Graph(id='nba-foul_11',
                                            config={'displayModeBar': False},
                                        ), md = 8)
            ],
            align="center",
        ),
        html.Hr(),
        dbc.Row([
                html.Div([
                    html.P(['Data Source: The Unofficial NBA Ref Ball Database']),
                    html.P('Credit: @owenlhjphillips'),
                    html.A(html.P('Get Data'), href='https://data.world/makeovermonday/2021w15', target = "_blank")
                ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                html.Div([
                    html.P("Developed By: "),
                    html.Div([
                        html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                        href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                    ])
                ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
        ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})

    ],
    fluid=True, style = {'background': '#FFFAF0'}
)


@app.callback(
    Output('nba-foul_2','figure'),
    [Input('nba_dropdown2','value'),Input('nba_dropdown1','value'),]
)
def plotbarnba(referee, year):
    vv = df[(df.Referee == referee)]
    fig2 = px.bar(
        data_frame=vv,
        x="foul_called",
        y="foul_type",
        opacity=0.9,                  # set opacity of markers (from 0 to 1)
        orientation="h",              # 'v','h': orientation of the marks
        barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                      # in 'group' mode, bars are placed beside each other.
                                      # in 'relative' mode, bars are stacked above (+) or below (-) zero.
        text='foul_called',            # values appear in figure as text labels
        hover_name='Referee',   # values appear in bold in the hover tooltip
        hover_data=['foul_per_game'],    # values appear as extra data in the hover tooltip
        # custom_data=['others'],     # invisible values that are extra data to be used in Dash callbacks or widgets

        log_x=True,                 # x-axis is log-scaled
        labels={"foul_type":"Types of Foul", "foul_called": 'Number of Foul Called(Log Scale)'},           # map the labels of the figure
        title='Foul Called', # figure title
        width=400,                   # figure width in pixels
        template='none',            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                      # 'plotly_white', 'plotly_dark', 'presentation',
                                      # 'xgridoff', 'ygridoff', 'gridon', 'none'

        animation_frame='Season',     # assign marks to animation frames
        animation_group='foul_type',         # use only when df has multiple rows with same object
        range_x=[1.5,1000],           # set range of x-axis

    )

    fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 2000
    fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
    fig2.update_layout(uniformtext_minsize=14, uniformtext_mode='hide'),
    fig2.update_traces(texttemplate='%{text:.2s}', textposition='auto', marker_color='#D8D7D4')


    fig2.update_layout(
        title = f'<span style="font-size: 18px;color:red;">{referee} Called Fouls Over the Years</span>',
#         title_size = 20,

        font_size = 10,
        template='xgridoff',
        yaxis=dict(
            fixedrange = True
        ),
        xaxis=dict(
            fixedrange = True
        ),
        margin=dict(
            l=120,
            r=20,
            b=10,
            t=60,
        ),
      showlegend=False,
        paper_bgcolor='#FFFAF0',
        plot_bgcolor='#FFFAF0',
    )
    return fig2





@app.callback(
    Output('nba-foul_11','figure'),
    [Input('nba_dropdown2','value'),Input('nba_dropdown1','value'),]
)
def plotzscore1(referee, year):
    ll = 'Foul call per Game in the Regular Season relative to A League Average Referee'
    kk = 'Amoung Referees that officiated 10 or more games'
    fig = go.Figure(
#                     layout_width=1000,
                    layout_height=850,
                    layout= go.Layout(title=f'<span style="font-size: 30px;color:red;">{referee + " (" + year})</span>' + '<br>' +  f'<span style="font-size: 15px;color:black">{ll}</span>'+ '<br>' +  f'<span style="font-size: 15px;color:black;">{kk}</span>'+'<br>'))

    for i, f_type in enumerate(to_retain):
        fig.add_trace(go.Box(x=df[(df.foul_type == f_type)& (df.Season == year)].z_score,
                         boxpoints='all', # can also be outliers, or suspectedoutliers, or False
                         jitter=1,#d some jitter for a better separation between points
                         pointpos=0, # relative position of points wrt box,
                         fillcolor= 'rgba(255,255,255,0)',
                         line = {'color': 'rgba(255,255,255,0)'},
                         hoveron= 'points',
                         opacity = 0.2,
                         name = f_type,
                         marker = {'color': '#D8D7D4', 'size': 10, 'line':{'width':1,'color':'DarkSlateGrey'}},))

        fig.add_trace(go.Box(x=[df[(df.Referee == referee) & (df.foul_type == f_type)& (df.Season == year)].z_score.tolist()[0]],
                         boxpoints='all', # can also be outliers, or suspectedoutliers, or False
                         jitter=1, # add some jitter for a better separation between points
                         pointpos=0, # relative position of points wrt box,
                         fillcolor= 'rgba(255,255,255,0)',
                         line = {'color': 'rgba(255,255,255,0)'},
                         hoveron= 'points',
                         opacity = 0.8,
                         name = f_type,
                         marker = {'color': '#FE0000', 'size': 15, 'line':{'width':2,'color':'DarkSlateGrey'}},))

        fig.add_annotation(
            x=df[(df.Referee == referee) & (df.foul_type == f_type)& (df.Season == year)].z_score.tolist()[0],y = i+0.1,xref="x",yref = 'y',
            text=f_type, showarrow=True,
            font=dict(family="Courier New, monospace",  size=12, color="#000"),
            align="center",  arrowhead=0,   arrowsize=0.3, arrowwidth=0.1,   arrowcolor="#636363",   ax=2,  ay=-20,
            bordercolor="#c7c7c7",  borderwidth=2, borderpad=4, bgcolor="#fff", opacity=0.8)

    fig.add_vline(
        x=0,
        fillcolor="#000", opacity=0.9,
        layer="above", line_width=1,
        line_dash="dot",
        )
    #
    fig.add_annotation(
            x=-4, y = 3.5, xref="x", yref = 'y', text='Calls Less than Average', showarrow=True,
            font=dict(family="Courier New, monospace", size=16, color="#000"),
            align="center", arrowhead=2, arrowsize=2, arrowwidth=2, arrowcolor="#636363",
            ax=150, ay=0, bordercolor="#c7c7c7", borderwidth=0, borderpad=4, opacity=0.8)

    fig.add_annotation(
            x=4, y = 3.5, xref="x", yref = 'y', text='Calls More than Average', showarrow=True,
            font=dict(family="Courier New, monospace", size=16, color="#000"),
            align="center", arrowhead=2, arrowsize=2, arrowwidth=2, arrowcolor="#636363",
            ax=-150, ay=0, bordercolor="#c7c7c7", borderwidth=0, borderpad=4, opacity=0.8)

    fig.update_layout(
    #     title='Points Scored by the Top 9 Scoring NBA Players in 2012',
        title_x=0.5,
        yaxis=dict(
    #         autorange=True,
    #         showgrid=True,
    #         zeroline=True,
            dtick=1,
            gridcolor='#D8D7D4',
            gridwidth=0.01,
    #         zerolinecolor='rgb(0, 0, 0)',
    #         zerolinewidth=20,
    #         visible=False,
            showticklabels=False,
            fixedrange = True
        ),
        xaxis = dict(
            title = 'Normalized per Game Value (Z_score)',
            zeroline = False,
            zerolinecolor='rgb(0, 0, 0)',
            zerolinewidth=1,
            gridcolor='#D8D7D4',
            gridwidth=0.01,
            range = [-4, 4],
            fixedrange = True
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='#FFFAF0',
        plot_bgcolor='#FFFAF0',
        showlegend=False
    )


    return fig








if __name__ == '__main__':
    app.run_server(debug=True)
