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
DATA_PATH = PATH.joinpath('../Week_24_Usa_university_very_expensive/').resolve()

df_new = pd.read_excel(DATA_PATH.joinpath("trimmed_data.xlsx"))
df2 = pd.read_excel(DATA_PATH.joinpath('hexmap_plots.xlsx'))
df_new = df_new.merge(df2, how='left', left_on='State', right_on='Abbreviation',)
state_stats = df_new.groupby(['State_y', 'Abbreviation', 'Row', 'Column']).agg({'$ of Loans Originated':'sum'}).reset_index().sort_values('$ of Loans Originated')

fig = go.Figure()

fig.add_traces(go.Scatter(
    x=state_stats.Column, y = state_stats.Row,
    text = ["<br>  ".join([i, "$"+ "{:,}".format(j)]) for i, j in zip(state_stats.State_y, state_stats['$ of Loans Originated'])],
    marker_symbol=14,
    marker_line_color="white",
    marker_color=state_stats['$ of Loans Originated'],
    hovertemplate = '&nbsp; %{text}</b>&nbsp;<extra></extra>',
    marker_colorscale=[[0, 'rgb(211, 234, 231)'], [0.5, 'rgb(57, 121, 173)'], [1, 'rgb(7, 69, 117)']],
    marker_line_width=0.5, marker_size=43, mode='markers'))

for i, row in state_stats.iterrows():

    fig.add_annotation(
            x=row['Column'], y = row['Row'],
            xref="x",yref="y",
            text=row['Abbreviation'],
            showarrow=False,
            font=dict(family="Rockwell, monospace",size=12,color="black"),
    #         align="center",arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="#636363",
            ax=20, ay=-30,
            opacity=0.9
            )

fig.update_layout(clickmode='event+select',
                  yaxis = dict(autorange="reversed",fixedrange=True,showgrid=False, showticklabels=False, showline=False,
                              zeroline = False),
                  xaxis = dict(fixedrange = True,showgrid = False,showticklabels=False, showline=False,zeroline = False),
                  hoverlabel=dict(bgcolor="white",font_size=15,  font_family="Rockwell"),
                  margin=dict(t=0, l=0, r=0, b=0, pad = 0),
                 height=350, width=550,
                  plot_bgcolor='#2E3D43',paper_bgcolor='#2E3D43', )

by_school = df_new.groupby(['School', 'School Type', 'State_x', 'State_y']).agg(
    {'# of Loans Originated': 'sum', '$ of Loans Originated': 'sum', 'Recipients': 'sum'}).reset_index().sort_values('$ of Loans Originated', ascending=False).reset_index(drop=True)
by_school = by_school.loc[:, ['School', 'School Type', 'State_x','State_y', '$ of Loans Originated',]]
by_school.columns = ['University', 'Type', 'State','State_full', 'Loan Originated in Dollars']
by_school['Loan Originated in Dollars'] = by_school.apply(lambda x: "{:,}".format(x[-1]), axis = 1)

heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

mmw24_viz = html.Div([
    html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910', href="https://twitter.com/abhinavk910", style={'color': "#BBBBBA"}),' for',
                html.Span(' Makeover Monday Week 22', style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.Span(' Student Loan created by University of USA',
                          style={'color': heading_color[0]}),
                ' in 2019'
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
    
    html.Div([

        html.Div([
            html.Div([
                html.H1('Which University of USA Create the Most Student Loans?', style={
                'color': "white", "text-align": "center"}, className='mb-5'),
                dcc.Graph(id='mmw24_1',
                          figure=fig,
                          config={'displayModeBar': False})], style={'width': "550px"}, className='pt-0'),
            html.Div([
                 dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[{"name": i, "id": i, "selectable": True} for i in ['University','Type', 'State', 'Loan Originated in Dollars']],
                            page_size=10,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            page_current= 0,
                            fixed_rows={'headers': True},
                            style_table={'height': '800px', 'overflowX':'auto', 'background': '#2E3D43'},
                            style_as_list_view=True,
                            style_cell={
                                'overflow': 'hidden',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'padding': '10px',
                                'textAlign': 'center',
                                'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                                'whiteSpace': 'normal'
                            },
                            style_data={
                                'backgroundColor': '#2E3D43',
                                'color':'#BCC0C7',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'lineHeight': '25px'
                            },
                     style_cell_conditional=[
                                            {
                                                'if': {'column_id': 'University'},
                                                'textAlign': 'left'
                                            }
                                        ],
                     style_header={
                                    'backgroundColor': 'rgb(25, 41, 48, 1)',
                                    'color':'#65B1D2',
                                    'fontWeight': 'bold'
                                },

                        )
            ], style={'width': '630px', 'height':'570px', 'background': '#2E3D43'}),
        ], className='d-flex flex-row justify-content-between'),
    ], style={'background': 'rgb(25, 41, 48, 0.9)', 'width': '1300px', 'min-height': '600px',
              "border-radius": "50px","box-shadow": "15px 0px 15px -10px rgba(0,0,0,0.75)"}, className='p-5'),
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
    ], style={'background': '', 'width': '1500px', 'min-height': '100px', "text-align": "center"}, className='pt-4 pl-4'),
], className='d-flex flex-column  align-items-center ', style = {'background': background_color[0]})

@app.callback(
    Output('datatable-interactivity', 'data'),
    Input('mmw24_1', 'selectedData'))
def display_click_data(clickData):
    if clickData:
        state = clickData['points'][0]['text'].split('<br>')[0]
        data = by_school[by_school.State_full == state]
        return data.iloc[:,:].to_dict('records')
    else:
        return by_school.iloc[:, :].to_dict('records')
