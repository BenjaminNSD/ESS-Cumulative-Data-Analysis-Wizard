import pandas as pd
import numpy as np
import pprint
import os
import pyreadstat as pyr
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Define the working directory
work_dir = r'C:\Users\beb\Documents\Python_processing\final'
os.chdir(work_dir)

# define stylesheets and colors
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {'background': '#111111', 'text': '#7FDBFF'}
# style defaults
style_dict={'backgroundColor': colors['background'], 'textAlign': 'center', 'color': colors['text']}
# ------------------------------------------------------------------------------

# import data and restructure
df, meta = pyr.read_sav('ESS1-9e01_agg.sav',  user_missing=False, encoding = "utf-8")
# prepare and restructure data
mapping = {1:2002, 2:2004, 3:2006, 4:2008, 5:2010, 6:2012, 7:2014, 8:2016, 9:2018}
df['date']=df.essround.replace(mapping)
df['date']=df.date.astype(int)
mapping = {'AF':'AFG', 'AL':'ALB', 'DZ':'DZA', 'AS':'ASM', 'AD':'AND', 'AO':'AGO', 'AI':'AIA', 'AQ':'ATA', 'AG':'ATG', 'AR':'ARG', 'AM':'ARM', 'AW':'ABW', 'AU':'AUS', 'AT':'AUT', 'AZ':'AZE', 'BS':'BHS', 'BH':'BHR', 'BD':'BGD', 'BB':'BRB', 'BY':'BLR', 'BE':'BEL', 'BZ':'BLZ', 'BJ':'BEN', 'BM':'BMU', 'BT':'BTN', 'BO':'BOL', 'BQ':'BES', 'BA':'BIH', 'BW':'BWA', 'BV':'BVT', 'BR':'BRA', 'IO':'IOT', 'BN':'BRN', 'BG':'BGR', 'BF':'BFA', 'BI':'BDI', 'CV':'CPV', 'KH':'KHM', 'CM':'CMR', 'CA':'CAN', 'KY':'CYM', 'CF':'CAF', 'TD':'TCD', 'CL':'CHL', 'CN':'CHN', 'CX':'CXR', 'CC':'CCK', 'CO':'COL', 'KM':'COM', 'CD':'COD', 'CG':'COG', 'CK':'COK', 'CR':'CRI', 'HR':'HRV', 'CU':'CUB', 'CW':'CUW', 'CY':'CYP', 'CZ':'CZE', 'CI':'CIV', 'DK':'DNK', 'DJ':'DJI', 'DM':'DMA', 'DO':'DOM', 'EC':'ECU', 'EG':'EGY', 'SV':'SLV', 'GQ':'GNQ', 'ER':'ERI', 'EE':'EST', 'SZ':'SWZ', 'ET':'ETH', 'FK':'FLK', 'FO':'FRO', 'FJ':'FJI', 'FI':'FIN', 'FR':'FRA', 'GF':'GUF', 'PF':'PYF', 'TF':'ATF', 'GA':'GAB', 'GM':'GMB', 'GE':'GEO', 'DE':'DEU', 'GH':'GHA', 'GI':'GIB', 'GR':'GRC', 'GL':'GRL', 'GD':'GRD', 'GP':'GLP', 'GU':'GUM', 'GT':'GTM', 'GG':'GGY', 'GN':'GIN', 'GW':'GNB', 'GY':'GUY', 'HT':'HTI', 'HM':'HMD', 'VA':'VAT', 'HN':'HND', 'HK':'HKG', 'HU':'HUN', 'IS':'ISL', 'IN':'IND', 'ID':'IDN', 'IR':'IRN', 'IQ':'IRQ', 'IE':'IRL', 'IM':'IMN', 'IL':'ISR', 'IT':'ITA', 'JM':'JAM', 'JP':'JPN', 'JE':'JEY', 'JO':'JOR', 'KZ':'KAZ', 'KE':'KEN', 'KI':'KIR', 'KP':'PRK', 'KR':'KOR', 'KW':'KWT', 'KG':'KGZ', 'LA':'LAO', 'LV':'LVA', 'LB':'LBN', 'LS':'LSO', 'LR':'LBR', 'LY':'LBY', 'LI':'LIE', 'LT':'LTU', 'LU':'LUX', 'MO':'MAC', 'MG':'MDG', 'MW':'MWI', 'MY':'MYS', 'MV':'MDV', 'ML':'MLI', 'MT':'MLT', 'MH':'MHL', 'MQ':'MTQ', 'MR':'MRT', 'MU':'MUS', 'YT':'MYT', 'MX':'MEX', 'FM':'FSM', 'MD':'MDA', 'MC':'MCO', 'MN':'MNG', 'ME':'MNE', 'MS':'MSR', 'MA':'MAR', 'MZ':'MOZ', 'MM':'MMR', 'NA':'NAM', 'NR':'NRU', 'NP':'NPL', 'NL':'NLD', 'NC':'NCL', 'NZ':'NZL', 'NI':'NIC', 'NE':'NER', 'NG':'NGA', 'NU':'NIU', 'NF':'NFK', 'MP':'MNP', 'NO':'NOR', 'OM':'OMN', 'PK':'PAK', 'PW':'PLW', 'PS':'PSE', 'PA':'PAN', 'PG':'PNG', 'PY':'PRY', 'PE':'PER', 'PH':'PHL', 'PN':'PCN', 'PL':'POL', 'PT':'PRT', 'PR':'PRI', 'QA':'QAT', 'MK':'MKD', 'RO':'ROU', 'RU':'RUS', 'RW':'RWA', 'RE':'REU', 'BL':'BLM', 'SH':'SHN', 'KN':'KNA', 'LC':'LCA', 'MF':'MAF', 'PM':'SPM', 'VC':'VCT', 'WS':'WSM', 'SM':'SMR', 'ST':'STP', 'SA':'SAU', 'SN':'SEN', 'RS':'SRB', 'SC':'SYC', 'SL':'SLE', 'SG':'SGP', 'SX':'SXM', 'SK':'SVK', 'SI':'SVN', 'SB':'SLB', 'SO':'SOM', 'ZA':'ZAF', 'GS':'SGS', 'SS':'SSD', 'ES':'ESP', 'LK':'LKA', 'SD':'SDN', 'SR':'SUR', 'SJ':'SJM', 'SE':'SWE', 'CH':'CHE', 'SY':'SYR', 'TW':'TWN', 'TJ':'TJK', 'TZ':'TZA', 'TH':'THA', 'TL':'TLS', 'TG':'TGO', 'TK':'TKL', 'TO':'TON', 'TT':'TTO', 'TN':'TUN', 'TR':'TUR', 'TM':'TKM', 'TC':'TCA', 'TV':'TUV', 'UG':'UGA', 'UA':'UKR', 'AE':'ARE', 'GB':'GBR', 'UM':'UMI', 'US':'USA', 'UY':'URY', 'UZ':'UZB', 'VU':'VUT', 'VE':'VEN', 'VN':'VNM', 'VG':'VGB', 'VI':'VIR', 'WF':'WLF', 'EH':'ESH', 'YE':'YEM', 'ZM':'ZMB', 'ZW':'ZWE', 'AX':'ALA'}
df['iso3166']=df.cntry.replace(mapping)
df=df.round(2)

# create lists with variable labels to be used in Dash graphs
dict_col=meta.column_names_to_labels
# remove redundant variables from label list
for key in ['cntry', 'cseqno', 'essround', 'idno', 'dweight', 'pspwght', 'pweight', 'anweight', 'cname', 'cedition', 'cproddat', 'name', 'edition']:
    dict_col.pop(key, None)
list_of_dict = [{'label': key+': '+ value, 'value': key} for key, value in dict_col.items()]
# create lists with value labels to be used in graphs
list_of_dict2 = []
def update_list(var):
    val_lab = meta.variable_value_labels[var]
    list_of_dict2 = [{'label': str(int(key)) + ' '+ value, 'value': key, 'disabled': True} for key, value in val_lab.items()]
    return list_of_dict2
# ------------------------------------------------------------------------------
# define text to be used in Dash
markdown_text = '''
### ESS Cumulative Data Analysis Wizard ###
This is my first interactive dashboard using Dash! Hope you like it. Creator: [Benjamin_Beuster](mailto:benjamin.beuster@gmail.com)
'''
markdown_text2 = '''
##### European Social Survey Cumulative File, ESS 1-9 (2020). #####
Data file edition 1.0. NSD - Norwegian Centre for Research Data, Norway - Data Archive and distributor of ESS data for ESS ERIC.
[doi:10.21338/NSD-ESS-CUMULATIVE](https://www.europeansocialsurvey.org/downloadwizard/)
'''
config={'showAxisDragHandles'==False}
# create the default figure for Dash
fig = px.line(df, x="date", y=df.index, color="cntry",
              hover_name="cntry", line_group="cntry",
        line_shape="spline", render_mode="svg", title='',
                   range_x =[2002, 2018]).update_traces(mode='lines+markers')
fig.update_xaxes(tick0=2002, dtick=2, title='')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    autosize=True, dragmode=False
)
# Create Dash layout
app.layout = html.Div([
    dcc.Markdown(children=markdown_text, style=style_dict),
    html.Div([
        html.Div([
            dcc.Dropdown(id='dropdown_vars', options=list_of_dict,
                         style={'width': '100%', 'margin-left': 0},
                         placeholder='Select a variable')], className="six columns"),
        html.Div([
            dcc.Dropdown(id='dropdown_labs', style={'width': '100%', 'margin-left': '0px', 'display': 'inline-block'},
                         placeholder='Show value labels')], className="six columns"),
    ], className="row"),
    dcc.Graph(id='ess_bar', figure=fig, style={'height': '80vh'},
              config= {'displaylogo': False, 'modeBarButtonsToRemove':['zoom2d', 'lasso2d', 'hoverClosestGl2d',
                'hoverCompareCartesian', 'toggleSpikelines', 'select2d', 'hoverClosestCartesian', 'hoverClosestGeo']}),
    dcc.RadioItems(id='radio', options=[{'label': 'Line', 'value': 'Line'}, {'label': 'Bar', 'value': 'Bar'},
                                        {'label': 'Map', 'value': 'Map'}], value='Line',
                  labelStyle={'display': 'inline-block'}),
    dcc.Markdown(children=markdown_text2, style=style_dict)],
        style = {'margin':'auto','width': "75%"})


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    dash.dependencies.Output(component_id='dropdown_labs', component_property='options'),
    [Input(component_id='dropdown_vars', component_property='value')]
)
def update_date_dropdown(name):
    try:
        return update_list(name)
    except:
        return [{'label': 'No labels found', 'value': 'test', 'disabled': True}]

@app.callback(
    Output('ess_bar', 'figure'),
    Input('dropdown_vars', 'value'),
    Input('radio', 'value'))

def update_graph(option_slctd, gtype):
    # Plotly Express
    if gtype=='Line':
        fig = px.line(df, x="date", y=option_slctd, color="cntry",
                  hover_name="cntry", line_group="iso3166",
                  line_shape="spline", render_mode="svg",
                  range_x=[2002, 2018]).update_traces(mode='lines+markers')
        fig.update_xaxes(tick0=2002, dtick=2, title='')
        try:
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                autosize=True, dragmode=False,
                title={'text': dict_col[option_slctd] + ' (MEAN / WEIGHTED)'})
        except:
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                autosize=True, dragmode=False,
                title={'text': 'Select a variable'})
        return fig
    elif gtype=='Bar':
        fig = px.bar(df, x="cntry", y=option_slctd, color='cntry', animation_frame='date', hover_name='cntry',
                       orientation='v', title='')
        try:
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                autosize=True, dragmode=False,
                title={'text': dict_col[option_slctd] + ' (MEAN / WEIGHTED)'})
        except:
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                autosize=True, dragmode=False,
                title={'text': 'Select a variable'})
        return fig
    elif gtype=='Map':
        fig = px.choropleth(df,
                            locations="iso3166",
                            color=option_slctd,
                            hover_name="cntry",
                            color_continuous_scale='viridis',
                            scope="europe", projection='eckert4',
                            animation_frame="date")
        try:
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                autosize=True, dragmode=False,
                title={'text': dict_col[option_slctd] + ' (MEAN / WEIGHTED)'})
        except:
            fig.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                autosize=True, dragmode=False,
                title={'text': 'Select a variable'})
        return fig
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
