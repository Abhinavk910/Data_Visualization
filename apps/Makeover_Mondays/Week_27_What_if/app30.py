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
DATA_PATH = PATH.joinpath('../Week_27_What_if/').resolve()

df1 = pd.read_csv(DATA_PATH.joinpath("data1.csv"))
df4 = pd.read_csv(DATA_PATH.joinpath("data2.csv"))

heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]



def country_map(df):
    bar_data = df.groupby('Winner').agg({'Electoral Votes Final Available':'sum'}).reset_index()
    bar_data.sort_values('Winner', inplace=True)
    fig1 = make_subplots(rows=2, cols=1, row_heights=[0.2, 0.8],  vertical_spacing=0.02)

    #map
    fig1.append_trace(go.Scatter(
        x=df.Column, y=df.Row,
        text=["<br>  ".join([i, "{:,}".format(int(j))]) for i, j in zip(df.State, df['Electoral Votes Final Available'])],
        marker_symbol=14,
        marker_line_color="white",
        marker_color=df.Winner.replace({'Trump': 'rgba(250,0,0,0.5)', 'Biden':'rgba(0,0,256,0.5)','UnKnown':'#999999'}),
        hovertemplate = '&nbsp; %{text}</b>&nbsp;<extra></extra>',
        marker_colorscale=[[0, 'rgb(211, 234, 231)'], [0.5, 'rgb(57, 121, 173)'], [1, 'rgb(7, 69, 117)']],
        marker_line_width=0.5, marker_size=43, mode='markers'), row=2, col=1)

    for i, row in df.iterrows():
        fig1.add_annotation(
                x=row['Column'], y = row['Row'],
                xref="x2",yref="y2",
                text=f"{row['Abbreviation']}<br>{int(row['Electoral Votes Final Available'])}",
                showarrow=False,
                font=dict(family="Rockwell, monospace",size=12,color="black"),
                ax=20, ay=-30,
                opacity=0.9
                )

    #bar plot
    l = {'Trump': 'rgba(250,0,0,0.5)', 'Biden':'rgba(0,0,256,0.5)','UnKnown':'#999999'}
    for i, row in bar_data.iterrows():
        fig1.append_trace(go.Bar(
                    x=[row['Electoral Votes Final Available']], y=['Result  '],
                    orientation='h',
                    hoverinfo='skip',
                    text=int(row['Electoral Votes Final Available']),
                    textposition='auto',
                    marker=dict(
                        color=l[row['Winner']],
                        line=dict(color=l[row['Winner']], width=1)
                    )
        ), row=1, col=1)

    x_inital = 200
    for i, j in zip(['Biden','Trump',  'Unknown'], ['rgba(0,0,256,0.5)', 'rgba(256,0,0,0.5)',  '#999999']):

        fig1.add_shape(dict(type="rect",
                          x0=x_inital, y0=1.5, x1=x_inital+15, y1=1.9, xref='x1', yref='y1',
                          line=dict(
                              color=j,
                              width=2,
                          ),
                          fillcolor=j,
                          opacity=1
                          ))

        fig1.add_annotation(dict(x=x_inital-25, y=1.75, xref='x1', yref='y1',
                               text=f'{i}',
                               showarrow=False,
                                align = 'left',
                               font=dict(
                                   family="Courier New, monospace",
                                   size=11,
                                   color="#667175",
                               ),
                               ))
        x_inital += 80



    fig1.update_layout(barmode='stack')

    fig1.update_yaxes(autorange="reversed",fixedrange=True,showgrid=False,color = "#667175", showticklabels=False, showline=False,
                                  zeroline = False, row=2, col=1)
    fig1.update_xaxes(fixedrange=True,showgrid=False, showticklabels=False, showline=False,
                                  zeroline = False, row=2, col=1)


    fig1.update_layout(clickmode='event+select',showlegend = False,

                      xaxis = dict(fixedrange = True,showgrid = False,showticklabels=False, showline=False,zeroline = False),
                      hoverlabel=dict(bgcolor="white",font_size=15,  font_family="Rockwell"),
                      margin=dict(t=10, l=30, r=30, b=10, pad = 0),
                     height=450, width=630,
                      plot_bgcolor='#F8ECC2',paper_bgcolor='#F8ECC2', )
    return fig1

demographic_group = ['Income', 'Age', 'Religion', 'Education', 'Voting Time', 'Marital Status', 'Gender', 'Moderate', 'Living','White']
demographic = [['Under $25,000', '$25,000 - $49,999',  '$50,000 - $74,999',  '$75,000 - $99,999','$100,000+'],
                ['18-29', '30-44', '45-64', '65'],
                ['Catholic','Protestant'],
                ['HS or Less','Some College','College Grad','Post Grad'],
                ['Did not vote in 2016','Early Voting','Election Day'],
                ['Single','Married'],
                ['Men','Women'],
                ['Moderate'],
                ['Rural','Small Town','Suburban','Urban'],
                ['White',]]
demographic_dictionary = {}
for i, j in enumerate(demographic):
    for k in j:
        demographic_dictionary[k] = demographic_group[i]

mmw27_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910",target="_blank", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 27', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.A(' Impact of Single Demographic on Presidential Election',
                       href="https://www.reddit.com/r/dataisbeautiful/comments/kji3wx/oc_2020_electoral_map_if_only_voted_breakdown_by/",
                       target="_blank",
                       style={'color': heading_color[0]}),
                ' in 2020'
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    
    html.Div([
        html.Div([
            html.P([html.Span('US Presidential Election 2020 | ', style={'font-size': '30px', 'background':''}),
                           html.Span(' Never Ending What Ifs..',style={'font-size': '50'})] , className='m-0 p-0'),
            html.Div([
                html.P('Select Demographic', className='m-0 p-0',style={'font-size': '10px', 'text-align':'center'}),
                dcc.Dropdown(
                        id='mmw27-1',
                        options=[
                            {'label': i, 'value': i} for i in list(demographic_dictionary.keys())
                        ],
                        value='Men',
                        clearable=False,
                        optionHeight=30,
                        style={'color':'Black','background-color':'#F8ECC2','vertical-align': 'middle', 'display': 'inline-block','font-size':"10px",'width' : "100px" ,
                           'border-color': 'grey', 'height':"25px", 'text-align': '', 'line-height': '20px'},
                        className='m-0 pb-3',
                    ),
                ],className='',style = {'background': '',})
            ],className='d-flex justify-content-between pb-1', style = {'background': '',}),
        html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
        html.Div([
            html.Div([
                html.Span('IF ONLY '
                       ,className="mt-1 mb-0 p-0",style={'color': 'Black','font-size':"50px" }),
                html.Span(id='mmw27-2',
                       className="mt-1 mb-0 p-0",style={'color': 'Black','font-size':"50px" }),
                html.Span(' Vote!'
                       ,className="mt-1 mb-0 p-0",style={'color': 'Black','font-size':"50px" }),
            ], style={'width': '500px'}, className='d-flex flex-column justify-content-center align-items-center'),
            html.Div([
                dcc.Graph(id='mmw27-3',
                          config={'displayModeBar': False})
            ], style={'width': "60%"})
        ], className='d-flex flex-row justify-content-between'),
        html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
        html.Div([
            html.Div([
                dcc.Graph(id='mmw27-4',
                          config={'displayModeBar': False})
            ], style={'width': "100%"}),

        ], className='d-flex flex-row justify-content-between mt-5')
    ], style={'background': '#F8ECC2', 'width': '1200px', 'min-height': '80vh',
              "border-radius": "50px","box-shadow": "15px 0px 15px -10px rgba(0,0,0,0.75)"}, className='p-5'),
    html.Div([
        html.Div([
            html.P([
                'Created by ',html.A('Abhinav', href='http://www.linkedin.com/in/abhinavk910',target="_blank", style={'color': heading_color[0]}),
                html.A(' Kumar', href="https://twitter.com/abhinavk910", target="_blank",style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'Tool: ',
                html.Span('Plotly', style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')], style={'background': '', 'width': '1200px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4'),
], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})


@app.callback(
    Output("mmw27-2", "children"),
    [Input("mmw27-1", "value")]
)
def heading_toggle(inp):
    return inp

@app.callback(
    Output("mmw27-3", "figure"),
    [Input("mmw27-1", "value")]
)
def graph_toggle1(filter_by):
    df = df4.merge(df1[df1.Demographic == filter_by][['State Abbr', 'Winner', 'Biden %', 'Trump %']],
                   how='left', right_on='State Abbr', left_on='Abbreviation',)
    df['Winner'] = df['Winner'].fillna('UnKnown')
    return country_map(df)

@app.callback(
    Output("mmw27-4", "figure"),
    [Input("mmw27-1", "value")]
)
def graph_toggle1(selected):
    demographic_group_value = demographic_dictionary[selected]
    index_value = demographic_group.index(demographic_group_value)
    no_of_row = len(demographic[index_value])
    if no_of_row <2:
        height_req = 350
    elif no_of_row<3:
        height_req = 400
    elif no_of_row<4:
        height_req = 500
    elif no_of_row<5:
        height_req = 700
    elif no_of_row<6:
        height_req = 900
        
    fig = make_subplots(rows=no_of_row, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    group = demographic[index_value]
    final_max_val = 0
    final_min_val = 100
    for kk,filter_by in enumerate(group):

        df = df4.merge(df1[df1.Demographic == filter_by][['Demographic','State Abbr', 'Winner', 'Biden %', 'Trump %']],
                   how='left', right_on='State Abbr', left_on='Abbreviation',)
        df.dropna(inplace=True)
        labels = df['State'].tolist()
        colors = df.Winner.replace({'Trump': "rgba(250,0,0,0.3)", 'Biden':"rgba(0,0,256,0.3)", 'UnKnown':'#D3D3D3'}).tolist()
        x_data = df.iloc[:, [-2,-1]].to_numpy()
        cur_max_val = x_data.max()
        cur_min_val = x_data.min()
        if cur_max_val > final_max_val:
            final_max_val = cur_max_val
        if cur_min_val < final_min_val:
            final_min_val = cur_min_val
        for i in range(0, df.shape[0]):
            fig.add_trace(go.Scatter(y=x_data[i], x=[labels[i], labels[i]], mode='lines',
                name=labels[i],
                line=dict(color=colors[i], width=7),
            ),row=kk+1, col=1)

            # endpoints
            fig.add_trace(go.Scatter(
                y=[x_data[i][0], x_data[i][-1]],
                x=[labels[i], labels[i]],
                mode='markers',
                hovertemplate='<b><i>%{x}&nbsp;</b></i><br>'+'%{y}%&nbsp;<extra></extra>',
                marker=dict(color=['blue','red' ], size=7)
            ),row=kk+1, col=1)

    for i,j in enumerate(group):
        fig.add_annotation(dict(x=5, y=final_max_val+10, xref='x'+str(i+1), yref='y'+str(i+1),
                               text=f'{str(j.replace("$", "USD "))}',showarrow=False,align = 'left',
                               font=dict(
                                   family="Courier New, monospace",
                                   size=13,
                                   color = "#667175",
                               )))


    fig.update_layout(title=dict(text='Comparing Similar Demographic',x = 0.5, y = 1,
                                  font=dict(size=25,family='Rockwell, monospace', color='black')),showlegend=False,margin=dict(t=50, l=30, r=30, b=10, pad = 0),
                       hoverlabel=dict(bgcolor="white",font_size=13,font_family="Rockwell"),
                      height=height_req, plot_bgcolor='#F8ECC2',paper_bgcolor='#F8ECC2', xaxis=dict(showgrid=False),)
    fig.update_xaxes(tickfont_size=8,showgrid=False,color = "#667175", gridcolor='black',categoryorder='category ascending', row=1, col=1)
    fig.update_yaxes(tickfont_size=8,showgrid=False,color = "#667175",
                     range=[final_min_val-3,final_max_val+10], tickmode='array', tickvals=[25, 50, 75], row=1, col=1)
    fig.update_xaxes(tickfont_size=8,showgrid=False,color = "#667175", gridcolor='black', row=2, col=1)
    fig.update_yaxes(tickfont_size=8,showgrid=False,color = "#667175",
                     range=[final_min_val-3,final_max_val+10], tickmode='array', tickvals=[25, 50, 75], row=2, col=1)
    fig.update_xaxes(tickfont_size=8,showgrid=False, gridcolor='black', row=3, col=1)
    fig.update_yaxes(tickfont_size=8,showgrid=False,color = "#667175",
                     range=[final_min_val-3,final_max_val+10], tickmode='array', tickvals=[25, 50, 75], row=3, col=1)
    fig.update_xaxes(tickfont_size=8,showgrid=False, gridcolor='black', row=4, col=1)
    fig.update_yaxes(tickfont_size=8,showgrid=False,color = "#667175",
                     range=[final_min_val-3,final_max_val+10], tickmode='array', tickvals=[25, 50, 75], row=4, col=1)
    fig.update_xaxes(tickfont_size=8,showgrid=False, gridcolor='black', row=5, col=1)
    fig.update_yaxes(tickfont_size=8,showgrid=False,color = "#667175",
                     range=[final_min_val-3,final_max_val+10], tickmode='array', tickvals=[25, 50, 75], row=5, col=1)

    return fig




