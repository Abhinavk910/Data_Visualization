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
import io
import base64
import requests
from bs4 import BeautifulSoup
import time
import re
from matplotlib import pyplot as plt
import operator

STOPWORDS= {'a',
 'about',
 'above',
 'after',
 'again',
 'against',
 'all',
 'also',
 'am',
 'an',
 'and',
 'any',
 'are',
 "aren't",
 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',
 "can't",
 'cannot',
 'com',
 'could',
 "couldn't",
 'did',
 "didn't",
 'do',
 'does',
 "doesn't",
 'doing',
 "don't",
 'down',
 'during',
 'each',
 'else',
 'ever',
 'few',
 'for',
 'from',
 'further',
 'get',
 'had',
 "hadn't",
 'has',
 "hasn't",
 'have',
 "haven't",
 'having',
 'he',
 "he'd",
 "he'll",
 "he's",
 'hence',
 'her',
 'here',
 "here's",
 'hers',
 'herself',
 'him',
 'himself',
 'his',
 'how',
 "how's",
 'however',
 'http',
 'i',
 "i'd",
 "i'll",
 "i'm",
 "i've",
 'if',
 'in',
 'into',
 'is',
 "isn't",
 'it',
 "it's",
 'its',
 'itself',
 'just',
 'k',
 "let's",
 'like',
 'me',
 'more',
 'most',
 "mustn't",
 'my',
 'myself',
 'no',
 'nor',
 'not',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'otherwise',
 'ought',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 'r',
 'same',
 'shall',
 "shan't",
 'she',
 "she'd",
 "she'll",
 "she's",
 'should',
 "shouldn't",
 'since',
 'so',
 'some',
 'such',
 'than',
 'that',
 "that's",
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 "there's",
 'therefore',
 'these',
 'they',
 "they'd",
 "they'll",
 "they're",
 "they've",
 'this',
 'those',
 'through',
 'to',
 'too',
 'under',
 'until',
 'up',
 'very',
 'was',
 "wasn't",
 'we',
 "we'd",
 "we'll",
 "we're",
 "we've",
 'were',
 "weren't",
 'what',
 "what's",
 'when',
 "when's",
 'where',
 "where's",
 'which',
 'while',
 'who',
 "who's",
 'whom',
 'why',
 "why's",
 'with',
 "won't",
 'would',
 "wouldn't",
 'www',
 'you',
 "you'd",
 "you'll",
 "you're",
 "you've",
 'your',
 'yours',
 'yourself',
 'yourselves'}

def bs(link):
    response=requests.get(link)
    soup=BeautifulSoup(response.text, "html.parser")
    return soup

def newvalue(OldValue, num):
    OldMax = num[0]
    OldMin = num[-1]
    NewMax = 50
    NewMin = 15
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
    return NewValue

def newvalue2(OldValue, key):
    OldMax = 50
    OldMin = 15
    NewMax = 0.87
    NewMin = 0.26
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = round((((OldValue - OldMin) * NewRange) / OldRange) + NewMin, 2)
    length = len(key.strip())
    avg_len = NewValue
    spance_taken_in_x = round(avg_len / 26 * length, 2)
    return spance_taken_in_x

def to_sub(x):
    
    pos = ['f', 'i', 'j', 'l', 't']
    neg = ['m', 'w']
    count = 0
    for i in x:
        if i in pos:
            count -= 0.007
        elif i in neg:
            count += 0.01
    return count

def hhhh(x):
    return newvalue2(x['ulter_size'], x['word']) + 0.02 + to_sub(x['word'])

def getcumsum(data, x, y):
    if y == 'color':
        return data[data.word == x][y]
    else:
        return float(data[data.word == x][y])

def ad(x, add):
    try:
        suma = x['space_take'] + add[x['group']]
    except:
        suma = x['space_take']
    return suma

def  getvocab(link = 'nil', data = 'nil', from_data = False):
    if from_data:
        visible_text = data
    else:
      
        soup = bs(link)
        # visible_text = soup.getText()

        visible_text = (" ").join([i.text for i in soup.findAll('p')] + [i.text for i in soup.findAll('li')])

    text = re.sub('[&?!\"\"”)(“\©,-//|\n\t{[\]\:=;\r ]+'," ", visible_text)
    text = re.sub('[^a-zA-Z]', " ", text)
    text = re.sub('wg\w+', "", text)
    text = text.lower()
    text = re.sub('wiki\w+', "", text)
    text = re.findall('[a-z\-\'\"]+', text)
    text = [word for word in text if word.lower() not in STOPWORDS and len(word) != 1]

    vocab = {}
    for word in text:
        if word not in vocab.keys():
            vocab[word] = 1
        else:
            vocab[word] += 1

    vocab = sorted(vocab.items(), key = operator.itemgetter(1), reverse = True)[:50]
    vocab = {key:value for key,value in vocab}
    num = list(vocab.values())
    vocab = sorted(vocab.items())
    vocab = {key:value for key,value in vocab}


    return vocab,num 

def get_data(vocab, num):  
    data = pd.DataFrame([vocab], ).T.reset_index()
    data.columns = ['word', 'fref']
    data['ulter_size'] = [newvalue(i, num = num) for i in list(data.fref)]
    data['space_take'] = data.apply(lambda x: hhhh(x), axis = 1)
    initial_x = 0.0
    maxvalue = 0.95
    lastvalue = initial_x
    newcum = []
    group = []
    gg = 0
    group_sub = {}
    group_no = {}
    i = 0
    for row in data.itertuples():
        thisvalue =  row[4] + lastvalue
        if thisvalue > maxvalue:
            group_no[gg] = i
            i = 1
            group_sub[gg] = maxvalue - oldthisvalue
            gg += 1
            thisvalue = row[4]
            newcum.append( thisvalue )
            lastvalue = thisvalue
            group.append(gg)
            continue
        i += 1
        newcum.append( thisvalue )
        lastvalue = thisvalue
        group.append(gg)
        oldthisvalue = thisvalue
    group_no[gg] = i
    group_sub[gg] = maxvalue - oldthisvalue
    data['cumsum'] = newcum
    data['group'] = group
    add = {i:group_sub[i]/group_no[i]  for i in range(len(group_no))}
    del add[list(add.keys())[-1]]
    data['space_take_new'] = data.apply(lambda x: ad(x, add), axis = 1)
    maxvalue = 1
    lastvalue = initial_x
    newcumnew = []
    group = []
    gg = 0
    i = 0
    for row in data.itertuples():
        thisvalue =  row[7] + lastvalue
        if thisvalue > maxvalue:
            gg += 1
            thisvalue = row[7]
            newcumnew.append( thisvalue )
            lastvalue = thisvalue
            group.append(gg)
            continue
      # gg += 1
        newcumnew.append( thisvalue )
        lastvalue = thisvalue
        group.append(gg)
        oldthisvalue = thisvalue

    data['cumsum_new'] = newcumnew
    data['group_new'] = group
    data['color'] = data['ulter_size'].apply(lambda x: '#05ADD4'  if x < 25 else '#0486DA' if x < 35 else '#012273' if x < 45 else '#1F1741')
    return data




heading_color = ['#E1C559']
text_heading_color = ['#C1C5C7']##C1C5C7
text_color = ['#667175']
background_color = ["#EEF2F7"]

myown2_viz = html.Div([
     html.Div([
        html.Div([
            html.P([
                'Created by Abhinav, ', html.A('@abhinavk910,', href="https://twitter.com/abhinavk910", style={'color': heading_color[0]}),
                html.Span(" WordCloud from Website's Text", style={'font-size': '50px','color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'This visualization highlights',
                html.Span(' Frequent words ',
                          style={'color': heading_color[0]}),
                ' Occuring in a Document or a Website ',
                html.A('More Text Analysis...', href='https://nlp-app-production.up.railway.app/app/text_analysis', target="_blank", style={'color': heading_color[0]})
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'width': '1200px', 'min-height': '100px'}, className='pt-4 pl-4'),
   html.Div([
       dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
#                     dbc.Input(id="input", placeholder="Type something...", type="text"),
                    dbc.Textarea(id="input_myown2", className="mb-0", placeholder="Website address ex:-https://abhinavk910.github.io/ak.github.io/"),
                ],sm=12, lg=8),
                dbc.Col([
                    dbc.Button('Generate WordCloud', id='sub_myown2',color="primary",style={'width':'200px', 'height':'38px'}, className="mr-1"),
                ],sm=12, lg=4)
            ], className='mt-2 mb-1'),
            dbc.Row([
                dbc.Col([
                    dcc.Loading(
                                        id="loadingnew-1",
                                        type="default",
                                        children= html.Img(id='example_myown2', style={'width':'100%'}), # img element
                                    )
                   
                ], className='')
            ])
        ], sm=12, lg=10),
        dbc.Col([
            html.Div([
        dash_table.DataTable(
                        id='table-nlp-1',
                        columns=[{"name": i, "id": i, "selectable": True} for i in ['Word','Freq']],
                        page_size=11,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current= 0,
                        style_cell={'whiteSpace': 'normal','height': 'auto'},   
    )],id='table_hidden_nlp1',hidden=True)
        ], sm=12, lg=2,className='mt-2 mb-0')
    ], className='')
   ],  style={'background': 'rgb(25, 41, 48, 0.9)',
              "border-radius": "25px","box-shadow": "15px 0px 15px -10px rgba(0,0,0,0.75)"}, className='p-5 m-5'),
    html.Div([
        html.Div([
            html.P([
                'Created by ',html.A('Abhinav', href='http://www.linkedin.com/in/abhinavk910', style={'color': heading_color[0]}),
                html.A(' Kumar', href="https://twitter.com/abhinavk910", style={'color': heading_color[0]})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'Tool: ',
                html.Span('Plotly', style={'color': heading_color[0]}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className='')
    ], style={'background': '', 'min-height': '100px', "text-align": "center"}, className=''),

    
    
    
    
])



@app.callback(
    [Output('example_myown2', 'src'),Output('table-nlp-1', 'data'), Output('table_hidden_nlp1', 'hidden')],
    Input('sub_myown2', 'n_clicks'),
    [State('input_myown2','value')]
)
def update_figure(n_points, link):
    print(n_points)
    if n_points==None:
        link='https://abhinavk910.github.io/ak.github.io'
    plt.rcParams["font.family"] = "serif"
    plt.rcParams['figure.dpi'] = 200
    vocab, num = getvocab(link)
    data_vocab = get_data(vocab, num)
    initial_x = 0.00
    initial_y = 0.90
    y_step_down = 0.17
    buf = io.BytesIO() # in-memory files
    fig, ax = plt.subplots(1,1,figsize=(15, 5))
    background_color = '#e2e5d7'
    fig.patch.set_facecolor(background_color)
    spance_taken_in_x = initial_x
    old = 0 
    for key, value in vocab.items():
        new = getcumsum(data_vocab, key, 'cumsum_new')
        sizef = getcumsum(data_vocab, key, 'ulter_size')
        if new < old:
            spance_taken_in_x = initial_x
            initial_y -= y_step_down
        ax=plt.text(spance_taken_in_x, initial_y, key.strip(), size = sizef ,c = list(getcumsum(data_vocab, key, 'color'))[0],
                 ha = 'left', va = 'baseline', wrap = True)
        spance_taken_in_x = new
        old = new
    plt.axis('off')
    plt.savefig(buf, format = "png") # save to the above file object
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
    exp = data_vocab.iloc[:,:2]
    exp.columns = ['Word','Freq']
    exp.sort_values(by='Freq',ascending=False, inplace=True)
    return ["data:image/png;base64,{}".format(data), exp.to_dict('records'), False]

