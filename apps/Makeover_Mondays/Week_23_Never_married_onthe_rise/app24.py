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
DATA_PATH = PATH.joinpath('../Week_23_Never_married_onthe_rise/').resolve()

df = pd.read_excel(DATA_PATH.joinpath("Never Married.xlsx"))
df['Never Married'] = df['Never Married']*100
df1 = df.query('Year == 2016')
df2 = df.groupby(['Gender','Age Range', 'Year']).sum().unstack().reset_index()
df2['difference'] = df2.apply(lambda x: x[3]-x[2], axis = 1)
df2.columns = ['Gender', 'Age Range', 'Never Married 2016','Never Married 2006', 'Difference']
df3 = pd.merge(df1, df2, left_on=['Gender', 'Age Range'], right_on=['Gender', 'Age Range']).iloc[:,[0,1,2,3,4,-1]]
df3.columns = ['Gender', 'Age Range', 'Year', 'Never Married 2016','Never Married 2006', 'Difference']
df4 = df3.groupby(['Age Range', 'Gender']).agg({'Difference':'sum', 'Never Married 2016':'sum','Never Married 2006':'sum'}).unstack()
df4.reset_index(drop = False, inplace=True )

fig = make_subplots(rows=5, cols=1, shared_xaxes=True, print_grid=False, vertical_spacing=(0.15 / df4.shape[0]))

for k, row in df4.iterrows():
    fig.append_trace(go.Bar(
        orientation='h',
        x=[row[('Difference', 'Men')], row[('Difference', 'Women')]],
        y=[ 'Men','Women',],
        text=[ "{:,.0f}%".format(row[('Difference', 'Men')]), "{:,.0f}%".format(row[('Difference', 'Women')]),],
        hoverinfo='text',
        customdata = row.unstack().iloc[:-1, [0,1]].T,
        hovertemplate =
                        '&nbsp;<br>&nbsp;&nbsp;<b>%{y}</b>'+
                        '<br>&nbsp;&nbsp;Never Married 2016 :-  %{customdata[1]:.1f}%&nbsp;&nbsp;'+
                        '<br>&nbsp;&nbsp;Never Married 2006 :-  %{customdata[2]:.1f}%&nbsp;&nbsp;'+
                        '<br>&nbsp;&nbsp;% Change vs 2016 :- %{customdata[0]:.1f}%&nbsp;&nbsp;<br>&nbsp;<extra></extra>',
        textposition='auto',
        marker=dict(opacity = 0.9,color=['#2FB5A7', '#FDE725'],line_color = '#C1C5C7',line_width = 2),
    ), row=k+1, col=1)
    fig.update_yaxes(title_text=row[('Age Range','')], showticklabels =  False,zeroline = False,color = '#C1C5C7', showgrid=False, row=k+1, col=1)
    fig.update_xaxes(showticklabels =  False,showgrid=False,color = '#C1C5C7',zeroline = True,zerolinecolor = '#C1C5C7', row=k+1, col=1)

fig.update_layout(
                  height = 1000,
                  # width=900,
                  title = dict(
                      text = '<Span style="color:#C1C5C7;font-size:30px;">NEVER </span>'+
                             '<Span style="color:#C1C5C7;font-size:30px;">MARRIED </span>'+
                             '<Span style="color:#C1C5C7;font-size:20px;">ON </span>'+
                             '<Span style="color:#C1C5C7;font-size:20px;">THE </span>'+
                             '<Span style="color:#6EC1E4;font-size:80px;">RISE </span>'+
                             '<Span style="color:#C1C5C7;font-size:15px;"><br>This visualization show us the percentage variation from 2006 to 2016<br> by gender and age range</span>'+
                             '<Span style="color:#FDE725;font-size:30px;"><br><br>Women </span>'+
                             '<Span style="color:#2FB5A7;font-size:30px;">Men </span>',
                      font=dict(family='Rockwell, monospace', color='black', size=25),x = 0.5
                    ),
                  showlegend = False,
                  plot_bgcolor="#1B1B1B",
                  paper_bgcolor = "#1B1B1B",
                  margin=dict(t=300, l=150, r=10, b=80, pad = 10),
                  bargroupgap = 0.2)




heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

mmw23_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 23', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' Percentage of Never Married Adults by Sex and Age',href = 'https://www.census.gov/newsroom/press-releases/2021/marriages-and-divorces.html',
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
    ], style={'background': '', 'width': '1200px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4'),
], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})
