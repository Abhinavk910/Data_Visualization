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

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_16_US_Aeroplane_Passengers/').resolve()




us_plane_layout = dbc.Container([
    dbc.Row([
        dbc.Col([

            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.P([html.Span('COVID-19 Impact ', style = {'color':'#ea686e', 'font-size': "30px"} ),
                               html.Span('on ', style = {'color':'rgb(37,37,37)', 'font-size': "25px"} ),
                               html.Span('U.S. Air Travel', style = {'color': 'rgb(189,189,189)','font-size': "30px"})], id = 'text', className = '' ),
                        html.P(['Spread of the novel coronavirus has caused passenger demand to collapse. April, 2020 registered',
                        html.Span(' 96%', style = {'font-size': '40px', 'color':'#ea686e'}),
                        html.P(['decrese in total passengers compare to average of last 5 years.'])]),
                    ], className = '')
                ],className = "ml-0 p-0",style = {'background': '',}),
            ], className = 'd-flex flex-column')
        ], width=4, className = "ml-0 p-0", style = {'background': '',}),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart-usairlines',config={'displayModeBar': False},
                              figure={},),
                ])
            ]),
        ], width=8),
    ],className='ml-1 mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart-usairlines',
                    config={'displayModeBar': False},
                    figure={}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart2-usairlines',
                    config={'displayModeBar': False},
                    figure={}),
                ])
            ]),
        ], width=6),
    ],className='mb-2'),
    dbc.Row([
            html.Div([
                html.P(['Data Source: Bureau of Transportation Statistics']),
                html.A(html.P('Get Data'), href='https://data.world/makeovermonday/2021w16', target = "_blank")
            ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
            html.Div([
                html.P("Developed By: "),
                html.Div([
                    html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                    href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                ])
            ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
    ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})

], fluid=True)



@app.callback(
    Output('bar-chart2-usairlines','figure'),
    Input('text', 'children')
)
def generatebar2(dd):
    df = pd.read_csv(DATA_PATH.joinpath('total_flight.csv'))
    years = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years,
                         y=df.query('Type2 == "Y"')['Count_of_flight'].astype('int').reset_index(
                             drop=True) - df.query('Type2 == "N"')['Count_of_flight'].astype('int').reset_index(
                             drop=True),
                         name='In USA',
                         marker_color='#ea686e',
                         ))

    fig.update_traces(marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1)
    fig.update_layout(
        height = 250,
        plot_bgcolor='white',
        title='<b>Number of Flight change in 2020 compare to 5 years Avg.',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        margin=dict(
            autoexpand=False,
            l=50,
            r=20,
            t=40,
            b=40,
        ),
        legend=dict(
    #         x=0,
    #         y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='overlay',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
    #         opacity = 0.2
    )
    return fig


@app.callback(
    Output('bar-chart-usairlines','figure'),
    Input('text', 'children')
)
def generatebar(dd):
    df = pd.read_csv(DATA_PATH.joinpath('groupby_movement_in_out.csv'))

    in_usa = df[df.Type == 'in_usa']
    out_usa = df[df.Type == 'out_usa']

    years = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years,
                         y=in_usa.query('Type2 == "Y"')['Total_Passengers'].reset_index(
                             drop=True),
                         name='Arrieve USA',
                         marker_color='rgb(189,189,189)',
                         ))
    # fig.add_trace(go.Bar(x=years,
    #                 y=in_usa.query('Type2 == "Y"')['Total_Passengers'],
    #                 name='In USA in 2020',
    #                 marker_color='#ea686e'
    #                 ))
    fig.add_trace(go.Bar(x=years,
                         y=out_usa.query('Type2 == "Y"')['Total_Passengers'].reset_index(
                             drop=True),
                         name='Departure USA',
                         marker_color='#ea686e'
                         ))
    # fig.add_trace(go.Bar(x=years,
    #                 y=-1*out_usa.query('Type2 == "Y"')['Total_Passengers'],
    #                 name='Out USA in 2020',
    #                 marker_color='#ea686e'
    #                 ))
    fig.update_traces(marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1)
    fig.update_layout(
        height = 250,
        plot_bgcolor='white',
        title='<b>Flow of Passenger In and Out of USA in 2020',
        font=dict(family='Arial',
                  size=15,
                  color='rgb(37,37,37)'),
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='',
            titlefont_size=16,
            tickfont_size=14,
        ),
        margin=dict(
            autoexpand=False,
            l=50,
            r=20,
            t=40,
            b=40,
        ),
        legend=dict(
            x=0.7,
            y=0.7,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        #     opacity = 0.2
    )
    return fig



@app.callback(
    Output('line-chart-usairlines','figure'),
    Input('text', 'children')
)
def generateline(dd):
    dd = pd.read_csv(DATA_PATH.joinpath('groupby_mean_passenger.csv'))



    labels = ['Avg of last 5 years', '2020']
    colors = ['rgb(189,189,189)','#ea686e']

    mode_size = [8, 12]
    line_size = [4, 6]

    x_data = np.vstack((np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']),)*2)

    y_data = np.array([
        dd.query('Type == "N"')['Total_Passengers'].tolist(),
        dd.query('Type == "Y"')['Total_Passengers'].tolist(),
    ])

    fig = go.Figure()

    for i in range(0, 2):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))

        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(

            showline=False,
    #         showgrid=True,
    #         gridcolor = 'black',
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
    #         showgrid=True,
            zeroline=False,
            showline= True,
            showticklabels=True,
            showgrid=True,
            gridcolor = 'rgb(150,150,150)',
            ticksuffix = "   ",
        ),
        height = 250,
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=40,
            b=30,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []


    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text=f'<b><span style="font-size: 25px;color:#ea686e;">2020</span> vs <span style="font-size: 25px;color:rgb(189,189,189);">Average of last 5 years</span> ',
                                  font=dict(family='Arial',
                                            size=20,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.19,
                                  xanchor='center', yanchor='top',
                                  text='Data Source: Bureau of Transportation Statistics',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))

    fig.update_layout(annotations=annotations)

    return fig
