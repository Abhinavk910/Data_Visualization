
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app




qty_cal_viz = html.Div(
    [
        html.H1('Quantity Calculator', className = 'mt-3 mb-1', style={'weight':'bold'}),
        html.Hr(),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Portfolio Budget:", style={'width':'150px'}),
                dbc.Input(placeholder="Amount",id='budget_s',value=100000, type="number"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Entry:", style={'width':'150px'}),
                dbc.Input(placeholder="Amount", id='entry_s',value=100, type="number"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Exit:", style={'width':'150px'}),
                dbc.Input(placeholder="Amount", id='exit_s',value=90, type="number"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Portfolio Loss:", style={'width':'150px'}),
                dbc.Input(placeholder="Amount", id='portfolio_loss_s',value=10, type="number"),
                dbc.InputGroupText("%"),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Profit %:", style={'width':'150px'}),
                dbc.Input(placeholder="Amount", id='entry_profit_s', value=5,type="number"),
                dbc.InputGroupText("%"),
            ],
            className="mb-3",
        ),
        html.Hr(),
        html.P(id='message'),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Investment", style={'width':'150px', 'color':'white',
                                                                                'background-color':'green'}),
                                        dbc.Input(placeholder="Amount", id='total_investment',type="number"),
                                    ],className="mb-3",
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Quantity", style={'width':'150px', 'color':'white',
                                                                                'background-color':'green'}),
                                        dbc.Input(placeholder="Amount", id='qty_stock',type="number"),
                                    ],className="mb-3",
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Point Gain", style={'width':'150px', 'color':'white',
                                                                                'background-color':'green'}),
                                        dbc.Input(placeholder="Amount", id='total_point_gain',type="number"),
                                    ],className="mb-3",
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Profit", style={'width':'150px', 'color':'white',
                                                                                'background-color':'green'}),
                                        dbc.Input(placeholder="Amount", id='total_gain',type="number"),
                                    ],className="mb-3",
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Portfolio Gain", style={'width':'150px', 'color':'white',
                                                                                'background-color':'green'}),
                                        dbc.Input(placeholder="Amount", id='portfolio_gain',type="number"),
                                        dbc.InputGroupText("%"),
                                    ],className="mb-3",
                                ),
                            ],lg=6,md=12
                        ),
                         dbc.Col(
                            [
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("StopLoss", style={'width':'150px', 'color':'white',
                                                                                'background-color':'red'}),
                                        dbc.Input(placeholder="Amount", id='stoploss_s',type="number"),
                                        dbc.InputGroupText("%"),
                                    ],className="mb-3",
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Point Loss", style={'width':'150px',  'color':'white',
                                                                                'background-color':'red'}),
                                        dbc.Input(placeholder="Amount", id='total_point_loss',type="number"),
                                    ],className="mb-3",
                                ),
                                dbc.InputGroup(
                                    [
                                        dbc.InputGroupText("Investment Loss", style={'width':'150px',  'color':'white',
                                                                                'background-color':'red'}),
                                        dbc.Input(placeholder="Amount", id='total_loss',type="number"),
                                    ],className="mb-3",
                                ),
                                
                            ],lg=6,md=12
                        ),
                    ]
                ),
            ]
        ),       
    ],className="mx-5", style = {'marn':'auto'}
)


@app.callback(
    [
        Output('stoploss_s', 'value'),
        Output('qty_stock', 'value'),
        Output('total_investment', 'value'),
        Output('total_point_loss', 'value'),
        Output('total_loss', 'value'),
        Output('total_point_gain', 'value'),
        Output('total_gain', 'value'),
        Output('portfolio_gain', 'value'),
        Output('message', 'children')
    ],
    [
        Input('budget_s', 'value'),
        Input('entry_s', 'value'),
        Input('exit_s', 'value'),
        Input('portfolio_loss_s', 'value'),
        Input('entry_profit_s', 'value')
    ]
)
def dd(budget, entry, exit, portfolio_loss, entry_profit):
    portfolio_loss = 0.01*portfolio_loss
    entry_profit = 0.01*entry_profit
    if exit < entry:
        stoploss = round((1-exit/entry),3)

        investment = (budget * portfolio_loss)/stoploss
        if investment > budget:
            qty = int(round(investment / entry, 0))
            total_invst = round(investment,2)
            message = 'Inverstment Exceed -- Either lower the exit point ie. incease stoploss or lower the portfolio risk'
            total_point_gain = 0
            total_gain = 0
            portfolio_gain = 0
        else:
            qty = int(round(investment / entry, 0))
            total_invst = round(investment,2)
            total_point_gain = round(entry * entry_profit, 2)
            total_gain = round(qty * total_point_gain,2)
            portfolio_gain = round((total_gain / budget)*100,2)
            message = ""

        total_point_loss = entry - exit
        total_loss = budget * portfolio_loss
    else:
        message = '!!! Please provide exit point below entry'
        qty = 0
        total_invst = 0
        total_point_gain = 0
        total_gain = 0
        portfolio_gain = 0
        stoploss = 0
        total_point_loss = 0
        total_loss = 0
        
    return [stoploss*100, qty, total_invst, total_point_loss,total_loss, total_point_gain, total_gain, portfolio_gain, message]