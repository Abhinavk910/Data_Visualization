import pandas as pd
import dash
from dash import dcc, html,  Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objs as go
import pathlib
import numpy as np
from app import app
from dash.exceptions import PreventUpdate
import dash_canvas
from dash_canvas.components import image_upload_zone
from dash_canvas.utils import (image_with_contour, image_string_to_PILImage, array_to_data_url)
import json

import pytesseract
import cv2
import imutils
from skimage import io

import re
import requests
from bs4 import BeautifulSoup

def  clean_text(word):
    word = word.lower()
    word = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?!#$%&\'()*,-/:;<=>?@[\\]^_`{|}~", "", word)
    word = re.sub(r"\d+", "", word)
    return word

def bs(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
def get_text(sitelink):
    soup = bs(sitelink)
#     try:
#         heading = soup.find(class_="special-article-heading").text.strip()
#     except:
#         heading = soup.find(class_="title").text.strip()
    subheading = soup.find(class_="intro").text.strip()
    content = [subheading] +  [i.text.strip() for i in soup.find(class_="article").findAll('p')]
    final_text = "\n".join([i.strip() for i in content])
    return final_text

def get_indianexpress(sitelink):
    soup = bs(sitelink)
    heading = soup.find(class_="heading-part").find(class_="native_story_title").text
    synopsis = soup.find(class_="heading-part").find(class_="synopsis").text
    contents = soup.find(id="pcl-full-content").findAll('p')
    content = "\n".join([i.text for i in contents])
    return heading + "\n" + synopsis + "\n" + content

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../dictionary/').resolve()

filename = DATA_PATH.joinpath("world_famous.png")
img_app3 = io.imread(filename)
height, width= (300,300)
canvas_width = 500
canvas_height = round(height * canvas_width / width)
scale = canvas_width / width

dicti = pd.read_csv(DATA_PATH.joinpath('my_dictionary.csv'))

words = dicti.Word.unique().tolist()


def get_crop(objects, image):

    data = objects['objects'][1]
    x, y, w, h = int(data['left']), int(data['top']), int(data['width']), int(data['height'])
    data = objects['objects'][0]
    sx, sy = data['scaleX'], data['scaleY']
    x_s, y_s, w_s, h_s = int(x*(1/sx)), int(y*(1/sy)), int(w*(1/sx)), int(h*(1/sy))
    cropped = image[y_s:y_s+h_s, x_s:x_s+w_s]

    return cropped

def findtext(image):

    if len(image.shape) > 2 and image.shape[2] == 4:
        #convert the image from RGBA2RGB
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) > 2 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    thresh = cv2.threshold(gray, 0, 256, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    text = pytesseract.image_to_string(thresh)
    return text


def get_data(new_split):

    value_find = []
    for i in range(0,len(new_split)):
        if i%2 == 0:
            value_find.append(new_split[i] + " ")
        else:
            value_find.append(html.B(new_split[i]))
    return html.P(value_find)


modalbody = html.Div([
    dbc.Row([
                image_upload_zone('upload-image-bg')
            ],align="center", className = 'd-flex justify-content-center'),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dash_canvas.DashCanvas(id='canvas-bg',
                                   width=canvas_width,
                                   height=canvas_height,
                                   scale=scale,
                                   image_content=array_to_data_url(img_app3),
                                   goButtonTitle='Crop Image',
                                   hide_buttons=['line', 'zoom', 'pan', 'pencil', 'select'],
                                 ),
            dbc.Button("Extract Text from Image", color='primary', id="extract-dictionary", className="ml-auto"),
        ]),
        dbc.Col([
            dcc.Loading(id="loading-1",
                        type="default",
                        children=[html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line', 'color': 'white'})],
                )
        ])

        ],className = 'm-2 p-2 ', justify="around", style = {'backgroundColor': '#111111'}),
])


modal = html.Div(
    [
        dbc.Button("Get Text from Image", id="open-centered", className="m-1"),
        dbc.Modal(
            [
                dbc.ModalHeader("Text Extraction From Image", style={'textAlign': 'center'}),
                dbc.ModalBody([
                    modalbody
                ]),
                dbc.ModalFooter([
                    dbc.Button("Transfer to Text Area", color='primary', id="get-data-from-image", className="ml-2"),
                    dbc.Button("Close", color='primary', id="close-centered", className="ml-2"),

                ]),
            ],id="modal-centered",centered=True,size="xl"),
    ],
)


modal_from_hindu = html.Div(
    [
        dbc.Button("Get News from The Hindu", id="open-centered-hindu", className="m-1"),
        dbc.Modal(
            [
                dbc.ModalHeader("News form The Hindu", style={'textAlign': 'center'}),
                dbc.ModalBody([
                    html.P([
                      'Paste',
                      html.A(' The Hindu ', href = "https://www.thehindu.com/opinion/editorial/", target = "_blank"),
                      'link here :-'
                    ]),
                    dbc.Input(id="input-hindu", placeholder="Paste Link Here...", type="text"),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Extract News", color='primary', id="get-data-from-image-hindu", className="ml-auto"),
                    dbc.Toast(
                        [html.P("News Extracted", className="mb-0")],
                        id="auto-toast",
                        icon="primary",
                        duration=2000,
                    ),
                    dbc.Button("Close", color='primary', id="close-centered-hindu", className="ml-auto"),

                ]),
            ],id="modal-centered-hindu",centered=True,size="xl", scrollable=True),
    ],
)

modal_from_indianexpress = html.Div(
    [
        dbc.Button("Get News from Indian Express", id="open-centered-iex", className = 'm-1 '),
        dbc.Modal(
            [
                dbc.ModalHeader("News form Indian Express", style={'textAlign': 'center'}),
                dbc.ModalBody([
                    html.P([
                      'Paste',
                      html.A('Indian Express ', href = "https://indianexpress.com/section/opinion/editorials/", target = "_blank"),
                      'link here :-'
                    ]),
                    dbc.Input(id="input-iex", placeholder="Paste Link Here...", type="text"),
                ]),
                dbc.ModalFooter([
                    dbc.Button("Extract News", color='primary', id="get-data-from-image-iex", className="ml-auto"),
                    dbc.Toast(
                        [html.P("News Extracted", className="mb-0")],
                        id="auto-toast-iex",
                        icon="primary",
                        duration=2000,
                    ),
                    dbc.Button("Close", color='primary', id="close-centered-iex", className="ml-auto"),

                ]),
            ],id="modal-centered-iex",centered=True,size="xl", scrollable=True),
    ],
)



word_layout =  html.Div([
    dcc.Textarea(
        id='textarea-state-example',
        value="",
        style={'width': '100%', 'height': 200, 'font_size': "20px"},
    ),
    html.Div([
        dbc.Button("Primary",color="primary", id='textarea-state-example-button', n_clicks=0, className="mr-2"),
        dbc.Button('Clear', color='secondary', id='textarea-clear', n_clicks=0, className="mr-2"),
        modal,
        modal_from_hindu,
        modal_from_indianexpress
    ], className = 'd-flex m-1 p-1 flex-wrap'),
    html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),
#     modalbody
], className = 'm-2 p-2')



#################################################################################################################
@app.callback(Output('textarea-example-output', 'children'),
              [Input('extract-dictionary', 'n_clicks')],
              [State('canvas-bg', 'json_data'), State('canvas-bg', 'image_content')])
def update_figure_upload(click, string, image):
    if click:
        if string:
            if image is None:
                im = img_app3
            else:
                im = image_string_to_PILImage(image)
                im = np.asarray(im, dtype = np.uint8)

            text = findtext(im)
            return str(text)

        else:
            im = img_app3
            return str(findtext(im))
    else:
        raise PreventUpdate


@app.callback(Output('canvas-bg', 'image_content'),
              [Input('upload-image-bg', 'contents'),
             Input('canvas-bg', 'json_data')])
def update_canvas_upload(image_string, data):
    if image_string is None:
        raise PreventUpdate
    elif image_string is not None:
        if data is None:
            return image_string
        else:
            try:
                data = json.loads(data)
                im = image_string_to_PILImage(image_string)
                im = np.asarray(im)
                cropped = get_crop(data, im)
                return array_to_data_url(cropped)
            except Exception as ins:
                print(ins, 'fuck')
                return image_string


@app.callback(
    Output("modal-centered-iex", "is_open"),
    [Input("open-centered-iex", "n_clicks"), Input("close-centered-iex", "n_clicks")],
    [State("modal-centered-iex", "is_open")],
)
def toggle_modal2(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal-centered-hindu", "is_open"),
    [Input("open-centered-hindu", "n_clicks"), Input("close-centered-hindu", "n_clicks")],
    [State("modal-centered-hindu", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output('textarea-state-example', 'value'),Output("auto-toast", "is_open"),Output("auto-toast-iex", "is_open")],
    [Input('textarea-clear', 'n_clicks'),Input("get-data-from-image", "n_clicks"),
     Input("get-data-from-image-hindu", "n_clicks"), Input("get-data-from-image-iex", "n_clicks")],
    [State('textarea-example-output', 'children'), State('input-hindu', 'value'), State('input-iex', 'value')]

)
def update_output2(n_clicks2, n_click3, n_clicks4,n_clicks5, data, sitelink, sitelinkiex):

    ctx = dash.callback_context

    if not ctx.triggered:
        text = """The Delhi High Court on Thursday dismissed pleas by social media platforms, Facebook and WhatsApp, challenging India's competition regulator CCI's order directing a probe into WhatsApp's new privacy policy.
                    Justice Navin Chawla said though it would have been "prudent" for the Competition Commission of India (CCI) to await the outcome of petitions in the Supreme Court and the Delhi HC against WhatsApp's new privacy policy, but not doing so would not make the regulator's order "perverse" or "wanting of jurisdiction"."""
        return text, False, False
    else:
#         print(ctx)
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "textarea-clear":
        return "", False, False
    elif button_id == 'get-data-from-image-hindu':
        text = get_text(sitelink)
        return text, True, False
    elif button_id == 'get-data-from-image-iex':
        text = get_indianexpress(sitelinkiex)
        return text, False, True
    else:

        return data, False



@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('textarea-state-example-button', 'n_clicks'),
    State('textarea-state-example', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
#         value = ["Textarea content initialized", html.B('asfdf'), "with multiple lines of text"]
        finallist = []
        value = value.replace('"', " ")
        dd = value.split('\n')
        test_list = [i for i in dd if i]
        for test_list_small in test_list:
            test_word = test_list_small.split()
            new_list = []
            for word in test_word:
                strip = clean_text(word)
                if strip in words:
                    meaning = dicti[dicti.Word == strip].iloc[0,2]
                    new_list.append("$%" + word + " (" + meaning + ")$%")
                else:
                    new_list.append(word)
            new = " ".join(new_list)
            new_split = new.split('$%')
            values = get_data(new_split)
            finallist.append(values)

        return finallist
