
from dash import Dash, dcc, html, get_asset_url
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
           suppress_callback_exceptions=True)
app.title = 'FUKUJU'

sidebar = dbc.Row([
    html.Img(src=get_asset_url('fukujulogo512.png'),
             style={'width': '20%', 'height': 'auto', 'padding': '2%'}),  # 'aspect-ratio':'5/3'
    html.P('FUKUJU KOGYO', style={'font-size': '5vw'})
], align='center', style={'height': '10vh'}, className='bg-dark')

content = html.Div([])


app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(sidebar, width=3, className='bg-light',
                style={'height': '100vh'}),
        dbc.Col(content, width=9, style={'height': '100vh'})
    ]), fluid=True
)

if __name__ == '__main__':
    #app.run_server(port=2910, debug=True, use_reloader=True)
    app.run_server(host='0.0.0.0', port=2910, debug=False)
