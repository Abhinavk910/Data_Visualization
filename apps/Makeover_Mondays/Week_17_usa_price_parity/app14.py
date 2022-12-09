import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html,  Input, Output, State
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
DATA_PATH = PATH.joinpath('../Week_17_usa_price_parity/').resolve()

df = pd.read_csv(DATA_PATH.joinpath('processed.csv'))
ff_state = df.GeoName.unique().tolist()
ff_state.remove('United States')

def color(x, select):
    if x in select:
        return '#108080'
    elif x == 'United States':
        return 'black'
    else:
        return '#B9AFAB'

mmw17_wiz =dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Div([
                html.H2('How Does Price Parity Compare Across THE UNITED STATES?', style = {'font_size': '150px'})
                ]),
            ],className = 'm-2 p-2'),
            dbc.Card([
                html.Div([
                    html.P('Highlight A State', style = {'font-size': '15px', 'text-align': 'center'}, className = 'mr-3 mt-2'),
                    dcc.Dropdown(
                        id='mmw17-dropdown-1',
                        options=[{'label': i, 'value': i} for i in ff_state],
                        value='California',
                        style = {'width': '200px'},
                        clearable=False
                    ),
                ], className = 'd-flex')
            ],className = 'm-2 p-2'),
            dbc.Card([
                html.P('All Items', className = 'ml-3 mt-2'),
                dcc.Slider(id='mmw17-slider-1',step=None,included=False),
                html.P('Goods', className = 'ml-3 mt-2'),
                dcc.Slider(id='mmw17-slider-2',step=None,included=False),
                html.P('Rents', className = 'ml-3 mt-2'),
                dcc.Slider(id='mmw17-slider-3',step=None,included=False),
                html.P('Other', className = 'ml-3 mt-2'),
                dcc.Slider(id='mmw17-slider-4',step=None, included=False)

            ], className = 'm-2 p-2')
        ], sm=12, md = 4),
        dbc.Col([
            dcc.Graph(id='mmw17-chart-1',config={'displayModeBar': False},
                  figure={}, ),
        ], sm=12, md = 8)

    ], className = 'm-2 align-content-center'),
    dbc.Row([
        html.Hr(style = {'background': 'black', 'width': "100%"}),
    ]),
    dbc.Row([

                html.Div([
                    html.P(['Data | Superstore']),
                    html.P('MakeOverMonday - Week 17'),
                    html.A(html.P('Get Data'), href='https://data.world/makeovermonday/2021w17', target = "_blank")
                ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                html.Div([
                    html.P("Developed By: "),
                    html.Div([
                        html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                        href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                    ])
                ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
        ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})

], fluid = 'True')

def nn(x):
    if str(x).split(".")[1] == '0':
        return int(x)
    else:
        return x

def mark_update(max, min, value):
    if value == max:
        return {
                nn(min): {'label': str(min), 'style': {'color': '#77b0b1'}},
                nn(max): {'label': str(max), 'style': {'color': '#108080', 'font-size': '15px'}}
            }
    elif value == min:
        # print('sefasf \n\n')
        return {
                nn(min): {'label': str(min), 'style': {'color': '#108080', 'font-size': '15px'}},
                nn(max): {'label': str(max), 'style': {'color': '#f50'}}
            }
    else:
        return {
                nn(min): {'label': str(min), 'style': {'color': '#77b0b1'}},
                nn(value): {'label': str(value),'style': {'color': '#108080','font-size': '15px'}},
                nn(max): {'label': str(max), 'style': {'color': '#f50'}}
            }

@app.callback(
    [Output('mmw17-slider-1','max'),
     Output('mmw17-slider-1','min'),
     Output('mmw17-slider-1','value'),
     Output('mmw17-slider-1','marks'),
     Output('mmw17-slider-2','max'),
     Output('mmw17-slider-2','min'),
     Output('mmw17-slider-2','value'),
     Output('mmw17-slider-2','marks'),
     Output('mmw17-slider-3','max'),
     Output('mmw17-slider-3','min'),
     Output('mmw17-slider-3','value'),
     Output('mmw17-slider-3','marks'),
     Output('mmw17-slider-4','max'),
     Output('mmw17-slider-4','min'),
     Output('mmw17-slider-4','value'),
     Output('mmw17-slider-4','marks'),

     ],
    Input('mmw17-dropdown-1', 'value')
)
def generate_mmweek17wiz(text):
    dff = df[df.GeoName == text]
    req_dic = dff.groupby('Description').agg({'value_x':['min', 'max']}).to_dict()
    min1 = req_dic[('value_x', 'min')]['All items']
    max1 = req_dic[('value_x', 'max')]['All items']
    value1 = float(df[(df.GeoName == text) & (df.years == 2019) & (df.Description == 'All items')]['value_x'])
    marks1=mark_update(max1, min1, value1)
    # {
    #         min1: {'label': str(min1), 'style': {'color': '#77b0b1'}},
    #         value1: {'label': str(value1)},
    #         max1: {'label': str(max1), 'style': {'color': '#f50'}}
    #     }
    min2 = req_dic[('value_x', 'min')]['Goods']
    max2 = req_dic[('value_x', 'max')]['Goods']
    value2 = float(df[(df.GeoName == text) & (df.years == 2019) & (df.Description == 'Goods')]['value_x'])
    marks2=mark_update(max2, min2, value2)
    # {
    #         min2: {'label': str(min2), 'style': {'color': '#77b0b1'}},
    #         value2: {'label': str(value2)},
    #         max2: {'label': str(max2), 'style': {'color': '#f50'}}
    #     }
    min3 = req_dic[('value_x', 'min')]['Rents']
    max3 = req_dic[('value_x', 'max')]['Rents']
    value3 = float(df[(df.GeoName == text) & (df.years == 2019) & (df.Description == 'Rents')]['value_x'])
    marks3=mark_update(max3, min3, value3)
    # {
    #         min3: {'label': str(min3), 'style': {'color': '#77b0b1'}},
    #         value3: {'label': str(value3)},
    #         max3: {'label': str(max3), 'style': {'color': '#f50'}}
    #     }
    min4 = req_dic[('value_x', 'min')]['Other']
    max4 = req_dic[('value_x', 'max')]['Other']
    value4 = float(df[(df.GeoName == text) & (df.years == 2019) & (df.Description == 'Other')]['value_x'])
    marks4=mark_update(max4, min4, value4)
    # print(max1, min1, value1, marks1, max2, min2, value2, marks2, max3, min3, value3, marks3, max4, min4, value4, marks4)


    return max1, min1, value1, marks1, max2, min2, value2, marks2, max3, min3, value3, marks3, max4, min4, value4, marks4


@app.callback(
    Output('mmw17-chart-1','figure'),
    Input('mmw17-dropdown-1', 'value')
)
def generate_week16wiz(text):
    to_select = [text , 'United States']
    df['layer'] = df.GeoName.apply(lambda x: 1 if x in to_select else 0 )
    df.sort_values(['layer', 'years'], inplace = True)
    fig = make_subplots(rows=2, cols=2, start_cell="top-left", subplot_titles=("All Items", "Goods", "Rents", "Other"),
                    vertical_spacing=0.05, shared_xaxes=True, shared_yaxes=False,)

    df1 = df.query('Description == "Rents"')
    df2 = df.query('Description == "All items"')
    df3 = df.query('Description == "Goods"')
    df4 = df.query('Description == "Other"')
    for state in df.GeoName.unique():
        color_use = color(state, text)
        if state in to_select:
            line_width_number = 4
        else:
            line_width_number = 2
        fig.add_trace(go.Scatter(x=df1[df1.GeoName == state].years,
                                 y=df1[df1.GeoName == state]['value_x'],
                                 name=state,
                                 marker_color=color_use,
                                 showlegend=False,
                                 line_width=line_width_number,
                                 mode='lines',
                                 text = [f'&#9660; {abs(i):.1f}% below Country Index' if i < 0 else f'&#9650; {abs(i):.1f}% above Country Index'  for i in df1[df1.GeoName == state].difference],
                                 hovertemplate =
                                 '&nbsp;<br>&nbsp;&nbsp;<b>%{x}</b><br><br>'+
                                 f'&nbsp;&nbsp;<b>{state}'+' - %{y}</b><br>' +
                                 '&nbsp;&nbsp;%{text}&nbsp;<extra></extra><br>&nbsp;',
                                ),

                      row=2, col=1)

        fig.add_trace(go.Scatter(x=df2[df2.GeoName == state].years,
                                 y=df2[df2.GeoName == state]['value_x'],
                                 name=state,
                                 marker_color=color_use,
                                 line_width=line_width_number,
                                 showlegend=False,
                                 text = [f'&#9660; {abs(i):.1f}% below Country Index' if i < 0 else f'&#9650; {abs(i):.1f}% above Country Index'  for i in df2[df2.GeoName == state].difference],
                                 hovertemplate =
                                 '&nbsp;<br>&nbsp;&nbsp;<b>%{x}</b><br><br>'+
                                 f'&nbsp;&nbsp;<b>{state}'+' - %{y}</b><br>' +
                                 '&nbsp;&nbsp;%{text}&nbsp;<extra></extra><br>&nbsp;',
                                 mode='lines'),
                      row=1, col=1)

        fig.add_trace(go.Scatter(x=df3[df3.GeoName == state].years,
                                 y=df3[df3.GeoName == state]['value_x'],
                                 marker_color=color_use,
                                 line_width=line_width_number,
                                 showlegend=False,
                                 mode='lines',
                                 text = [f'&#9660; {abs(i):.1f}% below Country Index' if i < 0 else f'&#9650; {abs(i):.1f}% above Country Index'  for i in df3[df3.GeoName == state].difference],
                                 hovertemplate =
                                 '&nbsp;<br>&nbsp;&nbsp;<b>%{x}</b><br><br>'+
                                 f'&nbsp;&nbsp;<b>{state}'+' - %{y}</b><br>' +
                                 '&nbsp;&nbsp;%{text}&nbsp;<extra></extra><br>&nbsp;',),
                      row=1, col=2)

        fig.add_trace(go.Scatter(x=df4[df4.GeoName == state].years,
                                 y=df4[df4.GeoName == state]['value_x'],
                                 marker_color=color_use,
                                 line_width=line_width_number,
                                 showlegend=False,
                                 mode='lines',
                                 text = [f'&#9660; {abs(i):.1f}% below Country Index' if i < 0 else f'&#9650; {abs(i):.1f}% above Country Index'  for i in df4[df4.GeoName == state].difference],
                                 hovertemplate =
                                 '&nbsp;<br>&nbsp;&nbsp;<b>%{x}</b><br><br>'+
                                 f'&nbsp;&nbsp;<b>{state}'+' - %{y}</b><br>' +
                                 '&nbsp;&nbsp;%{text}&nbsp;<extra></extra><br>&nbsp;',),
                      row=2, col=2)


    fig.update_layout(height=600,
                      width=850,
                      title_text="",
                      hoverlabel=dict(font_size=12, font_family="Rockwell"),
                      plot_bgcolor='white',
                      margin=dict( autoexpand=False, l=50, r=20, t=50, b=50, ),
                     )
    # Update yaxis properties
    fig.update_yaxes(title_text="",visible = False,fixedrange=True, row=1, col=1)
    fig.update_yaxes(visible = False,fixedrange=True, row=1, col=2)#range=[90, 115]
    fig.update_yaxes(showgrid=False,fixedrange=True, visible = False, row=2, col=1)
    fig.update_yaxes(title_text = "",fixedrange=True, visible = False, row=2, col=2)

    fig.update_xaxes(title_text="",visible = False,fixedrange=True, row=1, col=1)
    fig.update_xaxes(visible = False,fixedrange=True, row=1, col=2)#range=[90, 115]
    fig.update_xaxes(showgrid=False,fixedrange=True, visible = False, row=2, col=1)
    fig.update_xaxes(title_text = "",fixedrange=True, visible = False, row=2, col=2)

    return fig
