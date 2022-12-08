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
from datetime import datetime
from plotly.subplots import make_subplots
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_25_Stop_and_Search_UK/').resolve()

df = pd.read_csv(DATA_PATH.joinpath("stop-and-search-data.csv"))
df.dropna(inplace=True)
df['Stops_per_1000'] = df['Number of stop and searches']/df['Population']*1000
df['Stops_per_1000'] = df['Stops_per_1000'].round(0).astype('int')

heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']
text_color = ['#667175']
background_color = ["#EEF2F7"]

ethinicity = {'All':'All', 'Bangladeshi':'Bangladeshi', 'Indian':'Indian', 'Pakistani':'Pakistani',
 'Asian Other':'Any other Asian background', 'Black African':'Black African', 'Black Caribbean':'Black Caribbean',
 'Black Other':'Any other black background', 'Mixed White/Asian':'Mixed White and Asian',
 'Mixed W/B African':'Mixed White and Black African', 'Mixed W/B Caribbean':'Mixed White and Black Caribbean',
 'Mixed Other':'Any other mixed/multiple ethnic background', 'White British':'White British', 'White Irish':'White Irish',
 'White Other':'Any other white background', 'Chinese':'Chinese', 'Any Other':'Any other ethnic group'
            }


ethnicity_list = ['All','Asian', 'Black', 'Mixed', 'White','Other inc Chinese',]
filtered_df = df[df.Ethnicity.isin(ethnicity_list)]
avg_stops = filtered_df.groupby('Ethnicity').agg({'Stops_per_1000':'mean'}).round(0).reset_index()
fig = go.Figure()
colors = ["#5497BE", "#FDA14C", "#B89B89", "#878C92", "#8CBBD7", "#D88343" ]
for j,i in enumerate(ethnicity_list):
    x = filtered_df[filtered_df.Ethnicity == i].iloc[:,[1, 0]].T.to_numpy()
    y = filtered_df[filtered_df.Ethnicity == i].Stops_per_1000.tolist()
    fig.add_trace(go.Bar(
              x = x,
              y = y,
              name = i,
              width=0.2,
        hovertemplate = '&nbsp;%{x}<br>'+
                            '&nbsp;%{y}</b>&nbsp;<extra></extra>',
              marker=dict(color = colors[j])

    ))
    fig.add_trace(go.Scatter(
            x=x,
            y=filtered_df[filtered_df.Ethnicity == i].Stops_per_1000,
            mode='markers',
            hovertemplate = '&nbsp;%{x}<br>'+
                            '&nbsp;%{y}</b>&nbsp;<extra></extra>',
            marker=dict(color = colors[j], size=7),
            
        ))
    fig.add_trace(go.Scatter(
            x=[[i, i], [x[1][1], x[1][-2]]],
            y=[y[0]+5, y[-1]+5],
            text=[f'{x[1][0]} <br> {y[0]}', f'{x[1][-1]} <br> {y[-1]}'],

            mode="text",
            hovertemplate = '&nbsp;%{x}<br>'+
                                '&nbsp;%{y}</b>&nbsp;<extra></extra>',
            textfont=dict(
                family="Courier New",
                size=10,
                color=colors[j]
                ),
            
    ))

fig.update_layout(bargap=0.1, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1, # gap between bars of the same location coordinate.
    plot_bgcolor = '#FEFAF1',
    paper_bgcolor = '#FEFAF1',
    height = 600,
    width = 950,
    showlegend = False,
    margin=dict(t=10, l=0, r=0, b=0, pad = 0),
    yaxis = dict(autorange="reversed",fixedrange=True,showgrid=False, showticklabels=False, showline=False,
                              zeroline = False),
    xaxis = dict(fixedrange = True,showgrid = False, showline=False,zeroline = False, showdividers = False,showticklabels=False,),
    
                 )
x_inital = -0.5

for i, j in enumerate(ethnicity_list):

    fig.add_shape(type="rect",
                    x0=x_inital, y0=-2, x1=x_inital+11, y1=-20,xref='x', yref='y',
                    line=dict(
                        color='black',
                        width=1,
                    ),
                    fillcolor=colors[i],
                    opacity = 1
                )
    fig.add_annotation(x=x_inital+5.5, y=-15, xref='x', yref='y',
            text=f'{j}',
            showarrow=False,
            font=dict(
            family="Courier New, monospace",
            size=14,
            color="#ffffff"
            ),
            )
    fig.add_annotation(x=x_inital+5.5, y=-7, xref='x', yref='y',
            text=f' {int(avg_stops[avg_stops.Ethnicity == j]["Stops_per_1000"])} ',
            showarrow=False,
            font=dict(
            family="Raleway, monospace",
            size=18,
            color="#ffffff"
            ),
            )
    
    x_inital += 11

fig.add_annotation(x=0.5, y=-25, xref='paper', yref='y',
            text=f'Average number of Stops and Searches over the year 2009/10 to 2019/20',
            showarrow=False,
            font=dict(
            family="Courier New, monospace",
            size=12,
            color="black"
            ),
            )

fig.add_annotation(x=0.5, y=-40, xref='paper', yref='y',
            text=f'DataSource : gov.uk  || Viz created by :- Abhinav @abhinavk910',
            showarrow=False,
            font=dict(
            family="Courier New, monospace",
            size=11,
            color="black"
            ),
            )

fig.add_annotation(x=0.5, y=-50, xref='paper', yref='y',
            text=f'Stop and Search Rates by Ethnicity in the UK',
            showarrow=False,
            font=dict(
            family="Raleway, monospace",
            size=25,
            color="crimson"
            ),
            )

fig.add_annotation(x=[['Black'], ['2009/10']], y=120, xref='x', yref='y',
            text='<Span style="color:#DF343C;font-size:15px;">Stop and Search</span>'+
               '<Span style="color:#B89B89;font-size:10px;"><br>Ethnicity - </span>'+
               '<Span style="color:black;font-size:12px;">Black</span>'+
               '<br><Span style="color:#B89B89;font-size:10px;">Rate per 1000 population :- </span>'+
                '<Span style="color:black;font-size:12px;">120</span>',
            showarrow=True,ax = 150, ay = -50,
            font=dict(
            family="Raleway, monospace",
            size=25,
            color="crimson"
            ),
                align="left",arrowhead=0, arrowsize=1, arrowwidth=2, arrowcolor="#B89B89",
        bordercolor="#FEFAF1",borderwidth=2,borderpad=4,opacity=0.8
            )


tab1_content =   html.Div([
        html.P([html.Span('Stop and search rate per 1,000 people |', style={'font-size': '2.5vw','color':text_heading_color[0], 'background':''}),
                   html.Span(' by ethnicity over time',style={'font-size': '1.2vw', 'color':text_heading_color[0]})] , className='m-0 p-0'),
        html.Hr(style = {'background': text_heading_color[0], 'width': "100%"}, className='mt-1 mb-5 p-0'),
        html.Div([
            html.Div([
                html.H1('Select Ethnicity', style= {'color':text_heading_color[0], 'font-size':"30px"}),
                dcc.Dropdown(
                    id = 'mmw25_2',
                    options=[
                        {'label': i, 'value': ethinicity[i]} for i in ethinicity.keys()],
                    value=['All','Indian', 'Pakistani', 'Chinese'],
                    multi=True,
                    clearable=False,
                    style={'color':text_color[0],'background-color':'#192930', 'width' : "520px" ,
                           'border-color': '#192930'}
                )  
            ], className='mb-3 p-3', style = {'border-style':'solid','border-width': '2px','border-color': text_heading_color[0]}),
            html.Div([
                html.Div([
                    dcc.Graph(id='mmw25_1',
                              config={'displayModeBar': False})
                ], style={'width': "55%"}),
                html.Div([
                    dcc.Markdown('''
                            #### The data shows that, in the 2 years to March 2020:
                            * the national stop and search rate went up for the first time since 2009 to 2010, from 5 to 11 stop
                            and searches per 1,000 people
                            * rates went up in every ethnic group except the Chinese group, where they stayed broadly the same

                            #### Between April 2009 and March 2020:
                            * the national rate went down from 25 to 11 per 1,000 people
                            * the rate for White people was lower than the national rate in every year
                            * the rates for the Asian, Black, and Mixed ethnic groups were higher than the national rate in
                            every year
                            * the Chinese and Mixed White and Asian ethnic groups had the lowest rates out of all 16 ethnic groups 
                            in most years
                            * the Black Caribbean and Black Other groups consistently had the highest rates
                    ''',
                    style={'color': "#B5B9BB",'font-size':"" },id='mmw25_markdown')

                ], style={'width': "40%"}, className='m-1'),], className='d-flex flex-row justify-content-between mt-5')
        ], className = 'd-flex flex-column justify-content-between align-items-center'),
    ], style={'background':'#192930','width': '1300px', 'min-height': '600px',
              "border-radius": "50px","box-shadow": "15px 0px 15px -10px rgba(0,0,0,0.75)"}, className='p-5'),
  
tab2_content =  html.Div([
                    dcc.Graph(id='mmw25_200', figure=fig,
                              config={'displayModeBar': False})
                ], style={'width': ""}),


mmw25_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav for',
                html.Span(' Makeover Monday Week 25', style = {'color':heading_color[0]})],
                style={'color':"#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' Stop and search rate in UK',href = 'https://www.ethnicity-facts-figures.service.gov.uk/crime-justice-and-the-law/policing/stop-and-search/latest#by-ethnicity-over-time',
                       target = "_blank",style = {'color':heading_color[0]}),
                
            ],style={'color':"#BBBBBA"},className='m-0')], className='')],style={'background':'', 'width':'1200px', 'min-height':'100px'}, className = 'pt-4 pl-4'),
    dbc.Tabs(
    [
        dbc.Tab(tab2_content, label="Major Classification",tab_style={"marginLeft": "auto",}),
        dbc.Tab(tab1_content, label="Minor Classification" ,),
        
    ]),
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
], className='d-flex flex-column  align-items-center ', style={'background': background_color[0]})



@app.callback(
    [Output('mmw25_1', 'figure')],
    [Input('mmw25_2', 'value'),])
def update_output(ethnicity):
    
    if len(ethnicity) == 0:
        ethnicity = ['All']
    
    fig2 = go.Figure()
    for i in ethnicity:
        fig2.add_trace(go.Scatter(x=df[df.Ethnicity == i].Time, y=df[df.Ethnicity == i]['Stops_per_1000'],
                            name=i,
                            text=i,
                            hoverinfo='y+x',
                            line_shape='spline'))
    
    fig2.update_layout(
            plot_bgcolor = '#192930',
            paper_bgcolor = '#192930',
            hoverlabel=dict(
                font_size=15,
                font_family="Rockwell",
                align = 'auto',
            ),
            xaxis = dict(
                showline=True,
                linecolor='#667175',
                color = "#667175",
                showgrid=False,
                zeroline =False,
                ticks='outside',
                tickwidth=1.5,
            ),
            margin=dict(t=0, l=0, r=0, b=0, pad = 0),
            yaxis = dict(
                showline=True, 
                linecolor='#667175',
                showgrid=False,
                zeroline =False,
                color = "#667175",
                ticks='outside',
                tickwidth=1.5,
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.91,
                title_font_family="Courier",
                title_text='Ethnicity',
                title_font_color = text_heading_color[0],
                font=dict(
                    family="Courier",
                    size=12,
                    color=text_heading_color[0]
                ),
                bgcolor="#192930",
            ))

    return [fig2]