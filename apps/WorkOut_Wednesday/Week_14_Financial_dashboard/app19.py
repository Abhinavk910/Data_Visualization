
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pathlib
import plotly.graph_objects as go
from app import app
import pandas as pd

def figure_config(text_y, min_d, max_d):
    return {
        'title_text' : "",
        'plot_bgcolor' : 'white',
        'paper_bgcolor' : 'white',
        'hovermode':"x unified",
        'margin' : dict(t=0, l=0, r=50, b=0, pad = 0),
        'showlegend' : False,
        'xaxis' : dict(title=dict(text = '', font=dict(size=18, family='Courier', color='crimson'), standoff = 20),
                         range=['2004','2018'],
                         showticklabels=True,  # this is for toggling x axis label to show or not
                         showline=False,        # this is for showing line in x axis, it different from zeroline
                         showgrid=False,
                         zeroline =False,
                         layer='above traces',
                         tickmode = 'array',
                         tickvals = [2005, 2010, 2015],
                         ticks="",
                         tickwidth=1.5,
                         tickcolor='black',
                         ticklen=10,
                         fixedrange=True,  # Disabling Pan/Zoom on Axes
                         tickprefix = "  ",
                         ticksuffix = "  ",
                         showspikes = True,
                         spikemode = 'across',#"toaxis", "across", "toaxis+across", "toaxis+across+marker"
                         spikecolor = 'grey',
                         spikethickness = 2,
                         spikedash = "solid", #"solid", "dot", "dash", "longdash", "dashdot", or "longdashdot"
                         spikesnap = 'hovered data',#"data" | "cursor" | "hovered data"

                                ),
        'yaxis' : dict(title=dict(text = text_y, font=dict(size=12),
                                  ),
                                 range=[min_d,max_d],
                                 rangemode = 'normal',
                                 showline = True,
                                 showgrid=True,
                                 fixedrange=True,
                                 zeroline = False,
                                 nticks = 2,
                                 ticks="",
                                 mirror=False),
        'hoverlabel' : dict(bgcolor="white", font_size=12,)
    }

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../Week_14_Financial_dashboard/').resolve()

df = pd.read_csv(DATA_PATH.joinpath("data2.csv"))


www14_wiz = dbc.Container([
    html.Div(id='revenue'),
    dbc.Row([
        dbc.Col([
            html.P([html.Span('NCAA Revenues & Expenses |', style={'font-size': '2.5vw', 'background':''}),
                   html.Span(' Summary View',style={'font-size': '1.2vw'})] , className='m-0 p-0')
        ], md = 8),
        dbc.Col([
            html.P('Year', className='mb-1 mt-0 p-0',style={'font-size': '1.0vw'}),
            dcc.Dropdown(id='sortvalue',
                             placeholder='Select year ',
                             options=[{'label': i, 'value': i} for i in ['All'] + df.Year.unique().tolist()],
                             value='All', multi=False,
                             style={'height': '4vh', 'width': '8.0vw', 'font-size': "0.9vw",'display': 'inline-block',},
                             className='m-0 p-0'
                             ),
        ], md=2,align="end", style = {'background': '',},   )
    ], justify="between",align="end" , style = {'background':''}, className='m-0 p-0'),
    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    dbc.Row([
        dbc.Col([
            html.P('Revenues', style = {'text-align': 'left','background':'','font-size':"1.5vw"}, className='m-0 p-0'),
            html.P(children=[''],id = 'www14-3', style = {'text-align': 'center','background':'', 'font-size':"3.0vw"}, className='m-0 p-0'),
            html.P('Total Revenues USD', style = {'text-align': 'center','background':'', 'font-size':"1.0vw"}, className='m-0 p-0'),
            dcc.Graph(id = 'www14-1', config={'displayModeBar': False},style={'height': '30vh', 'width': '100%','background':''}),
            html.P('Revenues by Conference in USD', style = {'text-align': 'left','background':'','font-size':"1.5vw"}, className='m-0 p-0'),
            dcc.Graph(id = 'www14-2', config={'displayModeBar': False},style={'height': '60vh', 'width': '100%','background':''}),

        ], sm = 12, md = 4, style = {'background':''} ),
        dbc.Col([
            html.P('Expenses', style = {'text-align': 'left','background':'','font-size':"1.5vw"}, className='m-0 p-0'),
            html.P(children=[''],id = 'www14-6', style = {'text-align': 'center','background':'', 'font-size':"3.0vw"}, className='m-0 p-0'),
            html.P('Total Expenses USD', style = {'text-align': 'center','background':'', 'font-size':"1.0vw"}, className='m-0 p-0'),
            dcc.Graph(id = 'www14-4', config={'displayModeBar': False},style={'height': '30vh', 'width': '100%','background':''}),
            html.P('Expenses by Conference in USD', style = {'text-align': 'left','background':'','font-size':"1.5vw"}, className='m-0 p-0'),
            dcc.Graph(id = 'www14-5', config={'displayModeBar': False},style={'height': '60vh', 'width': '100%','background':''}),

        ], sm = 12, md = 4, style = {'background':''} ),
        dbc.Col([
            html.P('Profits', style = {'text-align': 'left','background':'','font-size':"1.5vw"}, className='m-0 p-0'),
            html.P(children=[''],id = 'www14-9', style = {'text-align': 'center','background':'', 'font-size':"3.0vw"}, className='m-0 p-0'),
            html.P('Total Profits USD', style = {'text-align': 'center','background':'', 'font-size':"1.0vw"}, className='m-0 p-0'),
            dcc.Graph(id = 'www14-7', config={'displayModeBar': False},style={'height': '30vh', 'width': '100%','background':''}),
            html.P('Profits by Conference in USD', style = {'text-align': 'left','background':'','font-size':"1.5vw"}, className='m-0 p-0'),
            dcc.Graph(id = 'www14-8', config={'displayModeBar': False},style={'height': '60vh', 'width': '100%','background':''}),

        ], sm = 12, md = 4, style = {'background':''} ),
        ], className='m-0 p-0'),
        html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
        dbc.Row([
            dbc.Col([
                    html.P(['WorkOut Wednesday Week 14']),
            ], sm = 12, md = 4),
            dbc.Col([
                html.A(html.P('Get Data'), href='https://data.world/annjackson/wow-google-analytics', target = "_blank")
            ], sm = 12, md = 4),
            dbc.Col([
                html.P("Developed By: "),
                html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]), href = 'http://www.linkedin.com/in/abhinavk910', target="_blank")
            ], style = {'display': 'flex'}, sm = 12, md = 4)

        ], justify="center", className='m-0 p-0')


], fluid=True,style = {'background': 'white'})

to_replace = {'American Athletic Conference':'AAC',
'Atlantic Coast Conference':'ACC',
'Big 12 Conference':"B12",
'Big East Conference':'BEC',
'Big Ten Conference':'B10',
'Conference USA':'CUSA',
'FBS Total':'FBS',
'Independent':'IND',
'Mid-American Conference':'MAC',
'Mountain West Conference':'MWC',
'Pacific-12 Conference':"P12",
'Southeastern Conference':'SOC',
'Sun Belt Conference':"SBC",
'Western Athletic Conference':'WAC'}

def full(x):

    for i, j in to_replace.items():

        if j == x:
            return i





@app.callback(
    [Output('www14-3', 'children'),Output('www14-6', 'children'), Output('www14-9', 'children')],
    [Input('sortvalue','value'), Input("www14-2", "selectedData"), Input("www14-5", "selectedData"), Input("www14-8", "selectedData")]
)
def populateheading(year, data, data2, data3):
#     print(data)

    # df = pd.read_csv('data2.csv')
    if data or data2 or data3:
        if data:
            x = data['points'][0]['label']
        elif data3:
            x = data3['points'][0]['label']
        else:
            x = data2['points'][0]['label']

        if year == 'All':
            rev = int(df[df['FBS Conference'] == x]['Total Revenues'].sum()/1000000)
            rev2 = int(df[df['FBS Conference'] == x]['Total Expenses'].sum()/1000000)
            rev3 = int(df[df['FBS Conference'] == x]['Profit'].sum()/1000000)
        else:
            rev = int(df[(df['FBS Conference'] == x) & (df.Year == year)]['Total Revenues'].sum()/1000000)
            rev2 = int(df[(df['FBS Conference'] == x) & (df.Year == year)]['Total Expenses'].sum()/1000000)
            rev3 = int(df[(df['FBS Conference'] == x) & (df.Year == year)]['Profit'].sum()/1000000)
    else:
        if year == 'All':
            rev = int(df['Total Revenues'].sum()/1000000)
            rev2 = int(df['Total Expenses'].sum()/1000000)
            rev3 = int(df['Profit'].sum()/1000000)
        else:
            rev = int(df.loc[df.Year == year]['Total Revenues'].sum()/1000000)
            rev2 = int(df.loc[df.Year == year]['Total Expenses'].sum()/1000000)
            rev3 = int(df.loc[df.Year == year]['Profit'].sum()/1000000)

    return  "{:,} M".format(rev),  "{:,} M".format(rev2), "{:,} M".format(rev3)


@app.callback(
    [Output('www14-1', 'figure'),Output('www14-4', 'figure'),Output('www14-7', 'figure')],
    [Input('sortvalue','value'),
    Input("www14-2", "selectedData"),
    Input("www14-5", "selectedData"),
    Input("www14-8", "selectedData"),
]
)
def plotconstant(value, data, data2, data3):
    # dff = pd.read_csv('data2.csv')

    if data or data2 or data3:
        if data:
            x = data['points'][0]['label']
        elif data3:
            x = data3['points'][0]['label']
        else:
            x = data2['points'][0]['label']
        fig = go.Figure()
        dff = df[df['FBS Conference'] == x]
        min_d = dff['Total Revenues'].min() - 10000000
        max_d = dff['Total Revenues'].max() + 10000000
        fig.add_trace(go.Scatter(x=dff.Year, y=dff['Total Revenues'], fill='tozeroy', mode = 'lines',
                                 text = ["{:,} M".format(int(i/1000000)) for i in dff['Total Revenues'].tolist()],

                                hovertemplate =
                                            '<extra></extra><b>%{text}</b><extra></extra>',
                                showlegend = False))
    else:
        fig = go.Figure()
        dff = df.groupby('Year').agg({'Total Revenues':'sum'}).reset_index()
        min_d = dff['Total Revenues'].min() - 1000000000
        max_d = dff['Total Revenues'].max() + 1000000000
        fig.add_trace(go.Scatter(x=dff.Year, y=dff['Total Revenues'], fill='tozeroy', mode = 'lines',
                                text = ["{:,} M".format(int(i/1000000)) for i in dff['Total Revenues'].tolist()],
                                hovertemplate =
                                            '<b>%{text}</b><extra></extra>',showlegend = False))

    fig.update_layout(figure_config('Total Revenues', min_d, max_d))

    if data or data2 or data3:
        if data:
            x = data['points'][0]['label']
        elif data3:
            x = data3['points'][0]['label']
        else:
            x = data2['points'][0]['label']
        fig2 = go.Figure()
        dff = df[df['FBS Conference'] == x]
        min_d = dff['Total Expenses'].min() - 10000000
        max_d = dff['Total Expenses'].max() + 10000000
        fig2.add_trace(go.Scatter(x=dff.Year, y=dff['Total Expenses'], fill='tozeroy', mode = 'lines' , line_color='indigo',
                                  text = ["{:,} M".format(int(i/1000000)) for i in dff['Total Expenses'].tolist()],
                                hovertemplate =
                                            '<b>%{text}</b><extra></extra>',showlegend = False))
    else:
        fig2 = go.Figure()
        dff = df.groupby('Year').agg({'Total Expenses':'sum'}).reset_index()
        min_d = dff['Total Expenses'].min() - 1000000000
        max_d = dff['Total Expenses'].max() + 1000000000
        fig2.add_trace(go.Scatter(x=dff.Year, y=dff['Total Expenses'], fill='tozeroy', mode = 'lines', line_color='indigo',
                                 text = ["{:,} M".format(int(i/1000000)) for i in dff['Total Expenses'].tolist()],
                                hovertemplate =
                                            '<b>%{text}</b><extra></extra>',showlegend = False))
    fig2.update_layout(figure_config('Total Expenses', min_d, max_d))

    if data or data2 or data3:
        if data:
            x = data['points'][0]['label']
        elif data3:
            x = data3['points'][0]['label']
        else:
            x = data2['points'][0]['label']
        fig3 = go.Figure()
        dff = df[df['FBS Conference'] == x]
        min_d = dff['Profit'].min() - 10000000
        max_d = dff['Profit'].max() + 10000000
        fig3.add_trace(go.Scatter(x=dff.Year, y=dff['Profit'], fill='tozeroy', mode = 'lines' , line_color='#000EAF',
                                  text = ["{:,} M".format(int(i/1000000)) for i in dff['Profit'].tolist()],
                                hovertemplate =
                                            '<b>%{text}</b><extra></extra>',showlegend = False))
    else:
        fig3 = go.Figure()
        dff = df.groupby('Year').agg({'Profit':'sum'}).reset_index()
        min_d = dff['Profit'].min() - 10000000
        max_d = dff['Profit'].max() + 10000000
        fig3.add_trace(go.Scatter(x=dff.Year, y=dff['Profit'], fill='tozeroy', mode = 'lines', line_color='#000EAF' ,
                                  text = ["{:,} M".format(int(i/1000000)) for i in dff['Profit'].tolist()],
                                hovertemplate =
                                            '<b>%{text}</b><extra></extra>',showlegend = False))
    fig3.update_layout(figure_config('Profits', min_d, max_d))

    return  fig, fig2, fig3

@app.callback(
  Output('www14-2', 'figure'),
    [Input('sortvalue','value'),
    Input("www14-5", "selectedData"),Input("www14-8", "selectedData")]
)
def plotgraph2(year, data, data2):
    # dff = pd.read_csv('data2.csv')
    if year == 'All':
        dd = df.groupby('FBS Conference').agg({'Total Revenues':'sum'}).reset_index()
    else:
        dd = df[df.Year == year].groupby('FBS Conference').agg({'Total Revenues':'sum'}).reset_index()
    fig = go.Figure()
    if data:
        x = data['points'][0]['label']
    elif data2:
        x = data2['points'][0]['label']
    else:
        x = None
    opacity_req = 1
    dd['full name'] = dd.apply(lambda x: full(x[0]), axis = 1)
    for i, row in dd.iterrows():
        if x:
            if row['FBS Conference'] == x:
                opacity_req = 1
            else:
                opacity_req = 0.2


        fig.add_trace(
            go.Bar(y=[row["FBS Conference"]],
                   x=[row["Total Revenues"]], orientation = 'h',
    #                name=row["Sub-Category"],
                   showlegend=False,
                   marker_color='#636EFA',
                   opacity=opacity_req,
    #                text = [abs(row['per_cha'])]
                   text = ["{:,} M".format(int(row["Total Revenues"]/1000000))],
                   textposition='auto',
                   texttemplate='%{text}',
                   hovertemplate = f'<b>{row["full name"]}</b>'+
                                    '<br><b>%{text}</b><br><extra></extra>'
                   )),

    fig.update_layout(clickmode='event+select',uniformtext_minsize=8, uniformtext_mode='hide',
                      yaxis={'categoryorder':'total ascending',
                            'ticksuffix': "  ",},
                      margin = dict(t=20, l=0, r=50, b=0, pad = 0),
                      plot_bgcolor= 'white',
                      paper_bgcolor = 'white',
                      xaxis={
                          'showticklabels':False,'title_text':"" , #'range':[0,dd['Total Revenues'].max()+100000000],
                      } )
    return fig

@app.callback(
    Output('www14-5', 'figure'),
    [Input('sortvalue','value'),
    Input("www14-2", "selectedData"),Input("www14-8", "selectedData")]
)
def plotgraph3(year, data, data2):
    # dff = pd.read_csv('data2.csv')
    if year == 'All':
        dd = df.groupby('FBS Conference').agg({'Total Expenses':'sum'}).reset_index()
    else:
        dd = df[df.Year == year].groupby('FBS Conference').agg({'Total Expenses':'sum'}).reset_index()
    fig = go.Figure()
    if data:
        x = data['points'][0]['label']
    elif data2:
        x = data2['points'][0]['label']
    else:
        x = None
    opacity_req = 1
    dd['full name'] = dd.apply(lambda x: full(x[0]), axis = 1)
    for i, row in dd.iterrows():
        if x:
            if row['FBS Conference'] == x:
                opacity_req = 1
            else:
                opacity_req = 0.2


        fig.add_trace(
            go.Bar(y=[row["FBS Conference"]],
                   x=[row["Total Expenses"]], orientation = 'h',
    #                name=row["Sub-Category"],
                   showlegend=False,
                   marker_color='indigo',
                   opacity=opacity_req,
                   hovertemplate = f'<b>{row["full name"]}</b>'+
                                    '<br><b>%{text}</b><br><extra></extra>',

    #                text = [abs(row['per_cha'])]
                   text = ["{:,} M".format(int(row["Total Expenses"]/1000000))],
                   textposition='auto',
                   texttemplate='%{text}',
                   )),

    fig.update_layout(clickmode='event+select',uniformtext_minsize=8, uniformtext_mode='hide',
                      yaxis={'categoryorder':'total ascending',
                            'ticksuffix': "  ",},
                      margin = dict(t=20, l=0, r=50, b=0, pad = 0),
                      plot_bgcolor= 'white',
                      paper_bgcolor = 'white',
                      xaxis={
                          'showticklabels':False,'title_text':""
                      } )
    return fig

@app.callback(
    Output('www14-8', 'figure'),
    [Input('sortvalue','value'),
    Input("www14-2", "selectedData"),Input("www14-5", "selectedData")]
)
def plotgraph3(value, data, data2):
    # dff = pd.read_csv('data2.csv')
    if value == 'All':
        dd = df.groupby('FBS Conference').agg({'Profit':'sum'}).reset_index()

    else:
        dd = df[df.Year == value].groupby('FBS Conference').agg({'Profit':'sum'}).reset_index()

    fig = go.Figure()
    if data:
        x = data['points'][0]['label']
    elif data2:
        x = data2['points'][0]['label']
    else:
        x = None
    opacity_req = 1
    dd['full name'] = dd.apply(lambda x: full(x[0]), axis = 1)
    for i, row in dd.iterrows():
        if x:
            if row['FBS Conference'] == x:
                opacity_req = 1
            else:
                opacity_req = 0.2


        fig.add_trace(
            go.Bar(y=[row["FBS Conference"]],
                   x=[row["Profit"]], orientation = 'h',
    #                name=row["Sub-Category"],
                   showlegend=False,
                   marker_color='#000EAF',
                   opacity=opacity_req,
    #                text = [abs(row['per_cha'])]
                   text = ["{:,} M".format(int(row["Profit"]/1000000))],
                   textposition='auto',
                   texttemplate='%{text}',
                   hovertemplate = f'<b>{row["full name"]}</b>'+
                                    '<br><b>%{text}</b><br><extra></extra>'
                   )),

    fig.update_layout(clickmode='event+select',uniformtext_minsize=8, uniformtext_mode='hide',
                      yaxis={'categoryorder':'total ascending',
                            'ticksuffix': "  ",},
                      margin = dict(t=20, l=0, r=50, b=0, pad = 0),
                      plot_bgcolor= 'white',
                      paper_bgcolor = 'white',
                      xaxis={
                          'showticklabels':False,'title_text':""
                      } )
    return fig
