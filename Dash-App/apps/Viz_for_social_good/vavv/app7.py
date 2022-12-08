import pandas as pd
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from plotly import graph_objs as go
import pathlib

from app import app

# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[
#     {"name": "viewport", "content": "width=device-width, initial-scale=1"}
# ])
# app.config['suppress_callback_exceptions'] = True
# server = app.server

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../vavv/').resolve()
#
df = pd.read_excel(DATA_PATH.joinpath('Data/Piura-Region-of-Peru-Survey-Data-for-Viz_new.xlsx'), sheet_name='Data_using')
# print(df)
ed = pd.read_excel(DATA_PATH.joinpath('Data/Piura-Region-of-Peru-Survey-Data-for-Viz_new.xlsx'), sheet_name='extra_data')
lat = list(ed[ed.type == 'Lat.'].value)
long = list(ed[ed.type == 'Long.'].value)
places = list(ed.place.unique())
population = list(ed[ed.type == 'Population'].value)
project_cost = list(ed[ed.type == 'Project Cost (USD)'].value)
table_data = pd.read_excel(DATA_PATH.joinpath('Data/Piura-Region-of-Peru-Survey-Data-for-Viz_new.xlsx'), sheet_name='ed2')





def generatecard(heading, title, description, rating, rating_description):
    return  dbc.Card(
        [
            dbc.CardHeader(heading),
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    html.P(description, className="card-text"),
                    html.H1(rating),
                    html.Strong(rating_description)
                ]
            ),
        ],className="card")

def generatecard2(title, description, rating_description, pop_num):
    return  dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Button(
                    title, id="popover-target-"+str(pop_num), color="info", className="btn-block h-50   "
                    ),
                    dbc.Popover(
                    [
                        dbc.PopoverHeader("Description"),
                        dbc.PopoverBody(description),
                    ],
                    id="popover-"+str(pop_num),
                    is_open=False,
                    target="popover-target-"+str(pop_num),
                    ),
                    html.H1(rating_description)
                ]
            ),
        ],className="card2_vavv")

def make_item(df, i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        f"{i}",
                        color="link",
                        id=f"group-{i}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                html.Div([
                    generatecard(row[1], row[2], row[3], row[5], row[4]) for index, row in df.iterrows()
                ], className = 'cards-group_vavv'),
                id=f"collapse-{i}",
            ),
        ]
    )


model = html.Div([
        dbc.Button("More Info", id="open-xl", color = 'info'),
        dbc.Modal(
            [
                dbc.ModalHeader(["Toggle Different Criteria for more information!"]),
                dbc.ModalBody(html.Div(id = 'collapse', className="accordion")),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-xl", className="ml-auto")
                ),
            ],
            id="modal-xl",
            size="xl",

        ),
    ], className = "m-2  d-flex justify-content-center")
layout3 =html.Div([
        dbc.Row([
            dbc.Col([
                html.H3(['OUR MISSION'], className= 'heading_name'),
                html.P('By tapping into the physical and spiritual nature of water, we empower people and communities in developing countries to generate clean water and sanitation solutions that bring "True Water True Life."'),

            ],sm=12, md=6, className = "d-flex flex-wrap align-content-center fadeInLeft"),
            dbc.Col([
                dbc.Card(
                [
                    dbc.CardImg(src="../assets/vavv/Pictures/mission.PNG", top=True)#, style = {"height": "200px", 'width': "400px"}),
                ])
            ],sm=12, md=6,className = "pt-4")

        ],className = 'mini_container_vavv'),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                [
                    dbc.CardImg(src="../assets/vavv/Pictures/monte_carlo.JPG", top=True,)# style = {"height": "300px", 'width': "300px"}),
                ])
            ],sm=12, md=4,className = "pt-4"),
            dbc.Col([
                html.Div(["Clean Water Project"], className= 'heading_name d-flex justify-content-center'),
                html.Div([
                    html.Div([
                        html.Div(["Monte Castillo"], className = 'card-heading-vavv'),
                        html.Div(['Community Name'], className = "card-detail-vavv")
                    ],className = "info_group_mem_vavv"),
                    html.Div([
                        html.Div(["Piura"], className = 'card-heading-vavv'),
                        html.Div(['Region'], className = "card-detail-vavv")
                    ],className = "info_group_mem_vavv"),
                    html.Div([
                        html.Div(["7000+"], className = 'card-heading-vavv'),
                        html.Div(['People Benefit'], className = "card-detail-vavv")
                    ],className = "info_group_mem_vavv"),
                    html.Div([
                        html.Div(["Canal Water"], className = 'card-heading-vavv'),
                        html.Div(['Primary Water Source'], className = "card-detail-vavv")
                    ],className = "info_group_mem_vavv"),
                    html.Div([
                        html.Div([
                            "MAY 2015 - AUG 2019",
                            dbc.Button("i", id="open_info",color="info", className="btn_vavv"  ),
                            dbc.Modal([
                                    dbc.ModalBody([
                                        dbc.Card([
                                            dbc.CardImg(src="../assets/vavv/Pictures/time_line.jpg", top=True, ),
                                        ])
                                        ]),
                                ], id="modal_info",size="xl",centered=True),
                        ], className = 'card-heading-vavv'),
                        html.Div(['Project Timeline'], className = "card-detail-vavv")
                    ],className = "info_group_mem_vavv"),
                    html.Div([
                        html.Div([
                        "Water Treatment Facility",
                        dbc.Button("i", id="open_info_2",color="info", className = "btn_vavv"),
                        dbc.Modal([
                                dbc.ModalBody([
                                    dbc.Card([
                                        dbc.CardImg(src="../assets/vavv/Pictures/water_treatment_facility.png", top=True, ),
                                    ])
                                ]),
                            ], id="modal_info_2",size="xl",centered=True),
                        ], className = 'card-heading-vavv'),
                        html.Div(['Solution'], className = "card-detail-vavv")
                    ], className = "info_group_mem_vavv"),
                ], className = 'info_group_vavv')
            ],sm=12, md=8,className = "d-flex justify-content-center flex-column fadeInLeft")
        ],className = 'mini_container_vavv'),
        dbc.Row([
            dbc.Col([
                html.P(['The ',html.Strong('Water Crisis'),' is the ', html.Strong( '#1 global risk '), 'based on impact to society.'])
            ],sm=12, md=3, className = 'card_vavv'),
            dbc.Col([
                html.P([html.Strong('785 million people '),'in the world do not have access to safe water (1/10th of the world’s population).'])
            ],sm=12, md=3, className = 'card_vavv'),

            dbc.Col([
                html.P(["By 2025, an ", html.Strong('estimated 1.8 billion people '),  "will live in areas plagued by water scarcity, with two-thirds of the world's population living in water-stressed regions."])
            ],sm=12, md=3, className = 'card_vavv'),
        ], className = 'd-flex justify-content-around fadeInLeft'),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=dcc.Graph(id='globe-1-vavv',animate=True,config={'editable': True, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','sendDataToCloud','ditInChartStudio','zoom2d','select2d','drawclosedpath', 'eraseshape','zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d','toggleSpikelines']})
                )
            ],sm=12, md=6),
            dbc.Col([
                    html.H4(
                        "Percentage of People live in a rural area who don't have access to safely managed water services"
                    ),
                    html.Ul([
                        html.Li([html.Strong('47%'),'  of the World']),
                        html.Li([html.Strong('58%'),' of the Latin America and The Caribbean']),
                        html.Li([html.Strong('80%'),' of the Peru'])
                    ]),
            ],sm=12, md=6, className = 'description_vavv fadeInLeft')
        ],className = 'mini_container_vavv'),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-2",
                    type="default",
                    children=dcc.Graph(id='globe-4-vavv',config={'editable': True, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','sendDataToCloud','ditInChartStudio','zoom2d','select2d','drawclosedpath', 'eraseshape','zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d','toggleSpikelines']})
                )
            ],sm=12, md = 12),
            dbc.Col([
                html.Strong('PERU WATER CRISIS'),

                html.Ul([

                    html.Li(['Only ', html.Strong("75%"),' of rural communities have basic (simple but unmanaged) drinking water services or better ']),
                    html.Li(['Only ', html.Strong("56%"),' of rural communities have basic sanitation facilities ']),
                    html.Li([html.Strong("12%"),' of children under theage of 5 experience chronic diarrhea due to waterborne diseases ']),

                ]),
            ],sm=12, md=12, className = 'description_vavv2 fadeInLeft')
        ],className = 'mini_container_vavv'),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-3",
                    type="default",
                    children=dcc.Graph(id='globe-3-vavv',config={'editable': True, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','sendDataToCloud','ditInChartStudio','zoom2d','select2d','drawclosedpath', 'eraseshape','zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d','toggleSpikelines']})
                )
            ],sm=12, md=6),
            dbc.Col([
                html.Strong('Piura Region'),
                html.Ul([
                    html.Li([html.Strong('84%'),' of people have basic drinking water.']),
                    html.Li([html.Strong('7.4%'),' depends surface water']),
                    html.Li([html.Strong('5.4%'),' depends on Unimproved']),
                    html.Li([html.Strong('2.8%'),' depends Limited-Service.']),
                ]),
            ],sm=12, md=6, className = 'description_vavv')
        ],className = 'mini_container_vavv'),
        html.Div(id = 'gogo'),
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    html.P(['VAVV has partnered with the Piura Regional Government of Peru to establish connections, build relationships, & collect preliminary data to evaluate ', html.Strong( 'Seven (7) New Communities'), '. VAVV will use it’s Scorecard Tool to evaluate & prioritize the communities we will serve next based on objective metrics.'])
                ],sm=12, md=10),
                dbc.Col([
                    dbc.Button(
                        "Our WorkPlan",
                        id="link-centered",
                        className="ml-auto",
                        target = 'blank',
                        color = 'primary',
                        href='https://veraaquaveravita.org/s/Project-Process-Flow-Chart.pdf'
                    )
                ],sm=6, md=2, className = ""),
            ], className = "d-flex align-self-center m-2 p-2"),
            dbc.Col([
                dcc.Loading(
                    id="loading-4",
                    type="default",
                    children=dcc.Graph(id='map1_vavv',clickData={'points': [{'hovertext': 'Carrizalillo'}]},config={'editable': True, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d','toImage','sendDataToCloud','ditInChartStudio','zoom2d','zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d','toggleSpikelines']})
                )
            ],sm=12, md=6, lg=6, className = "border-primary"),
            dbc.Col([
                html.Table(id = "table-vavv", className = "table-borderless")
            ],sm=12, md=6, lg=6,className = "d-flex align-self-center justify-content-center")
        ], className = 'mini_container_vavv'),
        dbc.Row(
            id = 'card-collection-vavv', className = 'd-flex justify-content-around flex-wrap align-content-around m-3'
        ),
        model,
        html.Div(id = 'chain-vavv'),
        html.Div(id = 'chain-vavav'),
        # html.Div(id='intermediate-value')
], className = "layout3-vavv ")

vavv_layout = html.Div(
    [
            html.Div([
                html.Div([
                    html.A([
                        html.Img(src='../assets/vavv/Logos/VAVV-wg-color-vert.png', className="image_vavv")
                    ],className = 'logo-image_vavv'),
                    html.Strong('TOGETHER WE CAN GIVE TRUE WATER TRUE LIFE!', className="logo_text_vavv")
                ], className = 'logo'),
                html.Div(id = 'google_translate_element'),
            ], className = "navbar_vavv"),

        layout3,
        html.Div(id="content"),


        # footer
        dbc.Row([
                html.Div([
                    html.Strong(['Give True Water True Life'], style = {'color': 'white'}),
                    html.P('For every $50 you give one person gets access to clean water for generations to come!'),
                    dbc.Button(
                        "DONATE",
                        id="link-centered2",
                        className="",
                        target = 'blank',
                        color = 'info',
                        href='https://veraaquaveravita.org/donate'
                    )
                ]),
                html.Div([
                    html.P("Developed By"),
                    html.Div([
                        html.A(
                        html.H1([
                            html.Span("A"), "bhinav ",html.Span('K'), "umar"
                        ]), href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                    ])
                ], className ='my_desc_vavv d-flex justify-content-center' )
        ], className = 'footer_vavv d-flex justify-content-around')
    ], className = 'body_vavv')


############################################################################

#############
def toggle_modal_wo_close(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output("modal_info", "is_open"),
    [Input("open_info", "n_clicks")],
    [State("modal_info", "is_open")],
)(toggle_modal_wo_close)

app.callback(
    Output("modal_info_2", "is_open"),
    [Input("open_info_2", "n_clicks")],
    [State("modal_info_2", "is_open")],
)(toggle_modal_wo_close)


@app.callback(
    Output("card-collection-vavv", "children"),
    [Input('map1_vavv', 'clickData')],
)
def populate_card(cdata):
    place = cdata['points'][0]['hovertext']
    # print(place, df.Location.unique())
    vv = df[df.Location == place]
    variable = ['Number of Days a Week that Water Demand is Met', 'Percentage from primary source',
                'Water related illnesses', 'Water related deaths',]
                # 'Current Cost of Water and/or Wastewater Services',
                # 'Observable water/wastewater environmental health risks','Level of proper sanitation and water supply at healthcare facility(ies) if any']
    code = []
    for j,i in enumerate(variable):
        # print(vv.loc[vv.Metric == i])
        rating_des = list(vv.loc[vv.Metric == i, 'Rating Description'])[0]
        metrics_des = list(vv.loc[vv.Metric == i, 'Metric Description'])[0]
        code.append(generatecard2(i, metrics_des, rating_des, j))
    return code

@app.callback(
    [Output("popover-"+str(i), "is_open") for i in range(4)],
    [Input("popover-target-"+str(i), "n_clicks") for i in range(4)],
    [State("popover-"+str(i), "is_open") for i in range(4)],
)
def toggle_popover(n0, n1, n2, n3, is_open0, is_open1, is_open2, is_open3):
    # print(n0, n1, n2, n3, is_open0, is_open1, is_open2, is_open3)
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False, False,False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        # print(ctx.triggered, button_id)
    if button_id == "popover-target-0":
        return not is_open0, is_open1, is_open2, is_open3
    elif button_id == "popover-target-1":
        return  is_open0, not is_open1, is_open2, is_open3
    elif button_id == "popover-target-2":
        return  is_open0,  is_open1, not is_open2, is_open3
    elif button_id == "popover-target-3":
        return  is_open0,  is_open1, is_open2, not is_open3
    return  is_open0, is_open1, is_open2, is_open3

def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
app.callback(
    Output("modal-xl", "is_open"),
    [Input("open-xl", "n_clicks"), Input("close-xl", "n_clicks")],
    [State("modal-xl", "is_open")],
)(toggle_modal)

#

@app.callback([
        Output('collapse', 'children'),
        ],
        [Input('map1_vavv', 'clickData')],
)
def getit(cdata):
    place = cdata['points'][0]['hovertext']
    dff = df[df.Location == place]
    dd = dff.groupby(['Criteria','Sub_Criteria', 'Metric','Metric Description', 'Rating Description']).agg({'Rating': 'max'}).reset_index()
    criteria = dd.Criteria.unique()
    code = []
    for i in criteria:
        code.append(make_item(dd[dd.Criteria == i], i))
    return [code]

#
@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in df.Criteria.unique()],
    [Input(f"group-{i}-toggle", "n_clicks") for i in df.Criteria.unique()],
    [State(f"collapse-{i}", "is_open") for i in df.Criteria.unique()],
)
def toggle_accordion(n1, n2, n3,n4, n5, n6, n7, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7):
    ctx = dash.callback_context
    click_check = [n1, n2, n3, n4, n5, n6, n7]
    only_false=[False, False, False,False, False, False, False]
    is_open = [is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7]
    if not ctx.triggered:
        return False, False, False,False, False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # print("\n", is_open, '\n', click_check)
    for i, j in enumerate(df.Criteria.unique()):
        if button_id == f"group-{j}-toggle" and click_check[i]:
            only_false[i] = not is_open[i]
            # print("\n", is_open , "\n", only_false)
            return only_false

    return False, False, False,False, False, False, False

@app.callback([

    Output('table-vavv', 'children')],
    [Input('map1_vavv', 'clickData')]
)
def populate_table_vavv(cdata):
    # print(cdata)
    location  = cdata['points'][0]['hovertext']
    # location = 'Carrizalillo'
    vv = table_data[table_data.place == location]
    community = list(vv.loc[vv.type == 'Community Name', 'value'])[0]
    # has_toilet = list(vv.loc[vv.type == 'Has Toliets or Latrines (Y/N)', 'value'])[0]
    # operational = list(vv.loc[vv.type == 'Operational Healthcare Facility (Y/N)', 'value'])[0]
    primary_source = list(vv.loc[vv.type == 'Primary Water Source', 'value'])[0]
    proposed_sol = list(vv.loc[vv.type == 'Proposed Solution', 'value'])[0]
    Project_Status = list(vv.loc[vv.type == 'Project Status', 'value'])[0]
    Project_Cost = list(vv.loc[vv.type == 'Project Cost (USD)', 'value'])[0]
    table_header = [
    html.Thead(html.Tr([html.Th("Community"), html.Th(community)]))
    ]

    row1 = html.Tr([html.Td("Primary Source of Water"), html.Td(primary_source)])
    row2 = html.Tr([html.Td("Proposed Solution"), html.Td(proposed_sol)])
    row3 = html.Tr([html.Td("Project Status"), html.Td(Project_Status)])
    row4 = html.Tr([html.Td("Project Cost in USD"), html.Td("$ " + str(Project_Cost))])

    table_body = [html.Tbody([row1, row2, row3, row4])]

    table = dbc.Table(table_header + table_body, bordered=True)
    return [table]

@app.callback([
    Output('map1_vavv', 'figure')],
    [Input('chain-vavv', 'children')]
)
def populate_vavv(n):

    fig = px.scatter_mapbox(lat=lat, lon=long,
                            hover_name=places,
                            hover_data={'Population':population, 'Budget (in $) ': project_cost},
                            zoom=9,
                            size=population,
                            opacity = 0.6,
                            mapbox_style='carto-positron',
                            color=project_cost,
                            color_continuous_scale='Sunset',

    #                         labels = {'primary_fuel': 'Primary fuel'},
                            # width = 700,
                            height = 300,
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
    fig.update_coloraxes(colorbar = dict(
                            thickness = 10,
                            len = 1,
                            x = 0.01,
                            ypad = 10,
                            ),
                        colorbar_tickfont=dict(
                            size = 15,
                            color = '#000',
                            family = "Open Sans"),
                        colorbar_title=dict(
                            text = "Budget"),
                        colorbar_title_font=dict(
                            family = "Open Sans",
                            size = 20,
                            color = '#000'))


    return [fig]




@app.callback([
    Output('globe-1-vavv', 'figure'),
    # Output('globe-2-vavv', 'figure'),
    Output('globe-3-vavv', 'figure'),
    Output('globe-4-vavv', 'figure'),],
    [Input('gogo', 'children'),
    # Input('one3', 'children),
    Input('google_translate_element', 'children')
    ],
    # [State('one3', 'children')]
)
def populate_globe_vavv(n,nclick):
    print(nclick)
    df = pd.read_csv(DATA_PATH.joinpath("Data/water world rural.csv"))
    # print(df)
    df2 = pd.read_csv(DATA_PATH.joinpath("Data/water latin rural.csv"))
    df3 = pd.read_csv(DATA_PATH.joinpath("Data/water peru rural.csv"))
    fd = pd.concat([df, df2, df3], ignore_index= True)
    fd.loc[fd.Region == "PER", 'Region'] = 'Peru'
    fig1 = px.bar(fd, x="Region", y="Coverage", color="Service Level", barmode="stack",
    color_discrete_map={
                    'Safely managed service': '#1C4E80',
                    'Basic service':'#0091D5',
                     'Surface water':"#A5D8DD",
                     'Unimproved':"#EA6A47",
                    'Limited service'        :'#7E909A'
                },
    category_orders={"Service Level": ['Safely managed service', 'Basic service', 'Surface water','Unimproved', 'Limited service']})
    # fig1.update_traces(texttemplate='%{text:.2f}', textposition='auto')
    fig1.update_layout(
        title = dict(
            text = "Rural Area's Drinking Water Service Level",
            font = dict(
                family = "PT Sans Narrow",
                size = 20,
                color = '#202020'),
            x = 0.5
        ),
        legend = dict(
            bgcolor = "rgba(256,256,256, 0.9)",  borderwidth = 0.1,  font = dict( family = "PT Sans Narrow",  size = 15,  color = '#202020'),
            orientation = 'h', xanchor = 'left',  yanchor = "bottom", x = -0.1, y = -0.5, title = dict( text = "Service Level", font = dict(
            family = "PT Sans Narrow", size = 20, color = '#202020'), side = 'left' )),
        margin={'l': 60, 'b': 60, 't': 80, 'r': 10},
        margin_autoexpand = True,
        autosize = True,
        paper_bgcolor = 'rgba(256,256,256, 0.9)',
        plot_bgcolor = 'rgba(256,256,256, 0.9)',
        hoverlabel = dict(
            bgcolor = '#fff',
            bordercolor = '#202020'
        ),
        barmode = 'stack',
        bargap = 0.2,
    )
    fig1.update_yaxes(
        color = '#202020',
        title = "Percentage",
        # type = "category",
        showdividers = False,
        showgrid = False,
        zeroline = False,
    )

    fig1.update_xaxes(
        color = '#202020',
        title = "",
        showgrid = False,
        zeroline = False,
        tick0 = 0,
        dtick = 1,
    ),
    # df = pd.read_csv("Data/water peura2.csv")
    # fig2 = px.bar(df, x="Region", y="Coverage", color="Service Level", barmode="stack",)

    df = pd.read_csv(DATA_PATH.joinpath('Data/time series for piura.csv'))
    df = df[df['Service Type'] == "Drinking water"]
    fig3 = px.area(df, x="Year", y="Coverage", color="Service Level",line_group="Region",
    color_discrete_map={

                    'At least basic':'#0091D5',
                     'Surface water':"#A5D8DD",
                     'Unimproved':"#EA6A47",
                    'Limited service'        :'#7E909A'
                },
    category_orders={"Service Level": ['At least basic', 'Surface water', 'Unimproved','Limited service',]})
    fig3.update_layout(
        title = dict(
            text = "Water Services in Piura Region",
            font = dict(
                family = "PT Sans Narrow",
                size = 20,
                color = '#202020'),
            x = 0.5
        ),
        legend = dict(
            bgcolor = "rgba(256,256,256, 0.9)",  borderwidth = 0.1,  font = dict( family = "PT Sans Narrow",  size = 15,  color = '#202020'),
            orientation = 'h', xanchor = 'left',  yanchor = "bottom", x = 0, y = -0.5, title = dict( text = "", font = dict(
            family = "PT Sans Narrow", size = 20, color = '#202020'), side = 'left' )),
        margin={'l': 60, 'b': 60, 't': 80, 'r': 10},
        margin_autoexpand = True,
        autosize = True,
        paper_bgcolor = 'rgba(256,256,256, 0.9)',
        plot_bgcolor = 'rgba(256,256,256, 0.9)',
        hoverlabel = dict(
            bgcolor = '#fff',
            bordercolor = '#202020'
        ),
        barmode = 'stack',
        bargap = 0.2,
    )
    fig3.update_yaxes(
        color = '#202020',
        # title = "",
        # type = "category",
        showdividers = False,
        showgrid = False,
    )

        # fig3.update_xaxes(
        #     color = '#202020',
        #     title = "",
        #     nticks = 5,
        #     dtick = "Y3",
        #     showgrid = False,
        #     zeroline = False,
        #     tick0 = 0,
        # ),


    df = pd.read_csv(DATA_PATH.joinpath('Data/peru all region.csv'))
    fig4 = px.bar(df, x="Region", y="Coverage", color="Service Level", barmode="stack",
    color_discrete_map={

                    'At least basic':'#0091D5',
                     'Surface water':"#A5D8DD",
                     'Unimproved':"#EA6A47",
                    'Limited service'        :'#7E909A'
                },
    category_orders={"Service Level": ['At least basic', 'Surface water', 'Unimproved','Limited service',]})

    fig4.update_layout(
        title = dict(
            text = "Peru's Different Region Drinking Water Service Level",
            font = dict(
                family = "PT Sans Narrow",
                size = 20,
                color = '#202020'),
            x = 0.5
        ),
        legend = dict(
            bgcolor = "rgba(256,256,256, 0.9)",  borderwidth = 0.1,  font = dict( family = "PT Sans Narrow",  size = 15,  color = '#202020'),
            orientation = 'h', xanchor = 'left',  yanchor = "bottom", x = 0.1, y = -0.5, title = dict( text = "Service Level", font = dict(
            family = "PT Sans Narrow", size = 20, color = '#202020'), side = 'left' )),
        margin={'l': 60, 'b': 60, 't': 80, 'r': 10},
        margin_autoexpand = True,
        autosize = True,
        paper_bgcolor = 'rgba(256,256,256, 0.9)',
        plot_bgcolor = 'rgba(256,256,256, 0.9)',
        hoverlabel = dict(
            bgcolor = '#fff',
            bordercolor = '#202020'
        ),
        barmode = 'stack',
        bargap = 0.2,
    )
    fig4.update_yaxes(
        color = '#202020',
        # title = "",
        # type = "category",
        showdividers = False,
        showgrid = False,
    )

    fig4.update_xaxes(
        categoryorder='array',
        categoryarray= list(df[df['Service Level'] == 'At least basic'].sort_values('Coverage').Region),
        color = '#202020',
        title = "",
        showgrid = False,
        zeroline = False,
        tick0 = 0,
        dtick = 1
    ),
    return fig1, fig3, fig4



if __name__ == '__main__':
    app.run_server(debug=True)
