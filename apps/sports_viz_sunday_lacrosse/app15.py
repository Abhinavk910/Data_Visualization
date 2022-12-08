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
DATA_PATH = PATH.joinpath('../sports_viz_sunday_lacrosse/').resolve()

dff = pd.read_csv(DATA_PATH.joinpath('processed.csv'))

to_melt = ['Win', 'Loss', 'Goals For', 'Goals Against', 'Goal Differential']

win = pd.read_csv(DATA_PATH.joinpath('processed_win.csv'))


sm4_wiz = dbc.Container([


    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H1(' NCAA D1 LACROSSE',style = {'font-size': '30px', 'text-align': 'center', 'color':'#F5F5F5'}),
                html.P("The NCAA D1 LACROSSE championship tournament decides the annual top men's and women's team. Here Team Stats from 2015-2019 represented, with team history of winning this championship.",
                      className = 'm-1 p-1',style = {'color':'#F5F5F5'}),
                # html.Hr(style = {'background': 'black', 'width': "100%"}),
                dbc.Card([
                    dbc.CardHeader('Select Gender', className = 'mr-3', style = {'width': '150px', 'color':"#F5F5F5"}),
                    dcc.RadioItems(id='sm4-radio-1',
                               options=[{'label': i, 'value': i} for i in ['Male', 'Female']],
                               value='Male',
                               labelClassName = 'radioitem ml-3 mr-4',
                               className = 'radio mt-2',
                               style = {'color':"#F5F5F5"}
                               )
                ], className = 'd-flex flex-row m-1 p-0', style = {"background" :'rgb(0,0,0, 0.1)'}),
                dbc.Card([
                    dbc.CardHeader('Select Team', className = 'mr-3', style = {'width': '150px', 'color':"#F5F5F5"}),
                    dcc.Dropdown(
                        id='sm4-dropdown-1',
#                         options=[{'label': i, 'value': i} for i in ff_state],
#                         value='California',
                        style = {'width': '200px', 'height':'30px'},
                        clearable=False,
                        className = 'ml-3 mt-1 '
                    ),
                ], className = 'd-flex flex-row  m-1 p-0',style = {"background" :'rgb(0,0,0, 0.1)'}),
                dbc.Card([
                    dbc.CardHeader('Select Year', className = 'mr-3', style = {'width': '150px', 'color':"#F5F5F5"}),
                    # html.P('Select Year', className = 'ml-3 mr-3 mt-1'),
                    dcc.Dropdown(
                            id='sm4-dropdown-2',
                            options=[{'label': i, 'value': i} for i in dff.Year.unique()],
                            value='2019',
                            style = {'width': '200px', 'height':'30px'},
                            clearable=False,
                            className = 'ml-3 mt-1',
                        ),
                ], className = 'd-flex flex-row m-1 p-0',style = {"background" :'rgb(0,0,0, 0.1)'}),
                html.Hr(style = {'background': 'black', 'width': "100%"}),
                 html.Div([
                     dbc.Button("Win", className="mr-1", style = {'height':"20px",'backgroundColor':'#29A1A2', 'font-size': '10px','text-align': 'center'}),#"#29A1A2", "#A88A90", "#5D625F"
                     dbc.Button("Runner Up", className="mr-1",  style = {'height':"20px",'backgroundColor':'#A88A90','font-size': '10px', 'text-align': 'center'}),
                     dbc.Button("Lost or not paricipated", className="mr-1",  style = {'height':"20px",'backgroundColor':'#5D625F','font-size': '10px','text-align': 'center'}),
                 ], className="d-flex flex-row justify-content-center"),
                dcc.Graph(id='sm4-wiz-2',config={'displayModeBar': False},
              figure={}, style = {'height':'200px'} ),
            ], style = {"background" :'rgb(0,0,0, 0.5)'}),


        ], sm=12, md=4, style = {"background" :'rgb(0,0,0, 0.1)'} ),
        dbc.Col([
            dcc.Graph(id='sm4-wiz-1',config={'displayModeBar': False},
                  figure={}, ),
        ], sm=12, md=8, style = {"background" :'rgb(0,0,0, 0.5)'})
    ], className = 'pt-2'),



    dbc.Row([
        html.Hr(style = {'background': 'black', 'width': "100%"}),
    ]),
    dbc.Row([

                html.Div([
                    html.P('Sports Viz Sunday - Month 4',style = {'color':'#F5F5F5'}),
                    html.A(html.P('Get Data'), href='https://10d9b011-755b-4b59-9f64-dbfb2ae95d87.filesusr.com/ugd/0c24ab_fb44eb1802fa4fdca4a1fc008f2d92ff.xlsx?dn=NCAA_D1_Lacrosse.xlsx', target = "_blank")
                ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                html.Div([
                    html.P("Developed By: ",style = {'color':'#F5F5F5'}),
                    html.Div([
                        html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                        href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                    ])
                ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
        ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})

], fluid = True, className = 'dashboard_lacrosse')



@app.callback(
    [
    Output('sm4-dropdown-1','options'),
    Output('sm4-dropdown-1','value'),
    ],
    [Input('sm4-radio-1','value')]
)
def populatedropdown(gender):

    df = dff[dff.gender == gender]
    options = [{'label': i, 'value': i} for i in df.Team.unique()]
    value = 'Virginia'
    return options, value


@app.callback(

    Output('sm4-wiz-1','figure'),
    [
        Input('sm4-dropdown-1','value'),
        Input('sm4-dropdown-2','value'),
        Input('sm4-radio-1', 'value')
    ]
)
def populatefig(team, year, gender):
    year = int(year)
    fig = go.Figure( layout_height=640,
                    layout= go.Layout(title=f'<span style="font-size: 30px;color:red;">{team + " (" + str(year)})</span>' + '<br>'))
    for i, f_type in enumerate(to_melt):
        fig.add_trace(go.Box(x=dff[(dff.variable == f_type) & (dff.Year == year)&(dff.Team != team)&(dff.gender == gender)].z_score,
                         boxpoints='all', # can also be outliers, or suspectedoutliers, or False
                         jitter=1,#d some jitter for a better separation between points
                         pointpos=0, # relative position of points wrt box,
                         fillcolor= 'rgba(255,255,255,0)',
                         line = {'color': 'rgba(255,255,255,0)'},
                         hoveron= 'points',
                         text=dff[(dff.variable == f_type) & (dff.Year == year)&(dff.Team != team)&(dff.gender == gender)].Team,
                         hovertemplate='%{text}',
                         opacity = 0.5,
                         name = f_type,
                         marker = {'color': '#D8D7D4', 'size': 10, 'line':{'width':1,'color':'DarkSlateGrey'}}
                             ))

        fig.add_trace(go.Box(x=[dff[(dff.Team == team ) & (dff.variable == f_type)  & (dff.Year == year)&(dff.gender == gender)].z_score.tolist()[0]],
                         boxpoints='all', # can also be outliers, or suspectedoutliers, or False
                         jitter=1, # add some jitter for a better separation between points
                         pointpos=0, # relative position of points wrt box,
                         fillcolor= 'rgba(255,255,255,0)',
                         line = {'color': 'rgba(255,255,255,0)'},
                         text = [team],
                         hovertemplate='%{text}',
                         hoveron= 'points',
                         opacity = 0.8,
                         name = f_type,
                         marker = {'color': '#FE0000', 'size': 15, 'line':{'width':2,'color':'DarkSlateGrey'}},))

        fig.add_annotation(
            x=dff[(dff.Team == team ) & (dff.variable == f_type)  & (dff.Year == year)&(dff.gender == gender)].z_score.tolist()[0],y = i+0.1,xref="x",yref = 'y',
            text=f_type, showarrow=True,
            font=dict(family="Courier New, monospace",  size=12, color="#000"),
            align="center",  arrowhead=0,   arrowsize=0.3, arrowwidth=0.1,   arrowcolor="#636363",   ax=2,  ay=-30,
            bordercolor="#c7c7c7",  borderwidth=2, borderpad=4, bgcolor="#fff", opacity=0.8)

    fig.add_vline(
        x=0,
        fillcolor="#000", opacity=0.9,
        layer="above", line_width=1,
        line_dash="dot",
        )

    fig.add_annotation(
            x=-5, y = 1.5, xref="x", yref = 'y', text='Less than Average', showarrow=True,
            font=dict(family="Courier New, monospace", size=12, color="white"),
            align="center", arrowhead=1, arrowsize=1, arrowwidth=1, arrowcolor="#636363",
            ax=120, ay=0, bordercolor="#c7c7c7", borderwidth=0, borderpad=4, opacity=0.8)

    fig.add_annotation(
            x=5, y = 1.5, xref="x", yref = 'y', text='More than Average', showarrow=True,
            font=dict(family="Courier New, monospace", size=12, color="white"),
            align="center", arrowhead=1, arrowsize=1, arrowwidth=1, arrowcolor="#636363",
            ax=-120, ay=0, bordercolor="#c7c7c7", borderwidth=0, borderpad=4, opacity=0.8)

    fig.update_layout(
        title_x=0.5,
        yaxis=dict(
    #         autorange=True,
    #         showgrid=True,
    #         zeroline=True,
            dtick=1,
            gridcolor='rgb(0, 0, 0, 0.1)',
            gridwidth=0.01,
    #         zerolinecolor='rgb(0, 0, 0)',
    #         zerolinewidth=20,
    #         visible=False,
            showticklabels=False
        ),
        xaxis = dict(
            title = 'Normalized per Game Value (Z_score)',
            # font = dict(
            #     family = "PT Sans Narrow",
            #     size = 12,
            color = 'white',
            zeroline = False,
            zerolinecolor='rgb(0, 0, 0, 0.1)',
            zerolinewidth=1,
            gridcolor='rgb(0, 0, 0, 0.1)',
            gridwidth=0.01,
            range = [-5, 5]
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor = 'rgb(0,0,0, 0.1)',
        plot_bgcolor = 'rgb(0,0,0, 0.1)',
        showlegend=False
    )

    return fig

@app.callback(

    Output('sm4-wiz-2','figure'),
    [
        Input('sm4-dropdown-1','value'),
        Input('sm4-dropdown-2','value'),
        Input('sm4-radio-1', 'value')
    ]
)
def populatefig2sm4(team, year, gender):
    nn = np.resize(np.arange(1971, 2020), (7,7))
    dff = win[win.gender == gender]
    colors = ["#29A1A2", "#A88A90", "#5D625F"]
    color_list = []
    for i, row in dff.iterrows():
        if row[1] == team:
            color_list.append(colors[0])
        elif row[2] == team:
            color_list.append(colors[1])
        else:
            color_list.append(colors[2])

    co = np.array(color_list)
    co = np.resize(co, (7,7))


    fig = go.Figure(data=[go.Table(
      header=dict(
        values=[""],
        line_color='rgb(0,0,0, 0.1)', fill_color='rgb(0,0,0, 0.1)',
        align='center',font=dict(color='black', size=1), height = 0
      ),
      cells=dict(
        values=nn,
        line_color=co,
        fill_color=co,
        align='center', font=dict(color='white', size=8)
        ))
    ])
    fig.update_layout(
        title=dict(
        text = f'Compionship won by {team}<br> over the Years',
        font = dict(
            family = "PT Sans Narrow",
            size = 20,
            color = '#F5F5F5'),
        ),
        title_x=0.5,
        title_y=0.9,

#         yaxis=dict(),
#         xaxis = dict(),
        margin=dict(l=10, r=10, b=0, t=80),
        paper_bgcolor = 'rgb(0,0,0, 0.1)',
        plot_bgcolor = 'rgb(0,0,0, 0.1)',
        height = 330
    )


    return fig
