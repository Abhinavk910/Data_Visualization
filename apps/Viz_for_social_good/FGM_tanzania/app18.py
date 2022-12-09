import dash_html_components as html
from dash import Dash
import dash
from dash_extensions import BeforeAfter
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from app import app

vfsg_tanzania = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Img(src = "../assets/fgm_tanzania/mapsmall.png", style = {"max-width": "150px"}),
                        ], className = ''),
                    html.Div([
                         html.H4(html.A("CROWD2MAP TANZANIA", href = "https://crowd2map.org/", target = "_blank"), className="card-title"),
                         html.P("Putting rural Tanzania on the map for 5 years", className="card-text"),
                         html.P('Crowd2Map Tanzania is an entirely volunteer crowdsourced mapping project putting rural Tanzania on the map. Since 2015, we have been adding schools, hospitals, roads, buildings and villages to OpenStreetMap with the help of volunteers worldwide and on the ground in Tanzania.',
                         style = {'font-size': "13px"}),
                    ], className = 'flex-grow-1 p-2 ')
                ], className = 'd-flex flex-md-wrap card_tanzania flex-lg-nowrap m-1'),
                dbc.Row([
                    dbc.Col([
                        html.P(['More than ',html.Strong('3 million'),' girls in the world are estimated to be at risk for FGM annually.'])
                    ],sm=12, md=4, className = 'card_tanzania p-2'),
                    dbc.Col([
                        html.P(['More than ',html.Strong('200 million '),'girls and women alive today have been subjected to the practice.'])
                    ],sm=12, md=4, className = 'card_tanzania p-2'),
                    dbc.Col([
                        html.P(["In Tanzania, approx. ",html.Strong("30% – 60% "),'of girls and women aged 15 to 49 still go through FGM.'])
                    ],sm=12, md=4, className = 'card_tanzania p-2'),
                    dbc.Col([
                        html.P([html.Strong("3000"),' girls prevented from undergoing FGM by this project'])
                    ],sm=12, md=4, className = 'card_tanzania p-2'),
                ], className = 'd-flex justify-content-around fadeInLeft'),
                dbc.Row([
                    dbc.Col([
                        html.P("Having better maps is vital in the fight against Female Genital Mutilation (FGM) and to help community development. We support many grassroots organisations in rural Tanzania, such as Hope for Girls and Women Tanzania, to use maps and data collection to make themselves more effective.",
                        style = {'font-size': "13px", 'text-align': 'justify', 'text-justify': 'inter-word'})
                    ],sm=12,md = 12,className = 'card_tanzania p-2'),
                ],className = "m-1", style = {}),
            ], md = 5, className = "m-0 d-flex flex-column align-items-center", style = {"background":''}),

            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Volunteers", style = {'color':"#DFB221",'min-height':'100px', 'background':'rgba(256,256,256, 0.9)', 'font-size':'25px'}),
                            dbc.CardBody([
                                html.P("16,382", className="card-text strong_card"  ),
                            ]),
                        ],outline = 'white',className = 'card_tanzania2', style={"min-height": "100%"},)
                    ],sm=12,md=6,lg=3, className = 'mb-2 ',style = {'background' : '', 'min-height' : "100px"}),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Area (sq. km)",style = {'color':"#DFB221",'min-height':'100px', 'background':'rgba(256,256,256, 0.9)', 'font-size':'25px'}),
                            dbc.CardBody([
                                html.P("120,358", className="card-text strong_card"),
                            ]),
                        ], className = 'card_tanzania2',style={"min-height": "100%"},)
                    ],sm=12,md=6,lg=3,className = 'mb-2',style = {'background' : ''}),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Length of roads (m)",style = {'color':"#DFB221", 'min-height':'100px','background':'rgba(256,256,256, 0.9)', 'font-size':'25px'}),
                            dbc.CardBody([
                                html.P("1,338,926", className="card-text strong_card"),
                            ]),
                        ], className = 'card_tanzania2',style={"min-height": "100%"},)
                    ],sm=12,md=6,lg=3,className = 'mb-2',style = {'background' : ''}),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Buildings",style = {'color':"#DFB221", 'min-height':'100px','background':'rgba(256,256,256, 0.9)', 'font-size':'25px'}),
                            dbc.CardBody([
                                html.P("5,202,390", className="card-text strong_card"),
                            ]),
                        ], className = 'card_tanzania2',style={"min-height": "100%"},)
                    ],sm=12,md=6,lg=3,className = 'mb-2',style = {'background' : ''}),

                ],className = 'd-flex flex-row m-1 p-1 flex-wrap', style = {'background' : '', 'width': "100%"} ),

                dbc.Row([
                    dbc.Col([
                        html.P('Slide the Image to See impact of Our initiative. Initial image showing the Total Count and after slide one is the count that has been added to OpenStreetMap.',
                               className = "p-1"),
                        BeforeAfter(before="../assets/fgm_tanzania/BEFORE2.png", after="../assets/fgm_tanzania/AFTER.png", width=750, height=350),
                    ],className="card_tanzania flex-column justify-content-center align-items-center", style = {'background':'', 'width': '750px'})
                ])

            ], md = 7, className = "p-2 d-flex flex-column align-items-center align-content-center" ,style = {}),
        # ], className = '' , style = {'background' : 'gray'}),
        ], className = "d-flex flex-row", style = {'background' : '#EBEEEE'}),
        dbc.Row([
                html.Div([
                    html.Strong(['Prevent FGM in Tanzania'], style = {'color': 'white'}),
                    html.P('$10 will provide 5 paper maps of a mapped area for schools and village offices'),
                    dbc.Button(
                        "DONATE",
                        id="link-centered2",
                        className="",
                        target = 'blank',
                        color = 'info',
                        href='https://www.globalgiving.org/projects/crowdsourced-mapping-to-prevent-fgm-in-tanzania/'
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
        ], className = 'footer_tanzania d-flex justify-content-around')

], style = {'overflow-x': 'hidden'}, className = 'body_tanzania')
