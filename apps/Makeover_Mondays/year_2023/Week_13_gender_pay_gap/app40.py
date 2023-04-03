import dash_mantine_components as dmc
from dash import html, dcc, Dash
import pandas as pd
import plotly.express as px
from dash_iconify import DashIconify
import numpy as np

from app import app

text = """category	Female	Male
Qualifying for the World Cup	37500	108695
Winning individual qualification games	15000	200000
Called up to World Cup side	37500	68750
Advancing to the knockout stages	0	329376
Winning the World Cup	110000	407608"""

data = [i.split('\t') for i in text.split("\n")]
df = pd.DataFrame(data[1:], columns=data[0])
df = df.melt(id_vars=['category'], value_vars=['Female', 'Male'], value_name='val', var_name='gender')
# df.dropna(inplace=True)
df['val'] = df.val.astype('float')



colors = {
    'Female': '#ef7b8b',
    'Male': '#3e607a',
}

label = df['val'].apply(lambda x:'{:,.0f}K'.format(x/1000))

fig = px.scatter(data_frame=df, x='gender', y='category', size='val',size_max=40, color='gender',
                 color_discrete_map=colors, custom_data=['val'], text=label, )

fig.update_xaxes(showgrid=False,range=[-0.5, 1.5], ticktext=['Female', 'Male'], tickvals=[0, 1],
                title='')
fig.update_yaxes(showgrid=False, title="")
fig.update_layout(hovermode='y unified', hoverlabel=dict(align='auto',font=dict(family='Roboto'),
                                                         bordercolor='black', bgcolor='white',
                                                         namelength=-1, font_size=12))
fig.update_layout(showlegend=False, plot_bgcolor='#fff', height=400, font={'color':'grey', 'size':10, 'family':'sans-serif'},
                 margin={'l':10, 't':50, 'b':50, 'r':10, 'pad':0},)
fig.update_traces(hovertemplate="$%{customdata[0]:,.0f}", textposition='middle right')

annotations = []

annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=1.03,
                            text=f'The Gender Pay Gap in US World Cup Bonuses',
                            font=dict(family='Inter', size=20,
                                      color='#3a3738'),
                            showarrow=False))
annotations.append(dict(xref='paper', yref='paper',
                            x=0.8, y=-0.17,
                            text=f'Data Source: The Guardian (from US soccer)',
                            font=dict(family='Inter', size=10,
                                      color='#969093'),
                            showarrow=False))
fig.update_layout(annotations=annotations)


app = JupyterDash(__name__)

backcolor = "#ECF9FF"
containercolor= "#f1faee"
paper_color = "#a8dadc"
selectcolor = "#457b9d"

app_layout = dmc.Container(children=[
    dmc.Stack([
        dmc.Paper(
            dmc.Group(children=[
                dmc.Text(['MakeOver Monday W13, 2023'], align='center', color='#033546', weight=700),
                dmc.Group(children=[
                      dmc.Text(['Created By ', dmc.Anchor("Abhinav Kumar",href="http://www.linkedin.com/in/abhinavk910",
                                        target="_blank", style={'text-decoration': 'none', 'color':selectcolor})
                      ], align='center', color=paper_color, weight=700),  
                    html.A(
                        dmc.Avatar(src='https://github.com/Abhinavk910/portfolio/blob/main/img/img-2.jpg',
                            size="xs",radius="lg"),
                    href="https://abhinavk910.github.io/portfolio/",
                    target="_blank",
                    ),
                    html.A(
                        dmc.Avatar(DashIconify(icon="mdi:linkedin", width=15, color=paper_color),#'#0a66c2'
                            size="xs",radius="xs"),
                    href="http://www.linkedin.com/in/abhinavk910",
                    target="_blank",
                    ),
                    html.A(
                        dmc.Avatar(DashIconify(icon="mdi:github", width=15, color=paper_color),#'#24292f'
                            size="xs",radius="xs"),
                    href="https://github.com/Abhinavk910/Data-Visualization/tree/main/apps/Makeover_Mondays",
                    target="_blank",
                    )
                ], spacing='xs', position='right')
            ], position='apart'),
            
            p=10, px=20, mb=1, radius=30,shadow="md",mx=2, style={"background-color": containercolor}
        ),
        dmc.Paper(
            children=[
                    dmc.Grid(
                        children=[
                            dmc.Col(
                                children=[
                                    dcc.Graph(figure=fig),                                
                                ])
                        ],align="flex-end")  
            ],className="",
             p=20, mb=1, radius=30,shadow="md",mx=2, style={"background-color": paper_color}
#             shadow="md",style={'max-width':'900px', "background-color": containercolor, 'margin':'auto'},p=20, radius=30
        ),
        dmc.Paper(children=[
            dmc.Group([
                dmc.Text(["Data : ",
                          dmc.Anchor(
                            "Dataworld",
                              href="https://data.world/makeovermonday/2023w13",
                              underline=False, target="_blank",
                        )], size=10),
            ])
        ],p=10, px=20, mb=10, radius=30,shadow="sm",mx=2, style={"background-color": containercolor}
        )
    ], style={'overflow-x': 'auto', 'max-width':'900px', 'min-width':'600px', 'margin':'auto'})
], size='auto',m=0,p=20, className='min-vh-100 mx-sm-0 mx-md-auto d-flex justify-content-center align-items-center', 
             style={"background-color": backcolor})

mmw13_2023_layout = dmc.MantineProvider(
        theme={
            'fontFamily': '"Inter", sans-serif',
            },
        children=[app_layout])