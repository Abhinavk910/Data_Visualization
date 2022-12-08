import re
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
# from wordcloud import WordCloud

def startsWithDateAndTime(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def FindAuthor(s):

    s=s.split(":")
    if len(s)==2:
        return True
    else:
        return False

def getDataPoint(line):
    splitLine = line.split(' - ')
    dateTime = splitLine[0]
    date, time = dateTime.split(', ')
    message = ' '.join(splitLine[1:])
    if FindAuthor(message):
        splitMessage = message.split(': ')
        author = splitMessage[0]
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message


def parse_data(chart_path):

    Data = []
    with open(chart_path, encoding="utf-8") as fp:
        fp.readline() # Skipping first line of the file because contains information related to something about end-to-end encryption
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if startsWithDateAndTime(line):
                if len(messageBuffer) != 0:
                    Data.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDataPoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)

    df = pd.DataFrame(Data, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.
    df["Date"] = pd.to_datetime(df["Date"])
    df["Time"] = df["Time"].str.strip()
    df["Time"] = pd.to_datetime(df["Time"])
    df["Time"] = df["Time"].apply(lambda x: x.time())
    df_2 = df[~df["Author"].isnull()].reset_index(drop=True)
    activity_df = df[df["Author"].isnull()]
    return df_2, activity_df

def basic_stats(df):
    total_messages = df.shape[0]
    number_of_days = (df["Date"].max() - df["Date"].min()).days + 1
    data = {
        'formed':  df["Date"].min().date(),
        'author': df["Author"].nunique(),
        'messages': total_messages,
        'total_days': number_of_days,
        'avg_message': round(total_messages/number_of_days, 2)
    }
    return data

def date_data(date_df):
    # enriching
    # print(date_df.info())


    ## 1. year
    date_df["year"] = date_df["Date"].apply(lambda x: x.year)

    ## 2. month
    date_df["month"] = date_df["Date"].apply(lambda x: x.strftime("%b"))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    date_df['month'] = pd.Categorical(date_df['month'], months)

    ## 3. week number
    date_df["week"] = date_df["Date"].apply(lambda x: x.strftime("%V"))

    ## 3. day_of_week
    date_df["day_of_week"] = date_df["Date"].apply(lambda x: x.strftime('%a'))
    day_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    date_df['day_of_week'] = pd.Categorical(date_df['day_of_week'], day_of_week)

    ##  4. day
    date_df['day'] = date_df["Date"].apply(lambda x: x.day)

    ## 5. hour
    try:
        date_df["hour"] = date_df["Time"].apply(lambda x: x.hour)
    except:
        date_df["Time"] = date_df["Time"].str.strip()
        date_df["Time"] = pd.to_datetime(date_df["Time"])
        date_df["Time"] = date_df["Time"].apply(lambda x: x.time())
        date_df["hour"] = date_df["Time"].apply(lambda x: x.hour)

    ## 3. part_of_day
    date_df["part_of_day"] = date_df["hour"].apply(lambda x: part_of_day(x))

    return date_df

def part_of_day(x):
    if (x > 4) and (x <= 8):
        return 'Early Morning'
    elif (x > 8) and (x <= 12 ):
        return 'Morning'
    elif (x > 12) and (x <= 16):
        return 'Noon'
    elif (x > 16) and (x <= 20) :
        return 'Eve'
    elif (x > 20) and (x <= 24):
        return'Night'
    elif (x <= 4):
        return'Late Night'

def talkativeness(percent_message, total_authors):
    mean = 100/total_authors
    threshold = mean*.25

    if (percent_message > (mean+threshold)):
        return ("Very talkative")
    elif (percent_message < (mean-threshold)):
        return ("Quiet, untalkative")
    else:
        return ("Moderately talkative")

def author_data(df):
    author_df = df["Author"].value_counts().reset_index()
    author_df.rename(columns={"index":"Author", "Author":"Number of messages"}, inplace=True)
    author_df["Total %"] = round(author_df["Number of messages"]*100/df.shape[0], 2)
    author_df["Talkativeness"] = author_df["Total %"].apply(lambda x: talkativeness(x, df["Author"].nunique()))
    return author_df

def author_date_date(t_author_df):
    # enriching
    ## 1. year
    t_author_df["year"] = t_author_df["Date"].apply(lambda x: x.year)
    ## 2. month
    t_author_df["month"] = t_author_df["Date"].apply(lambda x: x.strftime("%b"))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    t_author_df['month'] = pd.Categorical(t_author_df['month'], months)

    analysis_1_df = t_author_df.pivot_table(index=["month", "year"], columns=["Author"], values=["Message"], aggfunc="count", fill_value=0)
    analysis_1_df.columns = [col_[1] for col_ in analysis_1_df.columns]
    analysis_1_df = analysis_1_df.reset_index().sort_values(["year", "month"])
    analysis_1_df["month_year"] = analysis_1_df.apply(lambda x: x["month"] + " " + str(x["year"]), axis=1)
    analysis_1_df.drop(["month", "year"], axis=1, inplace=True)
    analysis_1_df.set_index('month_year',inplace=True)
    authors_list = analysis_1_df.sum().sort_values(ascending = False).index.to_list()


    if len(authors_list) > 3:
        value = authors_list[:3]
    else:
        value = authors_list

    return analysis_1_df, authors_list, value

# plotly
def update_fig(fig, xtitle, ytitle, toptitle, graph_height = 400, graph_width = 500, bot_margin = 100, left_margin = 80, right_margin = 80, top_margin = 20, x_standoff = 10):
    if toptitle!='None':
        annotations = []
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text=toptitle,
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
        fig.update_layout(annotations=annotations)
    fig.update_traces( marker_line_color='rgb(8,48,107)',
              marker_line_width=1.5, opacity=0.8)
    fig.update_layout(
    # width = graph_width,
    height = graph_height,
    xaxis=dict(
        automargin=True,
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
        title = dict(
            text = xtitle,
            font = dict(family='Arial',
                        size=15,
                        color='rgb(82, 82, 82)'),
            standoff = x_standoff
        )
    ),
    yaxis=dict(
        automargin=True,
        showgrid=True,
        gridcolor = "#f9f9f9",
        zeroline=True,
        showline=True,
        showticklabels=True,
        title = dict(
            text = ytitle,
            font = dict(family='Arial',
                        size=15,
                        color='rgb(82, 82, 82)'),
            standoff = 10
        )
    ),
    autosize=True,
    # margin=dict(
    #     autoexpand=False,
    #     l=left_margin,
    #     r=right_margin,
    #     t=top_margin,
    #     b= bot_margin
    # ),

    showlegend=False,
    # plot_bgcolor='white'
    plot_bgcolor = "LightSteelBlue"
    )
    return fig


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
