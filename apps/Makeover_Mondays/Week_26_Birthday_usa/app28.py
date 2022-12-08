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
DATA_PATH = PATH.joinpath('../Week_26_Birthday_usa/').resolve()

df1 = pd.read_csv(DATA_PATH.joinpath("US_births_1994-2003_CDC_NCHS.csv"))
df2 = pd.read_csv(DATA_PATH.joinpath("US_births_2000-2014_SSA.csv"))
df = pd.concat([df1, df2])

df['birth_date'] = pd.to_datetime(df.year*10000+df.month*100+df.date_of_month,format='%Y%m%d')

ff = df.groupby(['month', 'date_of_month']).agg({'births': 'mean'}).reset_index()
ff['rank'] = ff.births.rank(method = 'first', ascending = 0).astype(int)

df['concieve_date'] =  df.birth_date - datetime.timedelta(266)
df['concieve_date'] = df.concieve_date.apply(lambda x: x.strftime("%d/%b"))

ffd = df.iloc[:, [1, 2, 4]]
heat_map_data = ffd.pivot_table(index='month', columns='date_of_month', values = 'births')
z = heat_map_data.to_numpy()

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

fig = make_subplots(
    rows=3, cols=2, vertical_spacing=0.05,
    specs=[[None, {"rowspan": 1}],
           [{"rowspan": 1, "colspan": 2}, None],
           [{"rowspan": 1, "colspan": 2}, None]],column_widths=[0.7, 0.3], row_heights=[0.1, 0.8, 0.1],
    print_grid=False)

x = [i for i in range(1, 32)]
y = [i for i in range(1, 13)]
month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

hovertext = list()
for yi, yy in enumerate(y):
    hovertext.append(list())
    for xi, xx in enumerate(x):
        try:
            hovertext[-1].append('This date,<br><b>{}/{}</b>, had<br><b>{:,}</b><br />birth on<br>average. It<br>rank<br><b>{}</b>. The<br>conception<br>date* is<br><b>{}</b>.'.format(
                xx, month_name[yy-1], int(z[yi][xi]), ordinal(ff[(ff.month == yy) & (ff.date_of_month == xx)]['rank'].unique()[0]), df[(df.month == yy) & (df.date_of_month == xx)]['concieve_date'].unique()[0]))
        except:
            hovertext[-1].append('')


fig.add_trace(go.Heatmap(
    z=z,
    showscale=False,
    xgap=1,
    ygap=1,
    colorscale=[[0.0, '#FFF7F3'],
                [0.2, '#FFF7F3'],
                [0.511111111111111, "#FDE0DD"],
                [0.610922222222222222, "#FCC5C0"],
                [0.71333333333333333, "#FA9FB5"],
                [0.8144444444444444, "#F768A1"],
                [0.8555555555555556, "#DD3497"],
                [0.9166666666666666, "#AE017E"],
                [0.95888888888888888, "#7A0177"],
                [1.0, "#49006A"]],
    text=hovertext,
    hovertemplate='%{text}<extra></extra>'
), row=2, col=1)

annotation = []
shape = []
x_inital = 0.5
for i, j in zip(['<9K', "", "", "", "11K", "", "", "", ">12K"], ['#FFF7F3', '#FDE0DD', '#FCC5C0', '#FA9FB5', '#F768A1', '#DD3497', '#AE017E', '#7A0177', '#49006A']):

    shape.append(dict(type="rect",
                      x0=x_inital, y0=1.5, x1=x_inital+1, y1=3, xref='x1', yref='y1',
                      line=dict(
                          color='#FFF7F3',
                          width=0,
                      ),
                      fillcolor=j,
                      opacity=1
                      ))

    annotation.append(dict(x=x_inital+0.5, y=0.5, xref='x1', yref='y1',
                           text=f'{i}',
                           showarrow=False,
                           font=dict(
                               family="Courier New, monospace",
                               size=10,
                               color="#999999"
                           ),
                           ))
    x_inital += 1.03

annotation.append(dict(
    x=20, y=1, xref='x3', yref='y3',
                           text='<i>Notes: The conception date, purely for illustration, is 266 days prior to birth. It represent a hypothetical  "moment of conception"<br>' \
                                '       based on the normal gestation period for humans,280 days, minus the average time for ovulation, two weeks.<br>' \
                                'Data: U.S. National Center for Health Statistics(1994-2003); U.S. Social Security Administration(2004-2014)' \
                                '',
                           showarrow=False,
                           font=dict(
                               family="Courier New, monospace",
                               size=11,
                               color="#A5A5A5"
                           ),
    align='left',
    ax=20,
        ay=-30,
))
fig['layout'].update(
    annotations=annotation, shapes=shape)

fig.update_xaxes(side='top',
                 tickvals=[i for i in range(31)],
                 ticktext=[i for i in range(1, 32)],
                 showgrid=False, row=2, col=1)
fig.update_xaxes(fixedrange=True, showgrid=False, showline=False,
                 zeroline=False, showdividers=False, showticklabels=False, row=1, col=2)
fig.update_xaxes(fixedrange=True, showgrid=False, showline=False,range = [0,50],
                 zeroline=False, showdividers=False, showticklabels=False, row=3, col=1)
fig.update_yaxes(
    autorange="reversed",
    tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    ticktext=['Jan. ', 'Feb. ', 'March ', 'April ', 'May ', 'June ',
              'July ', 'Aug. ', 'Sep. ', 'Oct. ', 'Nov. ', 'Dec. '],
    showgrid=False,
    zeroline=False, row=2, col=1)
fig.update_yaxes(fixedrange=True, showgrid=False, showline=False,
                 zeroline=False, showdividers=False, showticklabels=False, row=1, col=2)
fig.update_yaxes(fixedrange=True, showgrid=False, showline=False,
                 zeroline=False, showdividers=False, showticklabels=False, row=3, col=1)
fig.update_layout(
     hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Rockwell",
        
    ),
    font=dict(color='#999999'),
    clickmode='event+select',
    title='<b><Span style="color:#787878;font-size:22px;">HOW POPULAR IS YOUR BIRTHDAY?</span></b>' +
    '<i><Span style="color:#A5A5A5;font-size:13px;"><br>Two decades of American Birthdays, averaged by month and day</span>',
    plot_bgcolor="#fff",
    height=700, width = 1100,
    margin=dict(t=100, l=10, r=10, b=10, pad=0),)


heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

mmw26_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 23', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' How common is your birthday?',href = 'http://thedailyviz.com/2016/09/17/how-common-is-your-birthday-dailyviz/',
                          style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    html.Div([
        html.Div([
            dcc.Graph(figure=fig,
                      config={'displayModeBar': False})
        ], style={'width': "100%"})
    ], style={'background': 'white', 'width': '1200px', 'min-height': '80vh',
              "border-radius": "50px"}, className='p-5 d-flex flex-columns align-items-center '),
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
    ], style={'background': '', 'width': '1200px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4')
], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})