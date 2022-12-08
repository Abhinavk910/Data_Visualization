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
DATA_PATH = PATH.joinpath('../Week_16_avg_sales/').resolve()

df = pd.read_csv(DATA_PATH.joinpath('required.csv'))

week_16_wiz = dbc.Container([
    dbc.Row([
        html.P('hi', id = 'text', hidden = True),
        html.H1('WorkOut Wednesday - Week 16'),
        html.H5(' Sub-Category Average Sales by Category'),
        dcc.Loading(
            id="loading-1-week_16_wiz",
            type="default",
            children=dcc.Graph(id='line-chart-week_16_wiz',config={'displayModeBar': False},
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
    Output('line-chart-week_16_wiz','figure'),
    Input('text', 'children')
)
def generate_week16wiz(text):
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(
            go.Bar(y=[[row["Category"]], [row["Sub-Category"]]],
                   x=[row["Sales"]], orientation = 'h',
    #                name=row["Sub-Category"],
                   showlegend=False,
                   marker_color=row["color"],
                   hovertemplate =
                        '&nbsp;<br>&nbsp;&nbsp;<b>%{y}</b>'+
                        f'<br>&nbsp;&nbsp;{int(row["Sales"]):,d}<br><br>'+
                        f'&nbsp;&nbsp;&#9650;<b>{abs(row["per_cha"])}% {["below" if row["per_cha"] < 0 else "above"][0]} the average category sale of {int(row["0"]):,d}</b>&nbsp;<extra></extra><br>&nbsp;',
    #                text = [abs(row['per_cha'])]
    #                text = [row['per_cha']]
    #                textposition='outside',
    #         texttemplate='%{text}%',
    #         textfont_size=11,

    #                legendgroup=row["type"] # Fix legend
                   )),

        fig.add_annotation(
            text=str(abs(row['per_cha']))+ "%",
            y = [row["Category"], row["Sub-Category"]],
            x = row["Sales"]+21000,
            showarrow=False,
        )
    #     fig.add_hline(y=[10], line_width=3, line_dash="dash", line_color="green")
        if row['per_cha'] < 0:
            fig.add_trace(go.Scatter(mode = 'markers',y=[[row["Category"]], [row["Sub-Category"]]],
                   x=[row["Sales"]+5000], marker_symbol = 6, marker_line_color="black", marker_color="black",
                               marker_line_width=0, marker_size=11 , showlegend=False,
                                    hovertemplate =
                        '&nbsp;<br>&nbsp;&nbsp;<b>%{y}</b>'+
                        f'<br>&nbsp;&nbsp;{int(row["Sales"]):,d}<br><br>'+
                        f'&nbsp;&nbsp;<b>&#9660;{abs(row["per_cha"])}% {["below" if row["per_cha"] < 0 else "above"][0]} the average category sale of {int(row["0"]):,d}</b>&nbsp;<extra></extra><br>&nbsp;',))
            fig.add_trace(go.Scatter(mode = 'markers',y=[[row["Category"]], [row["Sub-Category"]]],
                   x=[row["0"]], marker_symbol = 42, marker_line_color="#B9AFAB", marker_color="black",
                    hovertemplate =
                        '&nbsp;<br>&nbsp;&nbsp;<b>%{y}</b>'+
                        f'<br>&nbsp;&nbsp;{int(row["Sales"]):,d}<br><br>'+
                        f'&nbsp;&nbsp;<b>&#9660;{abs(row["per_cha"])}% below the average category sale of {int(row["0"]):,d}</b>&nbsp;<extra></extra><br>&nbsp;',
                               marker_line_width=1, marker_size=18 , showlegend=False ))
        else:
            fig.add_trace(go.Scatter(mode = 'markers',y=[[row["Category"]], [row["Sub-Category"]]],
                   x=[row["Sales"]+5000], marker_symbol = 5, marker_line_color="black", marker_color="black",
                               marker_line_width=0, marker_size=10, showlegend=False,
                                    hovertemplate =
                        '&nbsp;<br>&nbsp;&nbsp;<b>%{y}</b>'+
                        f'<br>&nbsp;&nbsp;{int(row["Sales"]):,d}<br><br>'+
                        f'&nbsp;&nbsp;<b>&#9650;{abs(row["per_cha"])}% {["below" if row["per_cha"] < 0 else "above"][0]} the average category sale of {int(row["0"]):,d}</b>&nbsp;<extra></extra><br>&nbsp;',)
                         )
            fig.add_trace(go.Scatter(mode = 'markers',y=[[row["Category"]], [row["Sub-Category"]]],
                   x=[row["0"]], marker_symbol = 42, marker_line_color="#B9AFAB", marker_color="black",
                    hovertemplate =
                        '&nbsp;<br>&nbsp;&nbsp;<b>%{y}</b>'+
                        f'<br>&nbsp;&nbsp;{int(row["Sales"]):,d}<br><br>'+
                        f'&nbsp;&nbsp;<b>&#9650;{abs(row["per_cha"])}% above the average category sale of {int(row["0"]):,d}</b>&nbsp;<extra></extra><br>&nbsp;',
                               marker_line_width=1, marker_size=18 , showlegend=False ))
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=10,
            font_family="Rockwell"
        ),
        plot_bgcolor='white',
        bargap=0.5,
        height = 700,
        width = 800,
        xaxis = dict(visible = False, fixedrange = True),
        yaxis = dict(position = 0,showdividers = True, fixedrange = True, side = 'left'),
        margin=dict(
            autoexpand=False,
            l=200,
            r=20,
            t=10,
            b=50,
        ),
#         title='<b>WorkOut Wednesday - Week 16',
#         font=dict(family='Arial',
#                   size=15,
#                   color='rgb(37,37,37)'),

    )




    return fig
