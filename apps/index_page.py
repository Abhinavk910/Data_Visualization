import dash_core_components as dcc
import dash_html_components as html



layout = html.Div([
    
    
    html.Div([
        html.Div([
            html.P([
                'PORTFOLIO'],
                style={'font-size': '30px','color': '#E1C559'}, className='m-1'),
        ], className='')
    ], style={'background': '', 'min-height': '50px', "text-align": "center"}, className=''),
    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    html.H2('Data Collection and Visualization', className='mt-1 mb-1'),
    
    dcc.Link("WordCloud from a website", href='/apps/wordcloud'),
    html.Br(),
    dcc.Link('National Family Health Survey (NFHS-5) 2019-20', href='/apps/nfhs5'),
    html.Br(),
    dcc.Link('New way to read', href='/apps/ready_to_read'),
    html.Br(),
    dcc.Link('Indian Refinery Dashboard', href='/apps/indian_refinery'),
    html.Br(),
    # dcc.Link('WhatsApp chat analysis', href='/apps/whatsapp_chat_analysis'),
    # html.Br(),


    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    html.H2('MakeOver Monday', className='mt-1 mb-1'),
    dcc.Link('Makeover Monday Week 13 Gender Pay Gap in Sports', href='/apps/gender_pay_gap'),
    html.Br(),
    dcc.Link('Makeover Monday Week 10 Germany Meat Production Declined', href='/apps/germany_meat_production'),
    html.Br(),
    dcc.Link('Makeover Monday Week 36 Abortion in usa', href='/apps/usa_abortion'),
    html.Br(),
    dcc.Link('Makeover Monday Week 34 Entry Level Job Experience', href='/apps/uk_entry_level_job_exp'),
    html.Br(),
    dcc.Link('Makeover Monday Week 32 UK Monthly Mortality Rate', href='/apps/uk_monthly_mortality_rate'),
    html.Br(),
    dcc.Link('Makeover Monday Week 27 What if __ Votes?', href='/apps/usa_what_if_votes'),
    html.Br(),
    dcc.Link('Makeover Monday Week 26 how popular your birthday', href='/apps/usa_birthday'),
    html.Br(),
    dcc.Link('Makeover Monday Week 25 Stop and Search in UK', href='/apps/sands_uk'),
    html.Br(),
    dcc.Link('Makeover Monday Week 24 University Originated Loan', href='/apps/usa_uni_loan'),
    html.Br(),
    dcc.Link('Makeover Monday Week 23 Never Married on the RISE', href='/apps/nm_rising'),
    html.Br(),
    dcc.Link('Makeover Monday Week 22 SUP contributors', href='/apps/sup_contributor'),
    html.Br(),
    dcc.Link('Makeover Monday Week 21 2020 Global Living Index', href='/apps/2020gli'),
    html.Br(),
    dcc.Link('Makeover Monday Week 20 Human vs Beast', href='/apps/human_vs_beast'),
    html.Br(),
    dcc.Link('Makeover Monday Week 19 1GB Data cost in World', href='/apps/1gb_data_price'),
    html.Br(),
    dcc.Link('Makeover Monday Week 18 CEOs Compensation', href='/apps/ceo_compensation'),
    html.Br(),
    dcc.Link('Makeover Monday Week 17 USA States Price Parity', href='/apps/usa_state_price_parity'),
    html.Br(),
    dcc.Link('Makeover Monday Week 16 Covid hit US Aircraft', href='/apps/covid_vs_us_air_travel'),
    html.Br(),
    dcc.Link('Makeover Monday Week 15 NBA Fouls', href='/apps/NBA_Fouls'),
    html.Br(),
    dcc.Link('2020, Makeover Monday Week 13 Pizza Topping in UK', href='/apps/pizza_topping_uk'),
    html.Br(),

    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    html.H2('WorkOut Wednesday', className='mt-1 mb-1'),
    dcc.Link('Workout Wednesday Week 17 US Population(2019)', href='/apps/us_population'),
    html.Br(),
    dcc.Link('Workout Wednesday Week 16 Wednesday wiz challenge Tableau', href='/apps/week_16_workout_wednesday'),
    html.Br(),
    dcc.Link('Workout Wednesday Week 15 Wednesday Workout Website Analytic', href='/apps/website_analytic'),
    html.Br(),
    dcc.Link('Workout Wednesday Week 14 Financial Dashboard', href='/apps/financial_dashboard'),
    html.Br(),


    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    html.H2('Viz for social Good', className='mt-1 mb-1'),
    dcc.Link('Video_volunteer(NGO) Dashboard', href='/apps/VideoVolunteers'),
    html.Br(),
    dcc.Link('CROWD2MAP TANZANIA', href='/apps/crowd2map_tanzania'),
    html.Br(),
    dcc.Link('Vera Aqua Vera Vita', href='/apps/vavv'),
    html.Br(),
    dcc.Link('FFL(NGO) Dashboard', href='/apps/ffl_dashboard'),
    html.Br(),

    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    html.H2('Sports Viz', className='mt-1 mb-1'),
    dcc.Link('Sports Viz Sunday Division 1 Lacrosse', href='/apps/sports_viz_sunday_lacrosse'),
    html.Br(),
    html.Hr(style = {'background': '', 'width': "100%"}, className='mt-1 mb-1 p-0'),
    html.Div([
        html.Div([
            html.P([
                'Created by ',html.A('Abhinav', href='http://www.linkedin.com/in/abhinavk910', style={'color': '#E1C559'}),
                html.A(' Kumar', href="https://twitter.com/abhinavk910", style={'color': '#E1C559'})],
                style={'color': "#BBBBBA"}, className='m-0'),
            html.P([
                'Tool: ',
                html.Span('Dash', style={'color': '#E1C559'}),
            ], style={'color': "#BBBBBA"}, className='m-0')
        ], className=''),
    
    dcc.Link('qty_cal', href='/apps/qty_cal', style={'color':'transparent'}),    
    ], style={'background': '', 'min-height': '50px', "text-align": "center"}, className=''),
], className = 'm-3')
    