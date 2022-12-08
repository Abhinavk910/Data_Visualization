import pandas as pd
import pathlib

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output,State

import plotly.express as px
from plotly import graph_objs as go

from app import app

# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[
#     {"name": "viewport", "content": "width=device-width, initial-scale=1"}
# ])
# server = app.server

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../ffl_dashboard/').resolve()
df = pd.read_csv(DATA_PATH.joinpath('final_data.csv'))
countries = df.Country
columns = df.columns


def generatecard(i):
    return html.Li([
            html.Div(str(i))
        ], className = 'left-list')

def generatetable(i, j):
    html.Tr([
        html.Td(str(i), className = 'head'),
        html.Td(' :- '),
        html.Td(str(j))
    ]),

ffl_dashboard_layout =html.Div([

                html.Div([
                    # navbar
                    html.Div([
                        html.Div([
                            html.A([
                                html.Img(src='../assets/ffl_dashboard/Logos/LOGO1.png', className="image")
                            ],className = 'logo-image'),
                            html.H1('Alone, we go quickly. Together, we go further.')
                        ], className = 'logo'),
                    ], className = "navbar"),
    ########################################################################
                    # first row
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div([
                                    dcc.Loading(
                                        id="loading-1",
                                        type="default",
                                        children=dcc.Graph(id='map')
                                    )
                                ], className = ""),
                            ], id = 'map-Container'),
                        ], sm=12, md=6, lg=6, className = 'mini_container3'),

                        dbc.Col([
                            html.Div([
                                html.Div([
                                    html.H4('Year :- '),
                                    dcc.RadioItems(
                                    id='crossfilter-xaxis-type',
                                    options=[{'label': i, 'value': i} for i in ['All', 2018, 2019, 2020]],
                                    value='All',
                                    labelClassName = 'radioitem',
                                    className = 'radio'
                                    )],className = 'radioitems'),

                                html.Div(className = 'hl'),
                                html.H1('summary'),

                                html.Table([
                                    html.Tbody([
                                    html.Tr([
                                        html.Td([html.Div(id='row1col1')], className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row1col2')])
                                    ]),
                                    html.Tr([
                                        html.Td([html.Div(id='row2col1')], className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row2col2')])
                                    ]),
                                    html.Tr([
                                        html.Td([html.Div(id='row4col1')], className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row4col2')])
                                    ]),
                                    ])
                                ], style = {'color':'white'})
                            ], className = 'summary ', style = {})
                        ], sm=12, md=6, lg=6, className =  'mini_container3')
                    ], justify="center"),

    #################################################################################
                    # second row
                    dbc.Row([
                        dbc.Col([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=dcc.Graph(id='projects_quant')
                            )
                        ], sm=11, md=11, lg=6, className =  'mini_container3 adjust'),
                        dbc.Col([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=dcc.Graph(id='graph')
                            )
                        ], sm=11, md=11, lg=6, className =  'mini_container3'),
                        dbc.Col([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=dcc.Graph(id='horizontal_bar')
                            )
                        ],sm=11, md=11, lg=8, className =  'mini_container3')
                    ], justify="center"),
                ], className= 'dashboard'),

                html.Div([
                    dbc.Row([

                        dbc.Col([
                            html.Div([
                                html.H1('Axis of Intervention'),
                                html.P("We Deal in 4 Secotrs :-  Health, Education, Emergency, Protection")
                            ], className = 'heading mini_container3 animated fadeInLeft'),
                        ], sm=12, md=12, lg=6, xl=5, className = ''),
                        dbc.Col([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=dcc.Graph(id='donut')
                            )

                        ], sm=12, md=12, lg=6,xl=5, className =  'mini_container3'),
                    ], justify="center"),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H1('Our Partners'),
                                html.P('We ensures that local partners spearhead field projects')
                            ], className = 'heading mini_container3 animated fadeInLeft'),
                        ], sm=12, md=12, lg=5, xl=5, className = ''),
                        dbc.Col([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=dcc.Graph(id='graph2')
                            )
                        ], sm=12, md=12, lg=6, xl=6, className = 'mini_container3')
                    ], justify="center"),
                ], className = 'partners'),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.H1("Explore Projects and Results"),

                            dcc.Dropdown(id='select_columns2',
                                placeholder='Select type ',
                                options=[{'label': i, 'value': i} for i in df['Project title'].unique()],
                                value='Buruli ulcer screening and treatment center',
                                multi=False,
                                className = 'dropdown',
                                optionHeight = 50,
                                clearable = False
                                ),
                            html.P("These projects respond to needs expressed by the serviced community. Projects exist for "
                                    "and are led by the community, which ensures their impact and sustainability."),
                        ], className = 'heading  mini_container3 animated fadeInLeft'),
                    ],sm=12, md=12, lg=5, xl=5, className = "animated fadeInLeft"),
                    dbc.Col([
                        html.Div([
                            html.Div(className = 'hl'),
                            html.H1(id = 'title'),
                            html.Table([
                                html.Tbody([
                                    html.Tr([
                                        html.Td('Country', className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row1col22')])
                                    ]),
                                    html.Tr([
                                        html.Td(['Year'], className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row2col22')])
                                    ]),
                                    html.Tr([
                                        html.Td(['Axis of Intervention'], className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row3col22')])
                                    ]),
                                    html.Tr([
                                        html.Td('Result', className = 'head'),
                                        html.Td(' :- '),
                                        html.Td([html.Div(id='row4col22')])
                                    ]),
                                ])
                            ], style = {'color':'white'})
                        ],className = 'result', style = {})
                    ],sm=12, md=12, lg=6, xl=6, className = " result animated fadeInLeft")
                ], justify="center", className = 'result-back '),



                # footer
                dbc.Row([
                        html.P("Developed By"),
                        html.Div([
                            html.A(
                            html.H1([
                                html.Span("A"), "bhinav",html.Span('K'), "umar"
                            ]), href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                        ])
                ],justify='center', className = 'footer1')
            ], className= "body")





@app.callback([Output('map', 'clickData'),
               # Output('graph', 'clickData'),
               ],
              [Input('map-Container', 'n_clicks'),
               ])
def reset_clickData(n_clicks):
    return [None]


# summary
@app.callback([
    Output('row1col1', 'children'),
    Output('row1col2', 'children'),
    Output('row2col1', 'children'),
    Output('row2col2', 'children'),
    Output('row4col1', 'children'),
    Output('row4col2', 'children'),

            ],
    [
    Input('map', 'clickData'),
    Input('crossfilter-xaxis-type', 'value')
    ]
    )
def update_summary(clickData, year):
    if clickData is None:
        row1col1 = 'We deals in Country'
        row1col2 = '9'
        if year == 'All':
            row2col1 = 'Total Projects'
            row2col2 = '69'
            row4col1 = 'Total Budget'
            row4col2 = '€ 9,327,433'
        else:
            row2col1 = 'Total Projects in '+ str(year)
            row2col2 = '23'
            row4col1 = 'Total Budget in '+ str(year)
            row4col2 = '€ ' + '{:0,}'.format(int(df.groupby(['Year'])['Voted Year project budget €'].sum()[year]))
    if clickData is not None:
        row1col1 = 'Name of Country'
        row1col2 = [clickData['points'][0]['hovertext']][0]
        if year == 'All':
            row2col1 = 'Total Projects'
            row2col2 = df.Country.value_counts()[row1col2]
            row4col1 = 'Total Budget'
            row4col2 = '€ '+ '{:0,}'.format(int(df.groupby(['Country','Year'])['Voted Year project budget €'].sum()[row1col2].sum()))
        else:
            row2col1 = 'Total Projects in '+ str(year)
            row2col2 = df.groupby(['Country', 'Year']).size()[row1col2][year]
            row4col1 = 'Total Budget in '+ str(year)
            row4col2 = '€ '+ '{:0,}'.format(int(df.groupby(['Country','Year'])['Voted Year project budget €'].sum()[row1col2][year]))

    # print(row1col1, row1col2)
    return [row1col1, row1col2, row2col1, row2col2, row4col1, row4col2,]

# map
@app.callback([
    Output('map', 'figure'),
    ],
    [
    Input('map', 'clickData'),
    Input('crossfilter-xaxis-type', 'value'),
    ])
def update_map(clickData, year):
    if clickData is None:
        if year != 'All':
            df_con_bud = df.groupby(['Country', 'Year']).agg({'Voted Year project budget €':'sum'}).reset_index().rename(columns = {'Voted Year project budget €': 'Total Budget'})
            df_con_bud = df_con_bud[df_con_bud.Year == year]
            df_con_bud['Percentage'] = df_con_bud['Total Budget']/df_con_bud['Total Budget'].sum()
            fig1 = px.choropleth(df_con_bud, locations="Country",
                            locationmode = 'country names',
                            color="Total Budget", # lifeExp is a column of gapminder
                            hover_name="Country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma,
                            hover_data={'Country': False,
                                        'Total Budget': False,
                                        'Budget in ' + str(year) + " (in €) ": (':0,',df_con_bud['Total Budget']),
                                        'Percentage of Budget in '+ str(year)+" ":(':.1%', df_con_bud['Percentage'])})
        else:
            df_con_bud = df.groupby(['Country']).agg({'Voted Year project budget €':'sum'}).reset_index().rename(columns = {'Voted Year project budget €': 'Total Budget'})
            df_con_bud['Percentage'] = df_con_bud['Total Budget']/df_con_bud['Total Budget'].sum()
            fig1 = px.choropleth(df_con_bud, locations="Country",
                            locationmode = 'country names',
                            color="Total Budget", # lifeExp is a column of gapminder
                            hover_name="Country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma,
                            hover_data={'Country': False,
                                        'Total Budget': False,
                                        'Total Budget (in €) ' : (':0,',df_con_bud['Total Budget']),
                                        'Percentage of Total Budget ' :(':.1%', df_con_bud['Percentage'])})
    else:
        if year != 'All':
            df_con_bud = df.groupby(['Country', 'Year']).agg({'Voted Year project budget €':'sum'}).reset_index().rename(columns = {'Voted Year project budget €': 'Total Budget'})
            df_con_bud = df_con_bud[(df_con_bud.Year == year)& (df_con_bud.Country == [clickData['points'][0]['hovertext']][0])]
            df_con_bud['Percentage'] = df_con_bud['Total Budget']/df_con_bud['Total Budget'].sum()
            fig1 = px.choropleth(df_con_bud, locations="Country",
                            locationmode = 'country names',
                            color="Total Budget", # lifeExp is a column of gapminder
                            hover_name="Country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma,
                            hover_data={'Country': False,
                                        'Total Budget': False,
                                        'Budget in ' + str(year) + " (in €) ": (':0,',df_con_bud['Total Budget']),
                                        })
        else:
            df_con_bud = df.groupby(['Country']).agg({'Voted Year project budget €':'sum'}).reset_index().rename(columns = {'Voted Year project budget €': 'Total Budget'})
            df_con_bud['Percentage'] = df_con_bud['Total Budget']/df_con_bud['Total Budget'].sum()
            df_con_bud = df_con_bud[df_con_bud.Country == [clickData['points'][0]['hovertext']][0]]
            fig1 = px.choropleth(df_con_bud, locations="Country",
                            locationmode = 'country names',
                            color="Total Budget", # lifeExp is a column of gapminder
                            hover_name="Country", # column to add to hover information
                            color_continuous_scale=px.colors.sequential.Plasma,
                            hover_data={'Country': False,
                                        'Total Budget': False,
                                        'Budget in ' + str(year) + "years (in €) ": (':0,',df_con_bud['Total Budget']),
                                        })


    fig1.layout = dict(geo = dict(scope='africa'))
    fig1.update_layout(clickmode='event+select',
                        margin=dict(t=80, l=10, r=10, b=10),
                        paper_bgcolor = 'rgb(0,0,0, 0.2)',
                        plot_bgcolor = 'rgb(0,0,0, 0.2)',
                        title_text='<a href="https://ffl.lu/"> Fondation Follereau Luxembourg are working in ',
                        font_family="Rockwell",
                        autosize=True,
                        # coloraxis_showscale=False,
                        )
    fig1.update_coloraxes(colorbar = dict(
                            thickness = 20,
                            len = 1,
                            x = 0.05,
                            ypad = 30,),
                        colorbar_tickfont=dict(
                            size = 15,
                            color = '#fff',
                            family = "Open Sans"),
                        colorbar_title=dict(
                            text = "Budget"),
                        colorbar_title_font=dict(
                            family = "Open Sans",
                            size = 20,
                            color = '#fff'))

    fig1.update_geos(fitbounds="locations")
    fig1.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)',landcolor="rgba(0,0,0,0.5)",showocean=True, oceancolor="rgba(0,0,0,0.2)", lakecolor="rgba(0,0,0,0.5)"  ))

    return [fig1]


#whole country budget
@app.callback([
    Output('graph', 'figure'),
    ],
    [Input('map', 'clickData'),
     Input('crossfilter-xaxis-type', 'value'),
     ]
    )
def update_country_data(clickData, year):

    if clickData is None:
        selected_country = countries
    else:
        selected_country  = [clickData['points'][0]['hovertext']]

    if clickData is None  and year == 'All':

        df_con_bud = df.groupby(['Country', 'Year']).agg({'Voted Year project budget €':'sum'}).reset_index()
        fig = px.area(df_con_bud, x="Year", y="Voted Year project budget €",
              color="Country",
              line_group="Country",
              # groupnorm='percent'
             )
        # fig.update_layout(hovermode="x unified")


    elif clickData is None and year != 'All':
        df_con_bud = df.groupby(['Country', 'Year']).agg({'Voted Year project budget €':'sum'}).reset_index()
        df_con_bud2 = df_con_bud[(df_con_bud.Year == year)]
        fig = px.pie(df_con_bud2, values='Voted Year project budget €', names='Country', title='Country',hole=.3
                    )
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig.update_traces(hoverinfo='name+value',textinfo='label+percent', textfont_size=15,textposition='inside', insidetextorientation='radial',
                          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.update_layout(uniformtext_minsize=12,showlegend= False)

        #                  annotations=[dict(text='Country', x=0.5, y=0.5, font_size=20, showarrow=False)])
    elif clickData is not None and year == 'All':
        df_con_bud = df.groupby(['Country', 'Year', ]).agg({'Voted Year project budget €':'sum'}).reset_index()
        df_con_bud2 = df_con_bud[(df_con_bud.Country == [clickData['points'][0]['hovertext']][0])]
        fig = px.area(df_con_bud2, x="Year", y="Voted Year project budget €",
              color='Country',
              line_group='Country',
              # groupnorm='percent'
             )
        # fig.update_layout(hovermode="x unified")

    elif clickData is not None and year != 'All':
        df_con_bud = df.groupby(['Country','Year', ]).agg({'Voted Year project budget €':'sum'}).reset_index()
        df_con_bud2 = df_con_bud[(df_con_bud.Year == year) &  (df_con_bud.Country == [clickData['points'][0]['hovertext']][0])]
        fig = px.pie(df_con_bud2, values='Voted Year project budget €', names='Country', title='Budget allocation',hole=.3
                    )
        fig.update_traces(hoverinfo='name+value',textinfo='label+percent', textfont_size=15,textposition='inside', insidetextorientation='radial',
                          marker=dict( line=dict(color='#000000', width=2)))
        fig.update_layout(uniformtext_minsize=12,showlegend= False)
        #                  annotations=[dict(text='Country', x=0.5, y=0.5, font_size=20, showarrow=False)])

    fig.update_layout(
    #     hovermode="x unified"
        title = dict(
            text = "Country Budget Allocation by Year",
            font = dict(
                family = "PT Sans Narrow",
                size = 20,
                color = '#14C8FF'),
            x = 0.5
        ),
        legend = dict(
            bgcolor = "rgba(0,0,0,0.3)",  borderwidth = 0.1,  font = dict( family = "PT Sans Narrow",  size = 15,  color = '#fff'),
            orientation = 'h', xanchor = 'left',  yanchor = "bottom", x = 0, y = -0.5, title = dict( text = "Year", font = dict(
            family = "PT Sans Narrow", size = 20, color = '#fff'), side = 'left' )),
        margin={'l': 60, 'b': 60, 't': 50, 'r': 10},
        margin_autoexpand = True,
        autosize = True,
    #     width = 00,
    #     height = 600,
        hovermode='closest',
        paper_bgcolor = 'rgb(0,0,0, 0.1)',
        plot_bgcolor = 'rgb(0,0,0, 0.1)',
        )

    fig.update_yaxes(
        color = '#fff',
        title = dict(
            text = "Budget(in €)",
            standoff = 10
        ),
        showline = False, # solid line in the  x = 0
        showgrid = False,
        showdividers = False,
    )
    fig.update_xaxes(
        color = '#fff',

        title = dict(
            text = "",
            standoff = 10
        ),

        showgrid = False,
        zeroline = False,
        showdividers = False,
        tick0 = 2017,
        dtick = 1
    ),
    return [fig]

# direct beneficiaries
@app.callback([
    Output('horizontal_bar', 'figure'),
    ],
    [Input('map', 'clickData'),
     Input('crossfilter-xaxis-type', 'value'),
     ]
    )
def direct_benefi(clickdata, year):

    if clickdata is None:
        df_con_bud = df.groupby(['Direct beneficiaries', 'Year']).agg({'Voted Year project budget €':['sum', 'count']}).reset_index()
        df_con_bud.columns = df_con_bud.columns.get_level_values(0)
        df_con_bud.columns = ['Direct beneficiaries', 'Year', 'Voted Year project budget €_sum', 'No. of Projects']
        df_con_bud.Year = df_con_bud.Year.astype('str')
        if year != 'All':
            df_con_bud = df_con_bud[df_con_bud.Year == str(year)]
        fig = px.bar(df_con_bud, x='Voted Year project budget €_sum', y="Direct beneficiaries", orientation='h',
             color='Year',
            hover_data={'Year': False,
                        'Direct beneficiaries': False,
                        'Voted Year project budget €_sum':False,
                        'Budget(in €)' : (':0,',df_con_bud['Voted Year project budget €_sum'])},
             hover_name='Direct beneficiaries',
             title='Direct beneficiaries from project')

    else:
        df_con_bud = df.groupby(['Country','Direct beneficiaries', 'Year']).agg({'Voted Year project budget €':['sum', 'count']}).reset_index()
        df_con_bud.columns = df_con_bud.columns.get_level_values(0)
        df_con_bud.columns = ['Country','Direct beneficiaries', 'Year', 'Voted Year project budget €_sum', 'Voted Year project budget €_count']
        df_con_bud.Year = df_con_bud.Year.astype('str')
        if year != 'All':
            df_con_bud = df_con_bud[(df_con_bud.Country == [clickdata['points'][0]['hovertext']][0]) & (df_con_bud.Year == str(year))]
        else:
            df_con_bud = df_con_bud[(df_con_bud.Country == [clickdata['points'][0]['hovertext']][0])]
        fig = px.bar(df_con_bud, x='Voted Year project budget €_sum', y="Direct beneficiaries", orientation='h',
                     color='Year',
                     hover_data={'Year': False,
                        'Direct beneficiaries': False,
                        'Voted Year project budget €_sum':False,
                        'Voted Year project budget €_count':False,
                        'Budget(in €)' : (':0,',df_con_bud['Voted Year project budget €_sum'])},
                     hover_name='Direct beneficiaries',
                     title='Direct beneficiaries from project')

    fig.update_xaxes(title='Budget', type='log', showgrid = False, color = '#fff')
    fig.update_layout(legend = dict(borderwidth = 0.1,font = dict(family = "PT Sans Narrow",size = 15,color = '#fff'),
                                    tracegroupgap = 0,xanchor = 'right',x = 0.95,y = 0.98, title = dict(text = "  Year",
                                    font = dict(family = "PT Sans Narrow",size = 20),side = 'top')))

    fig.update_yaxes(title='', color = '#fff')
    fig.update_layout(margin={'l': 50, 'b': 60, 't': 80, 'r': 0}, hovermode='closest',
                    title = dict(
                        font = dict(
                            family = "PT Sans Narrow",
                            size = 20,
                            color = '#14C8FF'),
                        x = 0.5
                    ),
                    paper_bgcolor = 'rgb(0,0,0, 0.1)',
                    plot_bgcolor = 'rgb(0,0,0, 0.1)',)
    fig.update_layout(barmode='stack')
    return [fig]

# no. of projects
@app.callback([
    Output('projects_quant', 'figure'),
    ],
    [Input('map', 'clickData'),
     Input('crossfilter-xaxis-type', 'value'),
     ]
    )
def direct_benefi(clickdata, year):

    if clickdata is None:
        df_con_bud = df.groupby(['Country', 'Year']).agg({'Voted Year project budget €':'sum', 'Project title':'count'}).reset_index()
        df_con_bud.Year = df_con_bud.Year.astype('str')
        if year != 'All':
            df_con_bud = df_con_bud[df_con_bud.Year == str(year)]
        fig = px.bar(df_con_bud, x='Project title', y="Country", orientation='h',
                     color='Year',
                     hover_data={'Country': False,
                         'Year':False,
                         'Project title': False,
                         'Budget' + " (in €) ": (':0,',df_con_bud['Voted Year project budget €'])},
                     hover_name='Project title',
                     title='Direct beneficiaries from project')
    else:
        df_con_bud = df.groupby(['Country', 'Year']).agg({'Voted Year project budget €':'sum', 'Project title':'count'}).reset_index()
        df_con_bud.Year = df_con_bud.Year.astype('str')
        if year != 'All':
            df_con_bud = df_con_bud[(df_con_bud.Country == [clickdata['points'][0]['hovertext']][0]) & (df_con_bud.Year == str(year))]
        else:
            df_con_bud = df_con_bud[(df_con_bud.Country == [clickdata['points'][0]['hovertext']][0])]
        fig = px.bar(df_con_bud, x='Project title', y="Country", orientation='h',
                     color='Year',
                     hover_data={'Country': False,
                         'Year':False,
                         'Project title': False,
                         'Budget' + " (in €) ": (':0,',df_con_bud['Voted Year project budget €'])},
                     hover_name='Project title',
                     title='Direct beneficiaries from project')

    fig.update_layout(
        title = dict(
            text = "Number of projects",
            font = dict(
                family = "PT Sans Narrow",
                size = 22,
                color = '#14C8FF'),
            x = 0.4
        ),
        legend = dict(
            bgcolor = "rgba(0,0,0,0.3)",  borderwidth = 0.1,  font = dict( family = "PT Sans Narrow",  size = 15,  color = '#fff'),
            orientation = 'h', xanchor = 'left',  yanchor = "bottom", x = 0, y = -0.5, title = dict( text = "Year", font = dict(
            family = "PT Sans Narrow", size = 20, color = '#fff'), side = 'left' )),
        margin={'l': 60, 'b': 60, 't': 80, 'r': 10},
        margin_autoexpand = True,
        autosize = True,
        paper_bgcolor = 'rgb(0,0,0, 0.2)',
        plot_bgcolor = 'rgb(0,0,0, 0.2)',
        hoverlabel = dict(
            bgcolor = '#fff',
            bordercolor = '#000'
        ),
        # transition = dict(
        #     duration= 500,
        #     easing= 'cubic-in-out',
        #     ordering = "layout first"
        # ),
        barmode = 'stack',
        bargap = 0.2,
    )
    fig.update_yaxes(
        color = '#fff',
        title = "",
        type = "category",
        showdividers = False,
    )

    fig.update_xaxes(
        color = '#fff',
        title = "",
        showgrid = False,
        zeroline = False,
        tick0 = 0,
        dtick = 1
    ),


    return [fig]

# axis of intervention
@app.callback([
    Output('donut', 'figure'),
    ],
    [
    Input('map', 'clickData'),
    Input('crossfilter-xaxis-type', 'value'),
     ]
    )
def plot_donut(clickData, year):

    if clickData is None  and year == 'All':
        df_con_bud2 = df.groupby(['Axis of intervention', 'Year']).agg({'Voted Year project budget €':'sum','Project title':'size' }).reset_index()
        fig = px.area(df_con_bud2, x="Year", y="Voted Year project budget €",
              color="Axis of intervention",
              line_group="Axis of intervention",
              # groupnorm='percent'
             )
    elif clickData is not None and year == 'All':
        df_con_bud = df.groupby(['Country','Axis of intervention', 'Year', ]).agg({'Voted Year project budget €':'sum','Project title':'size' }).reset_index()
        df_con_bud2 = df_con_bud[(df_con_bud.Country == [clickData['points'][0]['hovertext']][0])]
        fig = px.area(df_con_bud2, x="Year", y="Voted Year project budget €",
              color="Axis of intervention",
              line_group="Axis of intervention",
              # groupnorm='percent'
             )
    elif clickData is not None and year != 'All':
        df_con_bud = df.groupby(['Country','Axis of intervention', 'Year', ]).agg({'Voted Year project budget €':'sum','Project title':'size' }).reset_index()
        df_con_bud2 = df_con_bud[(df_con_bud.Year == year) &  (df_con_bud.Country == [clickData['points'][0]['hovertext']][0])]
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig = px.pie(df_con_bud2, values='Voted Year project budget €', names='Axis of intervention', title='Budget allocation',hole=.3
                    )
        fig.update_traces(hoverinfo='name+value',textinfo='label+percent', textfont_size=15,textposition='inside', insidetextorientation='radial',
                          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.update_layout(uniformtext_minsize=12,showlegend = False,
                         annotations=[dict(text='Sector', x=0.5, y=0.5, font_size=20, showarrow=False)])

    elif clickData is None and year != 'All':
        df_con_bud = df.groupby(['Axis of intervention', 'Year']).agg({'Voted Year project budget €':'sum','Project title':'size' }).reset_index()
        df_con_bud2 = df_con_bud[(df_con_bud.Year == year)]
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig = px.pie(df_con_bud2, values='Voted Year project budget €', names='Axis of intervention', title='Budget allocation',hole=.3
                    )
        fig.update_traces(hoverinfo='name+value',textinfo='label+percent', textfont_size=15,textposition='inside', insidetextorientation='radial',
                          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.update_layout(uniformtext_minsize=12,showlegend = False,
                         annotations=[dict(text='Sector', x=0.5, y=0.5, font_size=20, showarrow=False)])

    fig.update_layout(title = dict(
                        text = "Budget allocation by axis of intervention", font = dict(family = "PT Sans Narrow", size = 20, color = '#14C8FF'),
                        x = 0.5),
                    legend = dict(
                        bgcolor = "rgba(0,0,0,0.3)",  borderwidth = 0.1,  font = dict( family = "PT Sans Narrow",  size = 15,  color = '#fff'),
                        orientation = 'h', xanchor = 'left',  yanchor = "bottom", x = 0, y = -0.5, title = dict( text = "Year", font = dict(
                        family = "PT Sans Narrow", size = 20, color = '#fff'), side = 'left' )),
                    margin={'l': 60, 'b': 60, 't': 50, 'r': 10},
                    margin_autoexpand = True,
                    autosize = True,
                    hovermode='closest',
                    paper_bgcolor = 'rgb(0,0,0, 0.1)',
                    plot_bgcolor = 'rgb(0,0,0, 0.1)')
    fig.update_yaxes(color = '#fff', title = dict( text = "Money allocated(in €)", standoff = 10), showline = False, showgrid = False,
                    showdividers = False,)
    fig.update_xaxes(color = '#fff', title = dict( text = "", standoff = 10), showgrid = False, zeroline = False, showdividers = False,
                    tick0 = 2017,dtick = 1)
    return [fig]

# Partners
@app.callback([
                Output('graph2', 'figure'),
               ],
              [
              Input('crossfilter-xaxis-type', 'value'),
               ])
def up(value):
    df_con_bud = df.groupby([ 'Local partner', 'Country','Year']).size().reset_index()
    df_con_bud.rename(columns={0:'Total'}, inplace=True)
    fig = px.sunburst(df_con_bud,
                    path=['Local partner', 'Country'],
                    color='Total',
                    color_continuous_scale= 'Blues',
                    hover_name='Local partner',
                    hover_data = {'Local partner': False,
                                  'Country':False,
                                  'No. of Projects':df_con_bud['Total'],
                                  'Total' :False},

                    )
    fig.update_layout(
                        margin={'l': 60, 'b': 60, 't': 50, 'r': 10},
                        margin_autoexpand = True,
                        autosize = True,
                        hovermode='closest',
                        paper_bgcolor = 'rgb(0,0,0, 0.1)',
                        plot_bgcolor = 'rgb(0,0,0, 0.1)',
                        font_family="Rockwell",
                        font_color = '#000'
                        )
    fig.update_traces(
        hovertemplate='<b>%{label} </b> <br> No. of Projects: %{color}',
    )
    fig.update_coloraxes(
                showscale = False
                )
    return [fig]

#results
@app.callback([
    Output('row1col22', 'children'),
    Output('row2col22', 'children'),
    Output('row3col22', 'children'),
    Output('row4col22', 'children'),
    Output('title', 'children')
            ],
    [
    # Input('map', 'clickData'),
    Input('select_columns2', 'value')
    ]
    )
def results(value):

    df_con_bud = df.groupby(['Project title', 'Country', 'Year','Axis of intervention','Final_result']).size().reset_index()
    countries = ",".join(df_con_bud[df_con_bud['Project title'] == value].Country.unique())
    years = ", ".join([str(i) for i in df_con_bud[df_con_bud['Project title'] == value].Year.unique()])
    intervention = ", ".join([str(i) for i in df_con_bud[df_con_bud['Project title'] == value]['Axis of intervention'].unique()])

    result = list(df_con_bud[df_con_bud['Project title'] == value].Final_result.unique())

    results = []
    for i in result:
        try:
            for j in i.split(" $% "):
                if j!="":
                    results.append(j)
        except:
            continue

    code = html.Ul([
        generatecard(i) for i in results
    ], className = 'list_result')
    return [countries, years,intervention, code, value]


if __name__ == '__main__':
    app.run_server(debug=True)
