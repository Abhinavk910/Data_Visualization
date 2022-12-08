from apps.whatsapp_chat_analysis.help_function import *
import pandas as pd
from datetime import datetime
import pybase64
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
from plotly import graph_objs as go
import pathlib
from app import app
############################################ creating Server  ##############################


# to add font fontawesome
# external_scripts = [
#     {'src':'https://kit.fontawesome.com/a076d05399.js'}
# ]

# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://kit.fontawesome.com/a076d05399.js'],
# # assets_external_path='http://your-external-assets-folder-url/'
#  meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
#  external_scripts=external_scripts,
# )
# server = app.server

########################################### Data #########################################

#Preparing Data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../whatsapp_chat_analysis/').resolve()


chart_path = DATA_PATH.joinpath("Data/sample.txt")
df, activity_df = parse_data(chart_path)

################  Basic Stats  ############
stats_default = basic_stats(df)
if stats_default['avg_message'] < 1:
    freq_req_default = float(stats_default['avg_message'])
else:
    freq_req_default = int(stats_default['avg_message'])

# #################  timeline Stats  ############
# date_df = date_data(df)
#
# #################  for monthly stats ##########
# analysis_df_month = date_df.groupby(["year", "month"], as_index=False, sort=[True, True])["Message"].count()
# analysis_df_month = analysis_df_month[~analysis_df_month["Message"].isnull()]
# analysis_df_month["month_year"] = analysis_df_month.apply(lambda x: x["month"] + " " + str(x["year"]), axis=1)
#
# ################# for daily stats #############
# analysis_df_daily = date_df.groupby('Date', as_index=False, sort=[True])['Message'].count()



################# layout ######################
whatsapp_layout = html.Div([

                ################################# upload #######################
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                    ),
                html.Div(id="intermediate-value", style={"display": "none"}),



                ######################################## row 1 #################

                html.Div([

                    html.Div([
                        html.Div([
                            html.Div([
                                html.A([
                                    html.Span(className="fas fa-calendar-week"),
                                ]),
                                html.Span("Started"),
                            ], className = "social-media2"),
                            html.H6(id = "started",children = [])
                        ], className = "card mini_container medium_container")
                    ], className = "col-md-3 col-sm-6"),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.A([
                                    html.Span(className="fas fa-users"),
                                ]),
                                html.Span("Members"),
                            ], className = "social-media2"),
                            html.H6(id = "members",children = [])
                        ], className = "card mini_container medium_container")
                    ], className = "col-md-3 col-sm-6"),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.A([
                                    html.Span(className="fas fa-comments"),
                                ]),
                                html.Span("Messages"),
                            ], className = "social-media2"),
                            html.H6(id = "messages",children = [])

                        ], className = "card mini_container medium_container")
                    ], className = "col-md-3 col-sm-6"),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.A([
                                    html.Span(className="fas fa-chart-line"),
                                ]),
                                html.Span("Avg. Message"),
                            ], className = "social-media2"),
                            html.H6(id = "average",children = [])

                        ], className = "card mini_container medium_container")
                    ], className = "col-md-3 col-sm-6"),
                ], className = "row"),

                ################################### row 2 ######################

                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id='timeline_dropdown',
                                options=[
                                    {'label': 'Monthly', 'value': 'month'},
                                    {'label': 'Daily', 'value': 'daily'},
                                ],
                                value='month'
                            ),
                        ], className="dropdown_color")
                    ], className="col-md-3 col-sm-12"),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='graph_timeline')
                        ])
                    ], className="col-md-9 col-sm-12")
                ], className = 'row mini_container' ),

                ######################################## row 3 #################

                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='timeline_dropdown2',
                            options=[
                                {'label': 'Year', 'value': 'Year'},
                                {'label': 'Month', 'value': 'Month'},
                                {'label': 'Weekly', 'value': 'Weekly'},
                                {'label': 'Daily', 'value': 'Daily'},
                                {'label': 'Hourly', 'value': 'Hourly'},

                            ],
                            value='Year'
                        ),
                    ], className="col-md-3 col-sm-12 dropdown_color"),
                    html.Div([
                        dcc.Graph(id='graph_bar')
                    ], className="col-md-9 col-sm-12")
                ], className = 'row mini_container'),

                ######################################## row 4 ####################################
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id="members_list",
                            placeholder="Select a Member",
                            clearable=False,
                            multi=True,
                        )
                    ], className = "dropdown_color col-md-3 col-sm-12"),
                    html.Div([
                        dcc.Graph(id='graph_author_line')
                    ], className = "col-md-9 col-sm-12")
                ], className = 'row mini_container'),

                ######################################## row 5 ####################################


                html.Div([
                    html.Div([
                        dcc.Graph(id='graph_treemap')
                    ], className = "col-sm-12 col-md-12 col-xl-12"),
                ], className = 'row mini_container')
            ])



################ plotly brain #################

######################## Tackle upload data  ################################

@app.callback(Output('intermediate-value', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
              State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:

        content_type, content_string = list_of_contents[0].split(',')
        decoded = pybase64.b64decode(content_string)

        if 'txt' in list_of_names[0]:
            # Assume that the user uploaded a CSV file
            # print(decoded)
            Data = []
            messageBuffer = []
            date, time, author = None, None, None
            txt_data = decoded.decode('utf-8').split('\n')
            for fp in  range(1, len(txt_data)):
                fp = txt_data[fp]
                if not fp:
                    continue


                if startsWithDateAndTime(fp):
                    if len(messageBuffer) != 0:
                        Data.append([date, time, author, ' '.join(messageBuffer)])
                    messageBuffer.clear()
                    date, time, author, message = getDataPoint(fp)
                    messageBuffer.append(message)
                else:
                    messageBuffer.append(fp)
                # print(messageBuffer)
            df = pd.DataFrame(Data, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.
            df["Date"] = pd.to_datetime(df["Date"])
            df["Time"] = df["Time"].str.strip()
            df["Time"] = pd.to_datetime(df["Time"])
            df["Time"] = df["Time"].apply(lambda x: x.time())

            return df.to_json(date_format="iso", orient="split")



######################## Tackle row 1  ######################################


@app.callback([Output('started', 'children'),
               Output('members', 'children'),
               Output('messages', 'children'),
               Output('average', 'children')],
               [Input("intermediate-value", "children")])
def update_output(df_data):


    if df_data is not None:
        df = pd.read_json(df_data, orient="split")
        df_2 = df[~df["Author"].isnull()].reset_index(drop=True)
        stats = basic_stats(df_2)
        if stats['avg_message'] < 1:
            freq_req = float(stats['avg_message'])
        else:
            freq_req = int(stats['avg_message'])
        return stats['formed'].strftime("%d %b, %Y"), stats['author'], f'{stats["messages"]:,}', freq_req

    else:

        return stats_default['formed'].strftime("%d %b, %Y"), stats_default['author'], f'{stats_default["messages"]:,}', freq_req_default

######################## Tackle row 4 col2  ######################################


@app.callback([Output('members_list', 'options'),
               Output('members_list', 'value')],
              [Input("intermediate-value", "children")])
def update_dropdown(df_data):
    if df_data is not None:
        df_final = pd.read_json(df_data, orient="split")
        df_final = df_final[~df_final["Author"].isnull()].reset_index(drop=True)
        tt, authors_list, value = author_date_date(df_final)

    else:
        tt, authors_list, value = author_date_date(df)
    authors_list = companies = [{'label': i, 'value': i} for i in authors_list]
    return authors_list, value


@app.callback(Output('graph_author_line', 'figure'),
              [Input("intermediate-value", "children"),
               Input('members_list', 'value')])
def updete_author(df_data, values):
    if df_data is not None:
        df_final = pd.read_json(df_data, orient="split")
        df_final = df_final[~df_final["Author"].isnull()].reset_index(drop=True)
        t_analysis_data, authors_list, value = author_date_date(df_final)

    else:
        t_analysis_data, authors_list, value = author_date_date(df)


    fig = px.area(t_analysis_data[values])
    # fig.update_xaxes(rangeslider_visible=True)
    fig = update_fig(fig, xtitle = 'Time', ytitle = 'Messages', toptitle = 'Message Timeline',graph_height = 400)
    fig.update_layout(
        legend_title_text = 'Members',
        showlegend = True,
    #     legend=dict(
    #
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #     x=1
    )
    return fig




######################## Tackle data and graph  ################################

@app.callback([Output('graph_timeline', 'figure'),
                Output('graph_bar', 'figure'),
                Output('graph_treemap', 'figure')],
              [Input("intermediate-value", "children"),
               Input('timeline_dropdown', 'value'),
               Input('timeline_dropdown2', 'value')])
def update_map(df_data, average, average2):

    if df_data is not None:
        df_final = pd.read_json(df_data, orient="split")
        df_final = df_final[~df_final["Author"].isnull()].reset_index(drop=True)
        # activity_df = df[df["Author"].isnull()]
        date_df = date_data(df_final)


        #################  for monthly stats ##########
        analysis_df_month = date_df.groupby(["year", "month"], as_index=False, sort=[True, True])["Message"].count()
        analysis_df_month = analysis_df_month[~analysis_df_month["Message"].isnull()]
        analysis_df_month["month_year"] = analysis_df_month.apply(lambda x: x["month"] + " " + str(x["year"]), axis=1)

        ################# for daily stats #############
        analysis_df_daily = date_df.groupby('Date', as_index=False, sort=[True])['Message'].count()

        author_df = author_data(df_final)

    else:
        date_df = date_data(df)

        #################  for monthly stats ##########
        analysis_df_month = date_df.groupby(["year", "month"], as_index=False, sort=[True, True])["Message"].count()
        analysis_df_month = analysis_df_month[~analysis_df_month["Message"].isnull()]
        analysis_df_month["month_year"] = analysis_df_month.apply(lambda x: x["month"] + " " + str(x["year"]), axis=1)

        ################# for daily stats #############
        analysis_df_daily = date_df.groupby('Date', as_index=False, sort=[True])['Message'].count()

        author_df = author_data(df)


    #################################### fig1 ##################################
    if average == "month":
        fig = px.line(analysis_df_month, x='month_year', y='Message')
        fig.update_xaxes(rangeslider_visible=True)
        fig = update_fig(fig, xtitle = 'Time', ytitle = 'Message Count', toptitle = 'Message Timeline',graph_height = 400)


    else:
        fig = px.line(analysis_df_daily, x='Date', y='Message')
        fig.update_xaxes(rangeslider_visible=True)
        fig = update_fig(fig, xtitle = 'Time', ytitle = 'Message Count', toptitle = 'Message Timeline')

    #################################### fig2 ##################################


    if average2 == 'Month':
        data = analysis_df_month.groupby("month", as_index=False)["Message"].mean().round(0)
        fig2 = px.bar(data, x='month', y='Message',
                     hover_data=['month', 'Message'], color='Message')
        fig2 = update_fig(fig2, xtitle = 'Month', ytitle = 'Average Message',toptitle = 'None', graph_height = 300)

    elif average2 == 'Weekly':
        data = date_df.groupby(["year","week", "day_of_week"], as_index=False, sort=[True, True])["Message"].count()
        data = data[~data["Message"].isnull()]
        data = data.groupby("day_of_week", as_index=False)["Message"].mean().round(0)
        fig2 = px.bar(data, x='day_of_week', y='Message',
                     hover_data=['day_of_week', 'Message'], color='Message')
        fig2 = update_fig(fig2, xtitle = 'Week', ytitle = 'Average Message',toptitle = 'None', graph_height = 300)

    elif average2 == 'Daily':
        data = date_df.groupby(["year","month", "day"], as_index=False, sort=[True, True])["Message"].count()
        data = data[~data["Message"].isnull()]
        data = data.groupby("day", as_index=False)["Message"].mean().round(0)
        fig2 = px.bar(data, x='day', y='Message',
                     hover_data=['day', 'Message'], color='Message')
        fig2 = update_fig(fig2, xtitle = 'Daily', ytitle = 'Average Message',toptitle = 'None', graph_height = 300)

    elif average2 == 'Hourly':
        data = date_df.groupby(["year","month", "day", "hour"], as_index=False, sort=[True, True])["Message"].count()
        data = data[~data["Message"].isnull()]
        data = data.groupby("hour", as_index=False)["Message"].sum().round(0)
        data["part_of_day"] = data["hour"].apply(lambda x: part_of_day(x))
        fig2 = px.bar(data, x='hour', y='Message',
                     hover_data=['hour', 'Message'],
                     hover_name='part_of_day',
                     color='part_of_day',
                     )
        fig2 = update_fig(fig2, xtitle = 'Daily', ytitle = 'Total Message',toptitle = 'None', graph_height = 300)

        fig2.update_layout(
            # legend_title_text = 'Part of Day :-',
            showlegend = False,
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    else:
        data = analysis_df_month.groupby("year", as_index=False)["Message"].mean().round(0)
        fig2 = px.bar(data, x='year', y='Message',
                     hover_data=['year', 'Message'], color='Message')
        fig2 = update_fig(fig2, xtitle = 'Year', ytitle = 'Average Message',toptitle = 'None', graph_height = 300)
        fig2.update_layout(
            xaxis = dict(
                tickvals = data.year.tolist()
            )
        )

    #################################### fig3 ##################################


    fig3 = go.Figure()
    labels = author_df["Author"].values
    parents = []
    fig3.add_trace(go.Treemap(
        labels = labels,
        parents = [""]*len(labels),
        values =  author_df["Number of messages"].values,
        textinfo = "label+value+percent parent",
        textfont={'size':14},
        meta={"title.text":"Hi"},
        opacity = 0.8
    ))
    fig3 = update_fig(fig3, xtitle = 'Year', ytitle = 'Average Message',toptitle = 'Percentage of Messages', graph_height = 400)
    # fig3.update_layout(title_text="Message Distribution")


    ################################################################################################################

    return fig, fig2, fig3








if __name__ == '__main__':
    app.run_server(debug=True, port = 1000)
