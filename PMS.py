#from waitress import serve
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

import PMS_callback
import PMS_ng
import PMS_file_output
import PMS_helper
import PMS_realtime_monitor
import PMS_view

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
           suppress_callback_exceptions=True)
app.title = 'FUKUJU'

PMS_helper.df_product_init()

sidebar = html.Div([
    # dbc.Row(style={'height': '1vh'}),
    # dbc.Row(
    #    html.H4([html.Img(src=app.get_asset_url('fukujulogo512.png'),
    #                      style={'max-width': '30%', 'max-height': '70%', 'margin': '3.0%'}), 'FUKUJU NYUGYO'],
    #            style={'max-width': '100%', 'height': '8vh'})
    # ),
    dbc.Row([
            dbc.Col(
                html.Img(src=app.get_asset_url('fukujulogo512.png'),
                         style={'max-width': '90%', 'max-height': '90%'}
                         ), width=3,
            ),
            dbc.Col(html.H4('FUKUJU KOGYO', style={
                    'margin': '2.0%'}), width=9,),
            ], align='center', className='g-0', style={'max-width': '100%', 'height': '8vh'}),
    dbc.Row(
        dbc.Col(
            html.H4('選択項目'),
            width={'size': 10, 'offset': 1}),
        style={'height': '5vh'},
        className='bg-dark text-white',  # className='bg-primary text-white',
        align='end',
    ),
    # dbc.Row(
    #    style={'height': '1vh'},
    #    className='bg-dark',  # className='bg-primary',
    # ),
    dbc.Row([
            dbc.Col(
                html.H5('品名', style={'margin': '5.0%'}),
                width={'size': 10, 'offset': 1},
                align='end'),
            dbc.Col(
                dcc.Dropdown(id='product-picker', multi=False, value=PMS_helper.vars_product[0],  # value=None
                             options=[{'label': x, 'value': x}
                                      for x in PMS_helper.vars_product],
                             ),
                width={'size': 10, 'offset': 1}),
            ], style={'height': '10vh'}),
    dbc.Row([
            dbc.Col(
                html.H5('範囲', style={'margin': '5.0%'}),
                width={'size': 10, 'offset': 1},
                align='end'),
            dbc.Col(
                dbc.RadioItems(
                    id='radio-1',
                    options=[{'label': ' 全期間', 'value': 'all_range'},
                             {'label': ' 当月', 'value': 'current_month'},
                             # 'disabled': True
                             {'label': ' 先月', 'value': 'last_month'},
                             ], value='current_month'),
                width={'size': 10, 'offset': 1}),
            ], style={'height': '15vh'}),
    dbc.Row(style={'height': '20vh'}),
    dbc.Row([
            dbc.Col(
                dbc.Button('更新', id='button-1', color='secondary'),
                width={'size': 10, 'offset': 1}),
            ], style={'height': '5vh'}),
    dbc.Row([
            dbc.Col([
                dcc.ConfirmDialogProvider(
                    dbc.Button('ファイル出力', id='button-2', color='secondary'),
                    id='dialog', message='ファイルをダウンロードしますか？'),
                dcc.Download(id='download-file'),
            ], width={'size': 10, 'offset': 1}),
            ], style={'height': '5vh'}),
    dbc.Row(style={'height': '5vh'}),
    dbc.Row(
        dbc.Col(html.Div(id='view-0', style={'width': '100%', 'height': '100%'}),
                ), style={'height': '25vh'}),
])


content = html.Div([
    dbc.Row(
        html.H2(['Production Management System  ',
                 dbc.Badge('DEMO', color='warning')]),
        # className='bg-secondary',
        style={'width': '100%', 'height': '6vh', 'padding': '1.0%'},
    ),
    dbc.Row(
        dbc.Tabs(
            [
                dbc.Tab(label='生産実績', tab_id='tab-1-example-graph'),
                dbc.Tab(label='不良集計', tab_id='tab-2-example-graph'),
                dbc.Tab(label='リアルタイムモニタ', tab_id='tab-3-example-graph'),
            ],
            id='tabs-example-graph',
            active_tab='tab-1-example-graph',
        ),
        style={'width': '100%', 'height': '6vh', 'padding': '1.0%'},
        align='end',
    ),
    dbc.Row(
        html.Div(id='tabs-content-example-graph'),
        style={'width': '100%', 'height': '88vh', 'padding': '0.5%', },
    )
])


app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(sidebar, width=2, className='bg-light',
                style={'height': '100vh'}),
        dbc.Col(content, width=10, style={'height': '100vh'})
    ]), fluid=True
)

if __name__ == '__main__':
    app.run_server(port=2910, debug=True, use_reloader=True)
    # bindingを0.0.0.0にすることで全てのユーザーからのアクセスを許可
    # app.run_server(host='192.168.1.10') # 192.168.1.10 からのアクセスのみ許可
    # app.run_server(debug=True)
    # app.run_server(host='0.0.0.0', port=2910, debug=False)
    # serve(app.server, host='0.0.0.0', port=2910)  # 本番環境(waitress)
