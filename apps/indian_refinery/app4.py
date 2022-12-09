import pandas as pd
import pathlib

import dash
from dash import dcc, html,  Input, Output, State
import dash_bootstrap_components as dbc


import plotly.express as px
from plotly import graph_objs as go

from app import app


# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[
#     {"name": "viewport", "content": "width=device-width, initial-scale=1"}
# ])
# server = app.server
# Lorem = "asdfasfsdfasd"

# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
# app.config.assets_folder = 'assets'     # The path to the assets folder.
# app.config.include_asset_files = True   # Include the files in the asset folder
# app.config.assets_external_path = ""    # The external prefix if serve_locally == False
# app.config.assets_url_path = '/assets'



PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../indian_refinery/').resolve()


df = pd.read_excel(DATA_PATH.joinpath('data/refinery.xlsx'))
sector = df['Sector'].unique()
company = df['short'].unique()
sector_dic = {'PSU' : ['IOCL', 'HPCL','BPCL','CPCL', 'NRL','MRPL','ONGC'],
              'JV' : ['BORL','HMEL'],
              'PRIVATE' : ['RIL','EOL']}

df2 = pd.read_excel(DATA_PATH.joinpath('data/refinery.xlsx'), sheet_name='summary')
ddf3 = df2.set_index('Sector').stack().to_frame().reset_index().round(2)
ddf3.columns = ['Year', 'Sector', 'Refinery Capacity']




refinery_layout =html.Div([
                    html.Link(
                        rel='stylesheet',
                        href='../apps/indian_refinery/assets/style.css'
                    ),
                    dbc.Container([
                        html.Div([
                            html.Div([
                                html.H1("India Refinery Capacity Overview")
                            ], className = 'headingdata'),
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.H5("Explore distribution of Refineries in India", className="card-title"),

                                        dbc.Container([
                                            dbc.Label("Select by Sector"),
                                            dcc.Dropdown(

                                                id="sector",
                                                value = [],
                                                multi=True,
                                            ),
                                            ], className = ""),
                                        dbc.Container([
                                            dbc.Label("Select by Owner"),
                                            dcc.Dropdown(
                                                id="company",
                                                value = [],
                                                multi=True,
                                            ),
                                            ]),
                                        dbc.Container([
                                            dbc.Label("Select Sunburst Chart Value"),
                                            dcc.Dropdown(id='sortvalue',
                                                placeholder='Select type ',
                                                options=[{'label': i, 'value': j} for i, j in {"No. of Refineries" : 'Count', 'Refinery Capacity' : 'Sum'}.items()],
                                                value='Sum',
                                                multi=False
                                            ),
                                            ]),
                                        html.Hr(),
                                        dbc.Container([
                                            dbc.Label("Click on any refinery to get more information"),
                                            dcc.Markdown(id='plant_summary')
                                            ]),
                                        ])
                                ], className = "box box1 mini_container1"),
                                html.Div([
                                    html.H6(
                                        id = "totalrefinery"
                                    ),
                                    html.P("Total Refineries", style = {'textAlign': 'center'})

                                ], className = "box box2 mini_container"),
                                html.Div([
                                    html.H6(
                                        id = "totalrefinerycapacity"
                                    ),
                                    html.P("Total Refineries Capacity(MMTPA)", style = {'textAlign': 'center'})

                                ], className = "box box3 mini_container"),
                                html.Div([
                                    dbc.Col(dcc.Graph(id='map1',clickData={'points': [{'hovertext': 'Digboi Refinery'}]}))

                                ], className = "box box6 mini_container"),

                            ], className = "inputdata"),

                            html.Div([
                                html.Div([
                                    dbc.Col(dcc.Graph(id='graphh'))
                                ], className = 'box box7 mini_container'),

                                html.Div([
                                    dbc.Col(dcc.Graph(id='graph2h'))
                                ], className = 'box box8 mini_container')

                            ], className = 'inputdata2')
                        ], className = 'main'),

                    html.Div([
                            html.Div([
                                html.A('Source', href = 'http://petroleum.nic.in/documents/reports/annual-reports', target="_blank")
                            ], className = "footer__copyright"),
                            html.Div([
                                html.A('Developed by Abhinav Kumar', href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                            ], className = "footer__signature"),

                    ], className = "footer")
                    ], fluid=True),
                    ])



@app.callback([
    Output('company', 'options'),
    Output('sector', 'options')
    ],
    [
    Input('sector', 'value'),
    Input('company', 'value')
    ])
def update_date_dropdown(name1, name2):
    if len(name1) == 0:
        name1 = sector
    if len(name2) == 0:
        name2 = company
    companies = [{'label': i, 'value': i} for i in [sect for sec in name1 for sect in sector_dic[sec]]]
    sector_list = [{'label': i, 'value': i} for i in set([j for i in name2 for j in set(df[df.short == i].Sector)])]
    return companies, sector_list



@app.callback([
    Output('map1', 'figure'),
    Output('graphh', 'figure'),
    Output('graph2h', 'figure'),
    Output('totalrefinery', "children"),
    Output('totalrefinerycapacity', "children")],
    [Input('sector', 'value'),
    Input('company', 'value'),
    Input('sortvalue', 'value')])
def update_map(sectors, companys, sortvalue):
    sectorcheck = sectors
    ownercheck = companys
    if sortvalue == 'Count':
        if len(sectors) != 0 or len(companys) != 0:
            titled = 'No. of Refinery' + "  (Filter Selected)  "
        else:
            titled = 'No. of Refinery'
    else:
        if len(sectors) != 0 or len(companys) != 0:
            titled = 'Refinery Capacity(MMTPA)' + "  (Filter Selected)  "
        else:
            titled = 'Refinery Capacity(MMTPA)'


    # print(countries, power)
    if len(sectors) == 0:

        sectors = sector
    if len(companys) == 0:

        companys = company
    dff = df[df.Sector.isin(sectors)]
    dfff = dff[dff.short.isin(companys)]
    totalnumber = dfff.shape[0]
    totalcapacity = round(dfff.loc[:, ["Refining Capacity (2019-2020) (MMTPA)"]].sum(),2)
    fig = px.scatter_mapbox(dfff, lat="Latitude", lon="Longitude",
                        hover_name="Name",
                         hover_data=["Owner", 'Year of Commissioning', 'Sector', "barrels per day", "Refining Capacity (2019-2020) (MMTPA)" ],
                        color="Owner",zoom=2.5,
                        opacity = 0.6,
                        mapbox_style='carto-positron',
                        labels = {'primary_fuel': 'Primary fuel'},
                        size = 'Refining Capacity (2019-2020) (MMTPA)',
                        # width = 700,
                        # height = 450
                        )

    fig.update_layout( # customize font and legend orientation & position

    # font and legend
    font_family="Rockwell",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    paper_bgcolor="#f9f9f9",
         legend =  dict(
    title = 'Owner',
    xanchor="center",
    yanchor = "top",
    y=-0.1,
    x=0.9,
    orientation = "h",
    bgcolor = '#f9f9f9'
    )
    )


    dfff['Refining Capacity (2019-2020) (MMTPA)'] = dfff['Refining Capacity (2019-2020) (MMTPA)'].astype(float)
    Grouped = dfff.groupby(['Country','Sector', "short",'State','Name']).agg({'Refining Capacity (2019-2020) (MMTPA)': sortvalue.lower()}).reset_index().round(decimals=2)
    Grouped.columns = ['Country','sector', 'company', 'state', 'Name','count']



    graph = px.sunburst(Grouped,path=['Country','sector', 'company', 'state', 'Name'],
                        values='count',template = 'ggplot2',
                        hover_name = "count", title = titled,
                        hover_data = {'sector':False, 'company':False, 'state':False},
                        # height = 96,
                        )

    graph.update_traces(textinfo = 'label+percent entry ',)

    graph.update_layout(font_family="Rockwell",
    autosize=True,
    paper_bgcolor = "#f9f9f9",
    margin=go.layout.Margin(l=0, r=0, t=30, b=10),
        legend=dict(
                title= titled, orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"
        )
    )

    # bar graph
    if (len(ownercheck) != 0) or (len(sectorcheck)!= 0):


        if len(ownercheck) == 0:
            check = 'Sector'
            checkout = 'short'
            incheck = sectorcheck
        else:
            check = 'short'
            checkout = 'Sector'
            incheck = ownercheck
        ddf = df[df[check].isin(incheck)]
        ddf = ddf.iloc[:,5:19].drop(['Year of Commissioning', checkout ], axis = 1).set_index(check)
        ddf.columns = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        ddf = ddf.stack().to_frame().reset_index().round(2)
        ddf[check] = ddf[check].astype("category")
        ddf["level_1"] = ddf["level_1"].astype('str')
        ddf = pd.pivot_table(ddf, index = [check], columns=["level_1"], values = 0, aggfunc=[sum])
        ddf = ddf.unstack().to_frame().reset_index().round(2).drop(['level_0'], axis = 1)
        ddf.columns = ['Year', check, 'Refinery Capacity']
        fig2 = px.bar(ddf, x="Year", y="Refinery Capacity",barmode='stack',
                 color=check,
                 text='Refinery Capacity')
        fig2.update_layout( xaxis=dict(tickvals=ddf['Year'],tickangle = -45),)

    else:
        check = "Sector"
        fig2 = px.bar(ddf3, x="Year", y="Refinery Capacity",barmode='stack',
                 color=check,
                 text='Refinery Capacity')
        fig2.update_layout( xaxis=dict(
            tickvals=ddf3['Year'],
            tickangle = -45
            ),)



    # fig2.add_trace(go.Scatter(x=df2.Sector, y=total, text=total,
    #                     mode='lines', name = 'Total', line = dict(color='firebrick', width=4, dash='dot')))


    fig2.update_traces( marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.8, texttemplate='%{text:.3s}')

    fig2.update_layout( # customize font and legend orientation & position
        uniformtext_minsize=11,
        title_text='Refinery Capacity Addition Over Years',
        font_family="Rockwell",
        paper_bgcolor = "#f9f9f9",
        autosize=True,
        margin=go.layout.Margin(l=0, r=0, t=30, b=10),
        legend =  dict(
        title = 'Sector',
           xanchor="center",
           yanchor = "top",
           y=-0.1,
           x=0.1,
           orientation = "h"
           ),

        yaxis = dict(
        title = 'Refinery Capacity(MMTPA)'
        )
            )

    return fig, graph, fig2,  totalnumber, totalcapacity

@app.callback(dash.dependencies.Output('plant_summary', 'children'),
              [dash.dependencies.Input('map1', 'clickData')])
def update_summary(click_Data):
    plant_name  = click_Data['points'][0]['hovertext']
    owner = df[df['Name'] == plant_name]['Owner'].iloc[0]
    commissioning_year = df[df['Name'] == plant_name]['Year of Commissioning'].iloc[0]
    capacity_mw = df[df['Name'] == plant_name]['barrels per day'].iloc[0]
    year_capacity = df[df['Name'] == plant_name]['Refining Capacity (2019-2020) (MMTPA)'].iloc[0]
    # source = df[df['name'] == plant_name]['source'].iloc[0]
    # url = df[df['name'] == plant_name]['url'].iloc[0]


    update = f'''
                    **Summary of *{plant_name}*:**
                    - Plant owner: {owner}
                    - Year of Commissioning: {commissioning_year}
                    - Barrels per day: {capacity_mw}
                    - Year of Reported Capacity(MMT): {year_capacity}

                    '''


    return update



if __name__ == '__main__':
    app.run_server(debug=True)
