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
from app import app
from datetime import datetime


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_15_Website_Analytics/').resolve()

custom_date_parser = lambda x: datetime.strptime(x, "%M:%S")
df1 = pd.read_csv(DATA_PATH.joinpath('total session.csv'))
df2 = pd.read_csv(DATA_PATH.joinpath('avg_session_dur.csv'), parse_dates=['duration_in_minute'], date_parser=custom_date_parser)
df3 = pd.read_csv(DATA_PATH.joinpath('bounce_rate.csv'))
df4 = pd.read_csv(DATA_PATH.joinpath('avg_time_df.csv'), parse_dates=['duration_in_minute'], date_parser=custom_date_parser)

week_15_wiz = dbc.Container([
    dbc.Row([
        html.P('hi', id = 'text', hidden = True),
        html.H1('#WorkoutWednesday - Week 15 - Website Analytic'),

        html.Hr(style={'height':"5px",'width':"100%", 'background': '#f7cc63'}, className = 'p-0.5'),
    ], className = 'm-0 p-4'),
    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P(id='total-session-webanalytic', className = 'mb-0 pb-0', style = {'color':'#7830b6', 'font-size':'50px'}),
                    html.P('Total Session', className = "font-weight-bold text-capitalize mt-0 pt-0", style = {'font-size': '25px'})
                ], className = 'd-flex flex-column align-items-center justify-content-center')
            ], className = 'align-center', style = {'background': 'white', 'height' : '250px', 'border-style': 'none none none solid', 'border-left': '5px solid #7830b6'})
        ], width = 3),
        dbc.Col([
            dcc.Loading(
            id="loading-1-website_analytic",
            type="default",
            children=dcc.Graph(id='total-session-chart-webanalytic',config={'displayModeBar': False},
                      figure={}, ),)
        ], width = 9)
    ], className = 'm-4'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P(id='avg-session-webanalytic', className = 'mb-0 pb-0', style = {'color':'#58b8ba', 'font-size':'50px'}),
                    html.P('Avg Session Duration', className = "text-center font-weight-bold text-capitalize mt-0 pt-0", style = {'font-size': '25px'})
                ], className = 'd-flex flex-column align-items-center justify-content-center')
            ],className = 'align-center', style = {'background': 'white', 'height' : '250px', 'border-style': 'none none none solid', 'border-left': '5px solid #58b8ba'})
        ], width = 3),
        dbc.Col([
            dcc.Loading(
            id="loading-2-website_analytic",
            type="default",
            children=dcc.Graph(id='avg-session-chart-webanalytic',config={'displayModeBar': False},
                      figure={}, ),)
        ], width = 9)
    ], className = 'm-4'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P(id='bounce-rate-webanalytic', className = 'mb-0 pb-0', style = {'color':'#72b966', 'font-size':'50px'}),
                    html.P('Avg Bounce Rate', className = "text-center font-weight-bold text-capitalize mt-0 pt-0", style = {'font-size': '25px'})
                ], className = 'd-flex flex-column align-items-center justify-content-center')
            ],className = 'align-center', style = {'background': 'white', 'height' : '250px', 'border-style': 'none none none solid', 'border-left': '5px solid #72b966'})
        ], width = 3),
        dbc.Col([
            dcc.Loading(
            id="loading-3-website_analytic",
            type="default",
            children=dcc.Graph(id='bounce-rate-chart-webanalytic',config={'displayModeBar': False},
                      figure={}, ),)
        ], width = 9)
    ], className = 'm-4'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P(id='Avg-time-webanalytic', className = 'mb-0 pb-0', style = {'color':'#628cb9', 'font-size':'50px'}),
                    html.P('Avg Time on Page', className = "text-center font-weight-bold text-capitalize mt-0 pt-0", style = {'font-size': '25px'})
                ], className = 'd-flex flex-column align-items-center justify-content-center')
            ],className = 'align-center', style = {'background': 'white', 'height' : '250px', 'border-style': 'none none none solid', 'border-left': '5px solid #628cb9'})
        ], sm=11, md= 3 ),
        dbc.Col([
            dcc.Loading(
            id="loading-4-website_analytic",
            type="default",
            children=dcc.Graph(id='avg-time-chart-webanalytic',config={'displayModeBar': False},
                      figure={}, ),)
        ], sm=11, md= 9 )
    ], className = 'm-4'),
    dbc.Row([
                html.Div([
                    html.P(['Data | Superstore']),
                    html.A(html.P('Challenge_by:@Ann Jackson'), href = "https://public.tableau.com/profile/ann.jackson#!/",target ="_blank"),
                    html.A(html.P('Get Data'), href='https://data.world/annjackson/wow-google-analytics', target = "_blank")
                ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                html.Div([
                    html.P("Developed By: "),
                    html.Div([
                        html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                        href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                    ])
                ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
        ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})

],fluid=True, className = 'm-0', style = {'background': 'white'})


@app.callback(
    [Output('total-session-chart-webanalytic','figure'), Output('total-session-webanalytic', 'children')],
    Input('text', 'children')
)
def generate_week15analytic1(text):
    avgoftotalsession = int(df1.Sessions.mean())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1.Date, y=df1.Sessions, name='Total Session',
                             line=dict(color='#7830b6', width=2, dash='solid'),
                             hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Sessions: %{text}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',
                             text = ["{:,}".format(i) for i in df1.Sessions],
                            ))
    fig.add_trace(go.Scatter(x=[df1.Date.iloc[-1]], y = [df1.Sessions.iloc[-1]],
                      textposition='top center', textfont=dict(color='#7830b6'), mode='markers+text',
                      marker=dict(color='#7830b6', size=8),
                      hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Sessions: %{text}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',
                            text=["{:,}".format(df1.Sessions.iloc[-1])],)
                 )
    fig.add_hline(y=avgoftotalsession, line_dash="dot",
                  annotation_text="AVG: " + "{:,}".format(avgoftotalsession), annotation_font_size=12,
                  annotation_position="top left")

    fig.update_layout(title_text="",
                      height = 250,
                      # width = 250,
                      plot_bgcolor = 'white',
                      margin=dict(t=0, l=62, r=0, b=0),
                      showlegend = False,
                      xaxis=dict(title='',
                             range=['2019-11-15','2021-4-20'],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             mirror=False,
                             fixedrange=True,
                             tickformat="%b %d,%y"),
                      yaxis=dict(title='',
                             range=[0, 4500],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             fixedrange=True,
                             mirror=False),
                       hoverlabel=dict(bgcolor="white",
                                       font_size=12,
                                       font_family="Rockwell")
                     )
    return fig, "{:,}".format(df1.Sessions.sum())

@app.callback(
    [Output('avg-session-chart-webanalytic','figure'), Output('avg-session-webanalytic', 'children')],
    Input('text', 'children')
)
def generate_week15analytic2(text):

    # df2 = pd.read_csv('data/avg_session_dur.csv', parse_dates=['duration_in_minute'], date_parser=custom_date_parser)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2.Date.iloc[:-1], y=df2.duration_in_minute.iloc[:-1], name='Total Session',
                             line=dict(color='#58b8ba', width=2, dash='solid'),
                             hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Average Sessions Duration: %{y}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',

                            ))
    fig.add_trace(go.Scatter(x=[df2.Date.iloc[-2]], y=[df2.duration_in_minute.iloc[-2]],
                      textposition='top center', textfont=dict(color='#58b8ba'), mode='markers+text',
                      marker=dict(color='#58b8ba', size=8),
                      hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Average Sessions Duration: %{text}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',
                            text=[df2.duration_in_minute.iloc[-2].strftime("%M:%S")],
    #                         texttemplate='%M%S'
                             )
                 )
    fig.add_trace(go.Scatter(x=['2019-11-15', df2.Date.iloc[-1]], y=[df2.duration_in_minute.mean(), df2.duration_in_minute.mean()],
                      textposition='top right', textfont=dict(color='gray'), mode='lines+text',
                      text=["AVG: " +str(df2.duration_in_minute.mean().strftime("%M:%S")), ""],line=dict(color='gray', width=2,dash='dot')
    #                         texttemplate='%M%S'
                             )
                 )

    fig.update_layout(title_text="",
                      height = 250,
                      plot_bgcolor = 'white',
                      margin=dict(t=0, l=0, r=0, b=0),
                      showlegend = False,
                      xaxis=dict(title='',
                             range=['2019-11-15','2021-4-20'],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             mirror=False,
                             fixedrange=True,
                             tickformat="%b %d,%y"),
                      yaxis=dict(title='',
                             range=['1900-01-01 00:01:22', '1900-01-01 00:04:22'],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             mirror=False,
                             fixedrange=True,
                             dtick=60000,
                             tickformat="%M:%S"
                             ),
                       hoverlabel=dict(bgcolor="white",
                                       font_size=12,
                                       font_family="Rockwell")
                     )
    return fig, str(df2.duration_in_minute.mean().strftime("%M:%S"))


@app.callback(
    [Output('bounce-rate-chart-webanalytic','figure'), Output('bounce-rate-webanalytic', 'children')],
    Input('text', 'children')
)
def generate_week15analytic3(text):
    # df3 = pd.read_csv('data/bounce_rate.csv')
    # df3.head()

    avgofbouncerate = int(df3.bounce_rate.mean())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df3.Date, y=df3.bounce_rate, name='Total Session',
                             line=dict(color='#72b966', width=2, dash='solid'),
                             hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Bounce Rate: %{text}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',
                             text = [str(i) + '%' for i in df3.bounce_rate],
                            ))
    fig.add_trace(go.Scatter(x=[df3.Date.iloc[-1]], y = [df3.bounce_rate.iloc[-1]],
                      textposition='top center', textfont=dict(color='#72b966'), mode='markers+text',
                      marker=dict(color='#72b966', size=8),
                      hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Bounce Rate: %{text}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',
                            text=[str(df3.bounce_rate.iloc[-1])+"%"])
                 )
    fig.add_hline(y=avgofbouncerate, line_dash="dot",
                  annotation_text="AVG: " + str(avgofbouncerate)+"%", annotation_font_size=12,
                  annotation_position="top left")

    fig.update_layout(title_text="",
                      height = 250,
                      plot_bgcolor = 'white',
                      margin=dict(t=0, l=65, r=0, b=0),
                      showlegend = False,
                      xaxis=dict(title='',
                             range=['2019-11-15','2021-4-20'],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             mirror=False,
                             fixedrange=True,
                             tickformat="%b %d,%y"),
                      yaxis=dict(title='',
                             range=[0, 60],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             fixedrange=True,
                             mirror=False),
                       hoverlabel=dict(bgcolor="white",
                                       font_size=12,
                                       font_family="Rockwell")
                     )
    return fig, str(avgofbouncerate)+"%"


@app.callback(
    [Output('avg-time-chart-webanalytic','figure'), Output('Avg-time-webanalytic', 'children')],
    Input('text', 'children')
)
def generate_week15analytic4(text):
    # custom_date_parser = lambda x: datetime.strptime(x, "%M:%S")
    # df4 = pd.read_csv('data/avg_time_df.csv', parse_dates=['duration_in_minute'], date_parser=custom_date_parser)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df4.Date.iloc[:-1], y=df4.duration_in_minute.iloc[:-1], name='Total Session',
                             line=dict(color='#628cb9', width=2, dash='solid'),
                             hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Average Time on Page: %{y}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',

                            ))
    fig.add_trace(go.Scatter(x=[df4.Date.iloc[-2]], y=[df4.duration_in_minute.iloc[-2]],
                      textposition='top center', textfont=dict(color='#628cb9'), mode='markers+text',
                      marker=dict(color='#628cb9', size=8),
                      hovertemplate =
                                            '&nbsp;<br>&nbsp;&nbsp;&nbsp;Week of <b>%{x}</b>&nbsp;&nbsp;&nbsp;<br>'+
                                            '&nbsp;&nbsp;&nbsp;Average Time on Page: %{text}&nbsp;&nbsp;&nbsp;<extra></extra><br>&nbsp;',
                            text=[df4.duration_in_minute.iloc[-2].strftime("%M:%S")],
    #                         texttemplate='%M%S'
                             )
                 )
    fig.add_trace(go.Scatter(x=['2019-11-15', df4.Date.iloc[-1]], y=[df4.duration_in_minute.mean(), df4.duration_in_minute.mean()],
                      textposition='top right', textfont=dict(color='gray'), mode='lines+text',
                      text=["AVG: " +str(df4.duration_in_minute.mean().strftime("%M:%S")), ""],line=dict(color='gray', width=2,dash='dot')
    #                         texttemplate='%M%S'
                             )
                 )

    fig.update_layout(title_text="",
                      height = 250,
                      plot_bgcolor = 'white',
                      margin=dict(t=0, l=0, r=0, b=0),
                      showlegend = False,
                      xaxis=dict(title='',
                             range=['2019-11-15','2021-4-20'],
                             linecolor='#d9d9d9',
                             showline=True,
                             fixedrange=True,
                             showgrid=False,
                             mirror=False,
                             tickformat="%b %d,%y"),
                      yaxis=dict(title='',
                             range=['1900-01-01 00:01:00', '1900-01-01 00:02:22'],
                             linecolor='#d9d9d9',
                             showline=True,
                             showgrid=False,
                             mirror=False,
                             fixedrange=True,
                             dtick=60000,
                             tickformat="%M:%S"
                             ),
                       hoverlabel=dict(bgcolor="white",
                                       font_size=12,
                                       font_family="Rockwell")
                     )
    return fig, str(df4.duration_in_minute.mean().strftime("%M:%S"))
