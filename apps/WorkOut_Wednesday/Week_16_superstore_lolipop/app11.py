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
DATA_PATH = PATH.joinpath('../Week_16_superstore_lolipop/').resolve()

df = pd.read_csv(DATA_PATH.joinpath('state_sales.csv'))

colors = ['#33A02C', '#B2DF8A', '#A6CEE3', '#1F78B4']
def getcolor(x):
    if x == 'West':
        return colors[3]
    elif x == 'East':
        return colors[1]
    elif x == 'Central':
        return colors[0]
    elif x == 'South':
        return colors[2]

week_16_wiz2 = dbc.Container([
    dbc.Row([
        html.P('hi', id = 'text', hidden = True),
        html.H1('Sales By State'),
        # html.H5(' Sub-Category Average Sales by Category'),
        html.Div(
            [
                dbc.Button("2017", id="button-week161",color="primary", disabled = False, className="mr-1"),
                dbc.Button("2018", id="button-week162", color="primary", disabled = False, className="mr-1"),
                dbc.Button("2019", id="button-week163",color="primary",disabled = False,className="mr-1" ),
                dbc.Button("2020", id="button-week164",color="primary",disabled = False,className="mr-1" ),
                html.Span(id="out-week16", hidden =False,children=[2017], style={"vertical-align": "middle"}),
            ]
        ),
        dcc.Loading(
            id="loading-1-week_16_wiz_powerbi",
            type="default",
            children=dcc.Graph(id='line-chart-week_16_wiz_powerbi',config={'displayModeBar': False},
                      figure={}, ),)

    ], className = 'm-2 align-content-center flex-column'),
    dbc.Row([
                html.Div([
                    html.P(['Data | Superstore']),
                    html.A(html.P('Challenge_by:@Lorna Brown'), href = "https://public.tableau.com/profile/lorna.eden#!/vizhome/WOW2021W16CanyouuseQuickLODstorecreatethisview/WOW2021W16",target ="_blank"),
                    html.A(html.P('Get Data'), href='https://data.world/missdataviz/superstore-2021', target = "_blank")
                ], className ='d-flex justify-content-around align-content-center flex-grow-1 p-1 flex-wrap' ,style = {}),
                html.Div([
                    html.P("Developed By: "),
                    html.Div([
                        html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                        href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                    ])
                ], className ='d-flex justify-content-center align-content-center flex-grow-1 p-1 mb-0 ' , style = {})
        ], className = ' d-flex justify-content-around align-content-center text-muted small', style = {'min-height': '30px'})

], fluid = 'True')


@app.callback(
    [Output("button-week161", 'disabled'),
    Output("button-week162", "disabled"),
    Output("button-week163", "disabled"),
    Output("button-week164", "disabled"),
    Output('out-week16', 'children')],
    [Input("button-week161", "n_clicks"),
     Input("button-week162", "n_clicks"),
    Input("button-week163", "n_clicks"),
    Input("button-week164", "n_clicks"),],
    [State('out-week16', 'children')]
)
def on_button_click(n1, n2, n3, n4, state):
    ctx = dash.callback_context
    print(ctx.triggered)
    if not ctx.triggered:
        return False, False, False,False, state
    else:
        print(ctx)
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "button-week161":
        return True, False, False, False, 2017
    if button_id == "button-week162":
        return False, True, False, False, 2018
    if button_id == "button-week163":
        return False, False, True, False, 2019
    if button_id == "button-week164":
        return False, False, False, True, 2020

@app.callback(
    Output('line-chart-week_16_wiz_powerbi','figure'),
    Input('out-week16', 'children')
)
def generateplotweek16(year):
    fig = go.Figure()
    dff = df[df.year == year]

    global region_list
    region_list = ['Central', 'East', 'West', 'South']


    def check_legend(x):
        global region_list
        if x in region_list:
            region_list.remove(x)
            return True
        else:
            return False


    for i, row in dff.iterrows():
        fig.add_trace(
            go.Bar(y=[row["State"]],
                   x=[row["Sales"]],
                   orientation='h',
                   legendgroup=row['Region'],
                   showlegend= check_legend(row['Region']),
                   name=row['Region'],
                   marker_color=getcolor(row['Region']),
                   marker_line_width=1.5,
                   marker_line_color=getcolor(row['Region']),
                   width=[0.05],

                   ))
        fig.add_trace(go.Scatter(mode='markers', y=[row["State"]],text=str(row['Sales']),
                                 textfont_size=10,
                                 textposition='middle right',
                                 x=[row["Sales"]], marker_symbol=0, marker_line_color=getcolor(row['Region']), marker_color=getcolor(row['Region']),
                                 marker_line_width=2, marker_size=10, name=row['Region'], showlegend=check_legend(row['Region']),
                                 legendgroup=row['Region'], ))
        fig.add_annotation(
                text=str(row['Sales']),
                y=row["State"],
                x=row["Sales"]+10500,
                showarrow=False,
                font_size = 10,

            )
    fig.update_layout(
        margin=dict(
                autoexpand=False,
                l=200,
                r=40,
                t=10,
                b=50,
            ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=10,
            font_family="Rockwell"
        ),
        plot_bgcolor='white',
        bargap=0.5,
        height=1000,
        width=800,
        xaxis=dict(visible=False),
        yaxis=dict(position=0.04, tickfont_size=12,
                   showdividers=True, side='left'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.98,
            xanchor="center",
            x=0.5,
            #             traceorder="reversed",
            #             title_font_family="Times New Roman",
            title='Region',
            title_font_size=15,
            font=dict(
                    family="Courier",
                    size=12,
                    color="black"
            ),
            #             bgcolor="LightSteelBlue",
            #             bordercolor="Black",
            #             borderwidth=2
        )
    )
    return fig
