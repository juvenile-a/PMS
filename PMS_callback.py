import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

from dash import Input, Output, dcc, html, callback, exceptions  # State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import PMS_helper


# グラフに'DRAFT'追加
import plotly.io as pio
pio.templates['draft'] = go.layout.Template(
    layout_annotations=[
        dict(
            name='draft watermark',
            text='DRAFT',
            textangle=-20,
            opacity=0.2,
            font=dict(color='black', size=100),
            xref='paper', yref='paper',
            x=0.45, y=0.9,
            showarrow=False,
        )])
pio.templates.default = 'plotly+draft'

##############################
# タブ
##############################


@callback(Output('tabs-content-example-graph', 'children'),
          Input('tabs-example-graph', 'active_tab'))
def render_content(tab):
    match tab:
        case 'tab-1-example-graph':
            return html.Div([
                html.H3('生産実績', id='title-1', style={'padding': '1%'}),
                dbc.Row([
                        dcc.Loading(id='loading-1', type='default',
                                    children=[dcc.Graph(id='graph-1', config=dict({'displaylogo': False}))]),
                        #dcc.Interval(id='interval-1', interval=1000*60)
                        ], className='bg-light', style={'margin-left': '1%', 'padding': '1%', 'height': '100%'}),
            ])
        case 'tab-2-example-graph':
            return html.Div([
                html.H3('不良集計', id='title-2', style={'padding': '1%'}),
                dbc.Row([
                    dbc.Col([
                        dcc.Loading(id='loading-2-1', type='default',
                            children=[dcc.Graph(id='graph-2-1', config=dict({'displaylogo': False}))])
                    ], className='bg-light', style={'padding': '1%'}, width=6),
                    dbc.Col([
                        dcc.Loading(id='loading-2-2', type='default',
                            children=[dcc.Graph(id='graph-2-2', config=dict({'displaylogo': False}))])
                    ], className='bg-light', style={'padding': '1%'}, width=6),
                ], className='bg-light', style={'margin-left': '1%', 'padding': '1%', 'height': '50vh'}),
                dbc.Row([
                        dcc.Loading(id='loading-2-3', type='default',
                                    children=[dcc.Graph(id='graph-2-3', config=dict({'displaylogo': False})),
                                              #dcc.RangeSlider(0, 10, value=[5, 15], id='slider-2')
                                              ]),
                        ], className='bg-light', style={'margin-left': '1%', 'padding': '1%', 'height': '30vh'}),
            ])
        case 'tab-3-example-graph':
            return html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P(id='title-3-1', style={'margin': '2%'}),
                        dcc.Graph(id='graph-3-1', className='bg-light',
                                  style={'margin': '2%'}, config=dict({'displaylogo': False})),
                        dcc.Interval(id='interval-3-1', interval=2000)
                    ]),
                    dbc.Col([
                        html.P(id='title-3-2', style={'margin': '2%'}),
                        dcc.Graph(id='graph-3-2', className='bg-light',
                                  style={'margin': '2%'}, config=dict({'displaylogo': False})),
                        dcc.Interval(id='interval-3-2', interval=1000)
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        html.P(id='title-3-3', style={'margin': '2%'}),
                        dcc.Graph(id='graph-3-3', className='bg-light',
                                  style={'margin': '2%'}, config=dict({'displaylogo': False})),
                        dcc.Interval(id='interval-3-3', interval=2000)
                    ]),
                    dbc.Col([
                        html.P(id='title-3-4', style={'margin': '2%'}),
                        dcc.Graph(id='graph-3-4', className='bg-light',
                                  style={'margin': '2%'}, config=dict({'displaylogo': False})),
                        dcc.Interval(id='interval-3-4', interval=1000)
                    ]),
                ])
            ])
        case _: html.P('No Data...')


##############################
# 生産実績
##############################

layout_1 = dict(margin=dict(l=40, r=20, t=20, b=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=800,
                width=None,
                autosize=True,
                hovermode='x unified',
                xaxis=dict(spikemode='across',
                           spikedash='solid', spikethickness=1),
                hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)',
                                font=dict(size=20),
                                bordercolor='rgba(0,0,0,0.25)'),
                showlegend=False,
                )
# グラフ内注釈
text = ['実績数', '実績線', '計画線', '稼働率']
x = ['2023-1-18', '2023-1-6', '2023-1-27', '2023-1-5']
y = [1000, 3000, 10000, 13000]
ax = [40, -40, 40, -40]
ay = [-40, -40, 40, 40]

add_annotation = go.Layout(annotations=[dict(
    text=text[i],
    x=x[i], y=y[i],
    xref='x', yref='y',
    showarrow=True,
    font=dict(size=20, color='#ffffff'),
    align='center',
    arrowhead=2, arrowsize=1, arrowwidth=2,
    arrowcolor='#636363',
    ax=ax[i], ay=ay[i],
    bordercolor='#c7c7c7',
    borderwidth=2, borderpad=4,
    bgcolor='#ff7f0e', opacity=0.8
)for i in range(len(text))])


@callback(
    Output('graph-1', 'figure'),
    Output('title-1', 'children'),
    Input('product-picker', 'value'),
    Input('radio-1', 'value'),
    #Input('interval-1', 'n_intervals'),
    Input('button-1', 'n_clicks')
)
def update_1(product, range, n_clicks):  # n_intervals,
    if product is None:
        raise exceptions.PreventUpdate
    PMS_helper.df_update()

    # df 整形
    def df_shaping(df):
        df_temp = df.copy()[df['product'] == product]
        # pandasで扱える日付型に変換（.str.replace('/', '-')でも可）
        df_temp['_date'] = pd.to_datetime(df_temp['_date'])
        df_temp = df_temp.set_index(
            df_temp['_date'])  # '_date'をインデックスにする（複製追加される）
        df_temp = df_temp.drop(columns='_date')  # 不要になった'_date'を削除
        df_temp = df_temp.sort_index()  # 日付の順が逆になっているとエラーとなる為、ソートする
        return df_temp

    df_results_temp = df_shaping(PMS_helper.df_results)  # df 生産実績準備
    df_plan_temp = df_shaping(PMS_helper.df_plan)  # df 生産計画準備

    def month_range(start, end):
        df_results_temp2 = df_results_temp.copy()[start: end]

        # df_results_temp4 = df_results_temp2.iloc[0:0]
        # for x in products:
        #     df_results_temp3 = df_results_temp2.copy(
        #     )[df_results_temp2['product'] == x].drop(columns='product')

        #     df_results_temp3 = df_results_temp3.merge(
        #         pd.DataFrame(pd.date_range(start='2022-12-1',
        #                      end=df_results_temp3.index.max()), columns=['_date']),
        #         how='right', left_index=True, right_on='_date',
        #     ).set_index('_date').fillna(0)  # 連続した日付のデータフレームを作成してマージする。欠損日補填。
        #     df_results_temp3['product'] = x

        #     df_results_temp3['r_quantity_cumsum'] = df_results_temp3['r_quantity'].cumsum(
        #     )
        #     df_results_temp4 = pd.concat(
        #         [df_results_temp4, df_results_temp3], sort=True)

        df_results_temp3 = df_results_temp2.copy().drop(columns='product')
        df_results_temp3 = df_results_temp3.merge(
            pd.DataFrame(pd.date_range(start=start,
                                       end=df_results_temp3.index.max()), columns=['_date']),
            how='right', left_index=True, right_on='_date',
        ).set_index('_date').fillna(0)  # 連続した日付のデータフレームを作成してマージする。欠損日補填。
        df_results_temp3['product'] = product
        df_results_temp3['r_quantity_cumsum'] = df_results_temp3['r_quantity'].cumsum(
        )

        df_results_temp3 = df_results_temp3.reset_index().merge(
            PMS_helper.df_ct, how='left').set_index('_date')  # CT追加

        df_results_temp3['rate'] = (df_results_temp3['r_quantity'] /
                                    ((3600/df_results_temp3['ct']) *
                                    df_results_temp3['hour'])).round(3)  # 稼働率

        # # fig_1 = px.line(df_results_temp3, x=df_results_temp3.index, y='r_quantity_cumsum',
        # #                color='product', hover_data=['rate'], barmode='group')

        # # 良品数累積

        # fig_1 = px.line(df_results_temp3, x=df_results_temp3.index, y='r_quantity_cumsum',
        #                 color='product', markers=True, hover_data=['rate'])
        # fig_1.update_xaxes(title_text=None, dtick='D1',
        #                    tickformat='%d\n%m')
        # fig_1.update_yaxes(
        #     range=[0, df_results_temp3['r_quantity_cumsum'].max()*1.05], title_text='quantity')
        # fig_1.update_layout(layout_1)

        df_plan_temp2 = df_plan_temp.copy()[start: end]

        # df_plan_temp4 = df_plan_temp2.iloc[0:0]
        # for x in products:
        #     df_plan_temp3 = df_plan_temp2.copy(
        #     )[df_plan_temp2['product'] == x].drop(columns='product')
        #     df_plan_temp3 = df_plan_temp3.merge(
        #         pd.DataFrame(pd.date_range(start='2022-12-1',
        #                      end='2022-12-31'), columns=['_date']),
        #         how='right', left_index=True, right_on='_date',
        #     ).set_index('_date').fillna(0)  # 連続した日付のデータフレームを作成してマージする。欠損日補填。
        #     df_plan_temp3['product'] = x
        #     df_plan_temp3['p_quantity_cumsum'] = df_plan_temp3['p_quantity'].cumsum(
        #     )
        #     df_plan_temp4 = pd.concat(
        #         [df_plan_temp4, df_plan_temp3], sort=True)

        df_plan_temp3 = df_plan_temp2.copy().drop(columns='product')
        df_plan_temp3 = df_plan_temp3.merge(
            pd.DataFrame(pd.date_range(start=start,
                                       end=end), columns=['_date']),
            how='right', left_index=True, right_on='_date',
        ).set_index('_date').fillna(0)  # 連続した日付のデータフレームを作成してマージする。欠損日補填。
        df_plan_temp3['product'] = product
        df_plan_temp3['p_quantity_cumsum'] = df_plan_temp3['p_quantity'].cumsum(
        )

        df_union = pd.merge(df_plan_temp3, df_results_temp3,
                            how='left', on=['_date', 'product'])  # , left_index=True

        # fig_1 = px.line(df_union, x=df_union.index, y=['p_quantity_cumsum', 'r_quantity_cumsum'],
        #                 hover_data=['rate'])

        fig_1 = make_subplots(specs=[[{'secondary_y': True}]])
        # 計画線
        fig_1.add_trace(go.Scatter(x=df_union.index,
                                   y=df_union['p_quantity_cumsum'],
                                   line_color=px.colors.qualitative.Plotly[0],
                                   name='計画線',
                                   opacity=0.5))
        # 実績線
        fig_1.add_trace(go.Scatter(x=df_union.index,
                                   y=df_union['r_quantity_cumsum'],
                                   mode='lines+markers',
                                   marker=dict(size=6, symbol='circle', line=dict(
                                       width=1, color='Grey')),
                                   line_color=px.colors.qualitative.Plotly[1],
                                   name='実績線'))
        # 計画線 管理範囲
        df_quantity_temp = df_union[[
            'p_quantity_cumsum', 'r_quantity_cumsum']].copy()
        df_quantity_temp['p_quantity_cumsum_upper'] = df_quantity_temp['p_quantity_cumsum']*1.05
        df_quantity_temp['p_quantity_cumsum_lower'] = df_quantity_temp['p_quantity_cumsum']*0.95
        fig_1.add_trace(go.Scatter(x=np.concatenate([df_union.index, df_union.index[::-1]]),
                                   y=pd.concat([df_quantity_temp['p_quantity_cumsum_upper'],
                                                df_quantity_temp['p_quantity_cumsum_lower'][::-1]]),
                                   line_color='rgba(0,0,0,0)',
                                   fill='toself',
                                   fillcolor='rgba(26,150,65,0.1)',
                                   hoverinfo='skip',))
        # 実績 管理範囲外
        df_quantity_upper_over = df_quantity_temp[df_quantity_temp['r_quantity_cumsum']
                                                  > df_quantity_temp['p_quantity_cumsum_upper']]
        df_quantity_lower_over = df_quantity_temp[df_quantity_temp['r_quantity_cumsum']
                                                  < df_quantity_temp['p_quantity_cumsum_lower']]
        fig_1.add_trace(go.Scatter(x=df_quantity_upper_over.index,
                                   y=df_quantity_upper_over['r_quantity_cumsum'],
                                   mode="markers",
                                   marker=dict(size=20, symbol='triangle-up-open', color='Orange',
                                               line=dict(width=2)),
                                   hoverinfo='skip',))
        fig_1.add_trace(go.Scatter(x=df_quantity_lower_over.index,
                                   y=df_quantity_lower_over['r_quantity_cumsum'],
                                   mode="markers",
                                   marker=dict(size=20, symbol='triangle-down-open', color='Orange',
                                               line=dict(width=2)),
                                   hoverinfo='skip',))

        # 実績数
        fig_1.add_trace(go.Bar(x=df_union.index,
                               y=df_union['r_quantity'],
                               marker_color=px.colors.qualitative.Plotly[2],
                               name='実績数'))
        # 稼働率
        fig_1.add_trace(go.Scatter(x=df_union.index,
                                   y=df_union['rate'],
                                   mode='lines+markers',
                                   marker=dict(size=6, symbol='diamond', line=dict(
                                       width=1, color='Grey')),
                                   connectgaps=True,
                                   line_color=px.colors.qualitative.Plotly[9],
                                   name='稼働率',),
                        secondary_y=True)
        # 稼働率 管理範囲
        df_rate_temp = df_union[['rate']].copy()
        df_rate_temp['rate_upper'] = 1.0
        df_rate_temp['rate_lower'] = 0.8
        fig_1.add_trace(go.Scatter(x=np.concatenate([df_rate_temp.index, df_rate_temp.index[::-1]]),
                                   y=pd.concat([df_rate_temp['rate_upper'],
                                                df_rate_temp['rate_lower'][::-1]]),
                                   line_color='rgba(0,0,0,0)',
                                   fill='toself',
                                   fillcolor='rgba(255,150,50,0.1)',
                                   hoverinfo='skip',),
                        secondary_y=True)
        # 稼働率 管理範囲外
        df_rate_upper_over = df_rate_temp[df_rate_temp['rate']
                                          > df_rate_temp['rate_upper']]
        df_rate_lower_over = df_rate_temp[df_rate_temp['rate']
                                          < df_rate_temp['rate_lower']]
        fig_1.add_trace(go.Scatter(x=df_rate_upper_over.index,
                                   y=df_rate_upper_over['rate'],
                                   mode="markers",
                                   marker=dict(size=20, symbol='triangle-up-open', color='Orange',
                                               line=dict(width=2)),
                                   hoverinfo='skip',),
                        secondary_y=True)
        fig_1.add_trace(go.Scatter(x=df_rate_lower_over.index,
                                   y=df_rate_lower_over['rate'],
                                   mode="markers",
                                   marker=dict(size=20, symbol='triangle-down-open', color='Orange',
                                               line=dict(width=2)),
                                   hoverinfo='skip',),
                        secondary_y=True)

        fig_1.update_xaxes(title_text=None, dtick='D',
                           tickformat='%d\n%m月')
        fig_1.update_xaxes(range=(datetime.datetime(start.year, start.month, start.day, 0, 0)+datetime.timedelta(days=-0.5),
                                  datetime.datetime(end.year, end.month, end.day, 0, 0)+datetime.timedelta(days=0.5)))
        # fig_1.update_xaxes(rangeslider_visible=True)
        fig_1.update_yaxes(title_text='quantity')
        fig_1.update_yaxes(
            range=[0, max(df_union['p_quantity_cumsum'].max(), df_union['r_quantity_cumsum'].max())*1.40])
        fig_1.update_yaxes(
            title_text='数量', title_font_size=20, tickformat=',.0f')
        fig_1.update_yaxes(title_text='稼働率', tickformat='.0%', range=(0, 1.01),
                           showgrid=False, secondary_y=True)
        fig_1.update_layout(layout_1)
        fig_1.update_layout(add_annotation)  # 注釈追加
        title_1 = f'生産実績 {start.month}月 : {product}'
        return fig_1, title_1

    match range:
        case 'all_range':
            # df_results_temp3 = df_results_temp.iloc[0:0]  # 空のデータフレームを作成
            # for x in vars_product:
            #     df_results_temp2 = df_results_temp.copy(
            #     )[df_results_temp['product'] == x].resample('MS').sum(numeric_only=True)  # 月単位で合計'M':月の最終日,'MS':月の初日 値が文字列のカラムは消える
            #     df_results_temp2['product'] = x  # 消えたカラムを追加
            #     df_results_temp3 = pd.concat(
            #         [df_results_temp3, df_results_temp2], sort=True)  # データフレーム結合

            df_results_temp2 = df_results_temp.copy().resample('MS').sum(
                numeric_only=True)  # 月単位で合計'M':月の最終日,'MS':月の初日 値が文字列のカラムは消える
            df_results_temp2['product'] = product  # 消えたカラムを追加

            # df_results_temp2 = pd.merge(
            #    df_results_temp2, df_ct, on='product').set_index('index')  # CT追加 この方法だとインデックス消滅
            df_results_temp2 = df_results_temp2.reset_index().merge(
                PMS_helper.df_ct, how='left').set_index('_date')  # CT追加

            df_results_temp2['rate'] = (df_results_temp2['r_quantity'] /
                                        ((3600/df_results_temp2['ct']) *
                                        df_results_temp2['hour'])*100).round(1)  # 稼働率

            fig_1 = px.area(df_results_temp2, x=df_results_temp2.index, y='r_quantity',
                            markers=True, hover_data=['rate'])
            # fig_1 = px.bar(df_results_temp2, x=df_results_temp2.index, y='r_quantity',
            #                hover_data={'_date': ('|%Y年%m月', df_results_temp2.index),
            #                            'rare': df_results_temp2['rate']})
            fig_1.update_xaxes(title_text=None,
                               dtick='M1', tickformat='%m月\n%Y年')  # tickvals=df_results_temp2.indexを設定しないとラベルがズレる→.resample('MS')で解消
            fig_1.update_xaxes(rangeslider_visible=True)
            fig_1.update_xaxes(
                range=(df_results_temp2.index.min(), df_results_temp2.index.max()))
            fig_1.update_xaxes(rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month',
                         stepmode='backward'),  # 1ヶ月
                    dict(count=6, label='6m', step='month',
                         stepmode='backward'),  # 半年
                    dict(count=1, label='YTD', step='year',
                         stepmode='todate'),  # 表示範囲の最新の日付まで、その年の年初から
                    dict(count=1, label='1y', step='year',
                         stepmode='backward'),  # 1年
                    dict(step='all')  # 全期間表示
                ])
            ), rangeselector_bgcolor='white',)
            fig_1.update_yaxes(
                range=[0, df_results_temp2['r_quantity'].max()*1.2], title_text='quantity')
            fig_1.update_layout(layout_1)
            title_1 = f'生産実績 全期間 : {product}'

            # df_results_temp2.copy().to_excel('results.xlsx')  # エクセルファイル出力
            return fig_1, title_1

        case 'current_month':
            today = datetime.date.today()
            month_start = today + relativedelta(day=1)
            month_end = today + relativedelta(months=+1, day=1, days=-1)
            return month_range(month_start, month_end)

        case 'last_month':
            today = datetime.date.today()
            month_start = today + relativedelta(months=-1, day=1)
            month_end = today + relativedelta(day=1, days=-1)
            return month_range(month_start, month_end)

        case _: pass
