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
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../NFHS/').resolve()

df2  = pd.read_excel(DATA_PATH.joinpath('TRIMMED.xlsx'), sheet_name='TRIM STAGE 2')
tuples = [('S.No.', ''),
          ('Indicator_Code', ''),
          ('Indicators', ''),
          ('Sub Indictors', ''),
          ('NFHS-5', 'Urban'),
          ('NFHS-5', 'Rural'),
          ('NFHS-5', 'Total'),
          ('NFHS-4', 'Total'),
          ('State/UT', "")]

Final = pd.MultiIndex.from_tuples(tuples)
df2.columns = Final
df2.drop(0, inplace=True)


indicators = df2[('Indicators', '')].unique().tolist()
dictionary_sub = {}
for i in df2[('Indicators', '')].unique().tolist():
    dictionary_sub[i] = set(df2[df2[('Indicators', '')] == i]
                            [('Sub Indictors', '')].unique().tolist())

def shift(x, y):

    if isinstance(x, float):
        x = x
    else:
        x = max(x)
    return (x-y)*9/100

def get_graph(df2,code):
#     print(code)

    df_final = df2[df2[('Indicator_Code', '')] == code]
    df_final[('NFHS-5', 'Total')] = df_final[('NFHS-5', 'Total')].astype('float')
    df_final['State/UT'] = df_final['State/UT'].replace(['Dadra & Nagar Haveli and Daman & Diu', "Andaman & Nicobar Islands"], ['DNH & DD', 'AN Islands'])
    labels = df_final['State/UT'].tolist()
    # df_final.iloc[:, 7] = df2.iloc[:, 7].apply(lambda x: str(x).replace(',', "").replace("na", '0').replace("*", '0').replace('(', "").replace(')', "")).astype('float')

    fig = go.Figure()
    len_decimal = len(set(df_final.iloc[:,6].apply(lambda x: str(x).split('.')[-1]).tolist()))
    if len_decimal == 1:
        df_final.iloc[:,6] = df_final.iloc[:,6].apply(lambda x: int(x))

    if sum(df_final[('NFHS-4', 'Total')] == 'na') >30:
        df_final = df_final.sort_values(('NFHS-5', 'Total'), ascending=True)
        india_data = df_final[df_final[('State/UT', "")] == 'India']
        df_final.drop(index = df_final[df_final[('State/UT', "")] == 'India'].index, inplace=True)
        df_final = pd.concat([df_final, india_data])
        labels = df_final['State/UT'].tolist()
        x_data = df_final.iloc[:, -3].to_numpy()

        for i in range(0, df_final.shape[0]):
            fig.add_trace(go.Scatter(
                x=[x_data[i]],
                y=[i+1],
                mode='markers',
                marker=dict(color=['rgb(137, 123, 211)'], size=10)
            ))
        annotations = [] 
        for i in range(0, df_final.shape[0]):

            annotations.append(dict(
                    text=str((x_data[i])),
                    y = i+1,
                    x = x_data[i]+shift(x_data[-2], x_data[0]),
                    showarrow=False,
                    font_size=10
                ))
        annotations.append(dict(
                    x=x_data[-1], y = df_final.shape[0], xref="x", yref = 'y', text='NFHS-5<br>(2019-20)', showarrow=True,
                    font=dict(family="Courier New, monospace", size=12, color="rgb(137, 123, 211)"),
                    align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="rgb(137, 123, 211)",
                    ax=-30, ay=-35, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))  

        annotations.append(dict(
                    x=1, y =1.075, xref="paper", yref="paper", text='NFHS-4(2015-16) data not available ', showarrow=False,
                    font=dict(family="Courier New, monospace", size=12, color="rgb(91, 171, 171)"),
                    align="center"))  


    else:
        df_final.iloc[:, 7] = df_final.iloc[:, 7].apply(lambda x: str(x).replace(',', "").replace("na", '0').replace("*", '0').replace('(', "").replace(')', "")).astype('float')
        df_final[('NFHS-4', 'Total')] = df_final[('NFHS-4', 'Total')].astype('float')
        len_decimal = len(set(df_final.iloc[:,7].apply(lambda x: str(x).split('.')[-1]).tolist()))
        if len_decimal == 1:
            df_final.iloc[:,7] = df_final.iloc[:,7].apply(lambda x: int(x))
        df_final = df_final.sort_values(('NFHS-5', 'Total'), ascending=True)
        india_data = df_final[df_final[('State/UT', "")] == 'India']
        df_final.drop(index = df_final[df_final[('State/UT', "")] == 'India'].index, inplace=True)
        df_final = pd.concat([df_final, india_data])
        labels = df_final['State/UT'].tolist()
        x_data = df_final.iloc[:, [-3,-2]].to_numpy()
        for i in range(0, df_final.shape[0]):
            if x_data[i][0] > x_data[i][1]:
                fig.add_trace(go.Scatter(x=x_data[i], y=[i+1, i+1], mode='lines',
                    name=labels[i],
                    line=dict(color='rgba(137, 123, 211, 0.5)', width=10),
                ))

                # endpoints
                fig.add_trace(go.Scatter(
                    x=[x_data[i][0], x_data[i][-1]],
                    y=[i+1, i+1],
                    mode='markers',
                    marker=dict(color=['rgb(137, 123, 211)','rgb(91, 171, 171)' ], size=10)
                ))
            else:
                fig.add_trace(go.Scatter(x=x_data[i], y=[i+1, i+1], mode='lines',
                    name=labels[i],
                    line=dict(color='rgba(91, 171, 171, 0.5)', width=10),
                ))

                # endpoints
                fig.add_trace(go.Scatter(
                    x=[x_data[i][0], x_data[i][-1]],
                    y=[i+1, i+1],
                    mode='markers',
                    marker=dict(color=['rgb(137, 123, 211)','rgb(91, 171, 171)' ], size=10)
                ))
                


        annotations = []


    #     print(x_data)
        # Source
        for i in range(0, df_final.shape[0]):
            if x_data[i][0] > x_data[i][-1]:

                annotations.append(dict(
                        text=str((x_data[i][0])),
                        y = i+1,
                        x = x_data[i][0]+shift(x_data[-2], x_data[0][-1]),
                        showarrow=False,
                        font_size=11
                    ))
                annotations.append(dict(
                        text=str((x_data[i][-1])),
                        y = i+1,
                        x = x_data[i][-1]-shift(x_data[-2],  x_data[0][-1]),
                        showarrow=False,
                    font_size=11
                    ))
            else:
                annotations.append(dict(
                        text=str((x_data[i][0])),
                        y = i+1,
                        x = x_data[i][0]-shift(x_data[-2],  x_data[0][-1]),
                        showarrow=False,
                    font_size=10
                    ))
                annotations.append(dict(
                        text=str((x_data[i][-1])),
                        y = i+1,
                        x = x_data[i][-1]+shift(x_data[-2],  x_data[0][-1]),
                        showarrow=False,
                    font_size=10
                    ))

        if x_data[-1][1] > x_data[-1][0]:

            annotations.append(dict(
                    x=x_data[-1][-1], y = df_final.shape[0], xref="x", yref = 'y', text='NFHS-4<br>(2015-16)', showarrow=True,
                    font=dict(family="sarif", size=15, color="rgb(91, 171, 171)"),
                    align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="rgb(91, 171, 171)",
                    ax=40, ay=-35, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))
            annotations.append(dict(
                    x=x_data[-1][0], y = df_final.shape[0], xref="x", yref = 'y', text='NFHS-5<br>(2019-20)', showarrow=True,
                    font=dict(family="sarif", size=15, color="rgb(137, 123, 211)"),
                    align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="rgb(137, 123, 211)",
                    ax=-40, ay=-35, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))
        else:
            annotations.append(dict(
                    x=x_data[-1][-1], y = df_final.shape[0], xref="x", yref = 'y', text='NFHS-4<br>(2015-16)', showarrow=True,
                    font=dict(family="sarif", size=15, color="rgb(91, 171, 171)"),
                    align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="rgb(91, 171, 171)",
                    ax=-40, ay=-35, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))
            annotations.append(dict(
                    x=x_data[-1][0], y = df_final.shape[0], xref="x", yref = 'y', text='NFHS-5<br>(2019-20)', showarrow=True,
                    font=dict(family="sarif", size=15, color="rgb(137, 123, 211)"),
                    align="center", arrowhead=0, arrowsize=0.3, arrowwidth=2, arrowcolor="rgb(137, 123, 211)",
                    ax=40, ay=-35, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))
            
            
        annotations.append(dict(
                        x=0.62, y = 1.0175, xref="paper", yref = 'paper', text='Increased', showarrow=True,
                        font=dict(family="sarif", size=16, color="rgb(137, 123, 211)"),
                        align="center", arrowhead=0, arrowsize=0.3, arrowwidth=10, arrowcolor="rgba(137, 123, 211, 0.5)",
                        axref="pixel", ayref = 'pixel',
                        ax=70, ay=0, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))
        annotations.append(dict(
                    x=0.82, y = 1.0175, xref="paper", yref = 'paper', text='Decreased', showarrow=True,
                    font=dict(family="sarif", size=16, color="rgb(91, 171, 171)"),
                    align="center", arrowhead=0, arrowsize=0.3, arrowwidth=10, arrowcolor="rgba(91, 171, 171, 0.5)",
                    axref="pixel", ayref = 'pixel',
                    ax=70, ay=0, bordercolor="#c7c7c7", borderwidth=0, borderpad=4))


    fig.update_layout(annotations=annotations)

    fig.update_traces(
       hoverinfo='skip'
    )
    fig.update_layout(
    #         title = df_final['Sub Indictors'].unique().tolist()[0],
        plot_bgcolor = 'white', paper_bgcolor = 'white',height=800, width=730,
        xaxis=dict(
        fixedrange = True,
            showline=False,
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            linecolor='rgb(204, 204, 204)',

        ),
        yaxis=dict(
        fixedrange = True,
            showgrid=True,
            zeroline=False,
            showline=True,
            linecolor="#EBEBEB",
            showticklabels=True,
            gridcolor="#EBEBEB",
            tickmode = 'array',
            ticktext=labels,
            tickvals = np.arange(1,38).tolist(),
        ),
        autosize=False,
        margin=dict(
            autoexpand=True,
            l=150,
            r=0,
            t=50,
        ),
        showlegend=False,
    )


    return fig






def make_button(i):
    return dbc.Button(
        f"{i}",
        color="link",
        id=f"group-{i.replace('.', '$$')}-toggle",
        n_clicks=0,
    )


def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    make_button(i)
                )
            ),
            dbc.Collapse(
                dbc.CardBody([
                    #                     html.H4(f"This is the content of group {i}..."),
                    html.Div([
                        make_button(j) for j in dictionary_sub[i]
                    ], className='d-flex flex-column m-2 p-2 flex-wrap justify-content-between', style={'width':"99%", 'margin':'auto','background': ''})
                ]),
                id=f"collapse-{i}",
                is_open=False,
            ),
        ]
    )


def modal(i):

    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(f"{df2[df2[('Sub Indictors', '')] == i][('Indicators', '')].unique().tolist()[0]} || {i}"),
                    dbc.ModalBody([
                        html.Div([
                            dcc.Graph(figure=get_graph(df2, float(df2[df2[('Sub Indictors', '')] == i][('Indicator_Code', '')].unique().tolist()[0])),
                                      config={'displayModeBar': False})
                        ], style={'width': "50%"})

                    ]),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close",
                            id="close-centered-NFHS",
                            className="ml-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="modal-centered-NFHS",
                centered=True,
                size="lg",
                is_open=True,
            ),
        ]
    )


NFHS_VIZ = html.Div([
    html.P([html.Span('National Family Health Survey (NFHS-5) 2019-21 |', style={'font-size': '40px', 'background':''}),
                   html.Span(' 131 Key Indicators',style={'font-size': '20px'})] , className='m-0 p-0'),

    html.Div([make_item(i) for i in indicators]),
    html.Div(id='model-generate-NFHS', hidden=True),
     html.Div([
                html.Div([
                    html.A('Source', href = 'http://rchiips.org/nfhs/factsheet_NFHS-5.shtml', target="_blank")
                ], className = "footer__copyright"),
                html.Div([
                    html.A('Developed by Abhinav Kumar', href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
                ], className = "footer__signature"),

        ], className = "footer")
], className="accordion",style = {'width':'1200px', 'margin':'auto'}
)


##backend

@app.callback(
    [Output(f"collapse-{i}", "is_open")
     for i in df2[('Indicators', '')].unique().tolist()],
    [Input(f"group-{i}-toggle", "n_clicks")
     for i in df2[('Indicators', '')].unique().tolist()],
    [State(f"collapse-{i}", "is_open")
     for i in df2[('Indicators', '')].unique().tolist()],
)
def toggle_accordion(*arguments):
    ctx = dash.callback_context
#     print(ctx)
    if not ctx.triggered:
        return [False for i in indicators]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(
            ".")[0].split('-toggle')[0].split('group-')[-1]
#     print(button_id)
    arguments_state = arguments[len(indicators):]
    if indicators.index(button_id)+1:
        ind = indicators.index(button_id)
        current_state = arguments_state[ind]
        final_state = not current_state
        to_return = [False for i in indicators]
        to_return[ind] = final_state
        return to_return
    else:
        return [False for i in indicators]


@app.callback(
    Output("model-generate-NFHS", "children"),
    [Input(f"group-{ii}-toggle", "n_clicks") for ii in [j.replace('.', "$$")
                                                        for i in dictionary_sub.keys() for j in dictionary_sub[i]]],
)
def toggle_modal(*arguments):
    ctx = dash.callback_context
#     print(ctx)
    if not ctx.triggered:
        return arguments[-1]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(
            ".")[0].split('-toggle')[0].split('group-')[-1]

        return modal(button_id.replace("$$", "."))


@app.callback(
    Output("modal-centered-NFHS", "is_open"),
    [Input("close-centered-NFHS", "n_clicks")],
    [State("modal-centered-NFHS", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

