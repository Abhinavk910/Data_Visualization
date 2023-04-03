
import dash
from dash import dcc, html,  Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import  index_page
from apps.whatsapp_chat_analysis import app3
from apps.indian_refinery import app4
from apps.Viz_for_social_good.ffl_dashboard import app6
from apps.Viz_for_social_good.vavv import app7
from apps.Makeover_Mondays.Week_15_NBA_Fouls import app8
from apps.Makeover_Mondays.Week_16_US_Aeroplane_Passengers import app9
from apps.WorkOut_Wednesday.Week_16_avg_sales import app10
from apps.WorkOut_Wednesday.Week_16_superstore_lolipop import app11
from apps.dictionary import app12
from apps.WorkOut_Wednesday.Week_15_Website_Analytics import app13
from apps.Makeover_Mondays.Week_17_usa_price_parity import app14
from apps.sports_viz_sunday_lacrosse import app15
from apps.WorkOut_Wednesday.Week_17_US_Population import app16
from apps.Makeover_Mondays.Week_18_Ceos_compensation import app17
from apps.Viz_for_social_good.FGM_tanzania import app18
from apps.WorkOut_Wednesday.Week_14_Financial_dashboard import app19
from apps.Makeover_Mondays.Week_19_1gb_data_price import app20
from apps.Makeover_Mondays.Week_20_beat_animal_unarmed_dumbbell_plot import app21
from apps.Makeover_Mondays.Week_22_sup_contribution import app22
from apps.Makeover_Mondays.Week_21_wildlife_population_changing import app23
from apps.Makeover_Mondays.Week_23_Never_married_onthe_rise import app24
from apps.Makeover_Mondays.Week_24_Usa_university_very_expensive import app25
from apps.My_Own.NFHS import app26
from apps.Makeover_Mondays.Week_25_Stop_and_Search_UK import app27
from apps.Makeover_Mondays.Week_26_Birthday_usa import app28
from apps.Makeover_Mondays.year_2020.Week_13_pizza_topping_uk import app29
from apps.Makeover_Mondays.Week_27_What_if import app30
from apps.Makeover_Mondays.Week_32_mortality_rate_uk import app32
from apps.Makeover_Mondays.Week_34_entry_level_job_uk import app34
from apps.My_Own.wordcloud import app35
from apps.Makeover_Mondays.Week_36_abortion_usa import app36
from apps.My_Own.qty_cal import app37
from apps.Viz_for_social_good.Video_volunteer import app38
from apps.Makeover_Mondays.year_2023.Week_10_germany_meat_production import app39
from apps.Makeover_Mondays.year_2023.Week_13_gender_pay_gap import app40

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/whatsapp_chat_analysis':
        return app3.whatsapp_layout
    if pathname == '/apps/indian_refinery':
        return app4.refinery_layout
    if pathname == '/apps/ffl_dashboard':
        return app6.ffl_dashboard_layout
    if pathname == '/apps/vavv':
        return app7.vavv_layout
    if pathname == '/apps/NBA_Fouls':
        return app8.nba_layout
    if pathname == '/apps/covid_vs_us_air_travel':
        return app9.us_plane_layout
    if pathname == '/apps/week_16_workout_wednesday':
        return app10.week_16_wiz
    if pathname == '/apps/week_16_workout_wednesday2':
        return app11.week_16_wiz2
    if pathname == '/apps/ready_to_read':
        return app12.word_layout
    if pathname == '/apps/website_analytic':
        return app13.week_15_wiz
    elif pathname == '/apps/usa_state_price_parity':
        return app14.mmw17_wiz
    elif pathname == '/apps/sports_viz_sunday_lacrosse':
        return app15.sm4_wiz
    elif pathname == '/apps/us_population':
        return app16.www17_wiz
    elif pathname == "/apps/ceo_compensation":
        return app17.mmw18_wiz
    elif pathname == '/apps/crowd2map_tanzania':
        return app18.vfsg_tanzania
    elif pathname == '/apps/financial_dashboard':
        return app19.www14_wiz
    elif pathname == "/apps/1gb_data_price":
        return app20.mmw19_wiz
    elif pathname == '/apps/human_vs_beast':
        return app21.mmw20_wiz
    elif pathname == "/apps/sup_contributor":
        return app22.mmw22_viz
    elif pathname == '/apps/2020gli':
        return app23.mmw21_viz
    elif pathname == '/apps/nm_rising':
        return app24.mmw23_viz
    elif pathname == "/apps/usa_uni_loan":
        return app25.mmw24_viz
    elif pathname == '/apps/nfhs5':
        return app26.NFHS_VIZ
    elif pathname == '/apps/sands_uk':
        return app27.mmw25_viz
    elif pathname == '/apps/usa_birthday':
        return app28.mmw26_viz
    elif pathname == '/apps/pizza_topping_uk':
        return app29.mmw13_viz_2020
    elif pathname == '/apps/usa_what_if_votes':
        return app30.mmw27_viz
    elif pathname == '/apps/uk_monthly_mortality_rate':
        return app32.mmw32_viz
    elif pathname == '/apps/uk_entry_level_job_exp':
        return app34.mmw34_viz
    elif pathname == '/apps/wordcloud':
        return app35.myown2_viz
    elif pathname == '/apps/usa_abortion':
        return app36.mmw36_viz
    elif pathname == '/apps/qty_cal':
        return app37.qty_cal_viz
    elif pathname == '/apps/VideoVolunteers':
        return app38.vv_layout
    elif pathname == '/apps/germany_mean_production':
        return app39.mmw10_2023_layout
    elif pathname == '/apps/gender_pay_gap':
        return app39.mmw13_2023_layout
    else:
        return index_page.layout



if __name__ == '__main__':
    app.run_server(debug=False, port=5500,)
