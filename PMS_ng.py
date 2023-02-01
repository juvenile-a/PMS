import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

from dash import Input, Output, dcc, html, callback, exceptions
import plotly.express as px

import PMS_helper

##############################
# 不良集計
##############################

# product = ['AAA', 'BBB', 'AAA', 'BBB', 'AAA', 'AAA', 'AAA',
#            'AAA', 'AAA', 'BBB', 'AAA', 'BBB', 'AAA', 'AAA', 'AAA', 'AAA']
# process = ['OP-1', 'OP-1', 'OP-2', 'OP-2', 'OP-3', 'OP-4', 'OP-4',
#            'OP-4', 'OP-1', 'OP-1', 'OP-2', 'OP-2', 'OP-3', 'OP-4', 'OP-4', 'OP-4']
# categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
#               'H', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# count = [8, 3, 2, 4, 1, 4, 5, 1, 8, 3, 2, 4, 1, 4, 5, 1]
# df_ng = pd.DataFrame(
#     dict(product=product, process=process, categories=categories, count=count))

# df_ng.to_json('data/ng_sample.json') # JSON形式で出力

# df_ng = df_ng.groupby(['categories']).sum()
# df_ng = df_ng.sort_values('count', ascending=False)

# df_ng = pd.read_json('data/ng_sample.json')

layout_2 = dict(margin=dict(l=40, r=20, t=20, b=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                autosize=True,
                hoverlabel=dict(bgcolor='white')
                )


@callback(
    Output('graph-2-1', 'figure'),
    Output('graph-2-2', 'figure'),
    Output('graph-2-3', 'figure'),
    Output('title-2', 'children'),
    Input('product-picker', 'value'),
    Input('radio-1', 'value'),
)
def update_2(product, range):
    if product is None:
        raise exceptions.PreventUpdate  # コールバック処理を停止

    PMS_helper.df_update_ng()

    # df 整形
    def df_shaping(df):
        df_temp = df.copy()[df['product'] == product].drop(columns='product')
        # pandasで扱える日付型に変換（.str.replace('/', '-')でも可）
        df_temp['_date'] = pd.to_datetime(df_temp['_date'])
        df_temp = df_temp.groupby(
            ['_date', 'process', 'categories'], as_index=False).sum()
        df_temp = df_temp.set_index(
            df_temp['_date'])  # '_date'をインデックスにする（複製追加される）
        df_temp = df_temp.drop(columns='_date')  # 不要になった'_date'を削除
        df_temp = df_temp.sort_index()  # 日付の順が逆になっているとエラーとなる為、ソートする
        return df_temp

    df_ng_temp = df_shaping(PMS_helper.df_ng)  # df NG準備

    def month_range(start, end):
        df_ng_temp_month = df_ng_temp.copy()[start: end]

        df_ng_temp_1 = df_ng_temp_month.copy().drop(
            columns='process').reset_index(drop=True)
        df_ng_temp_1 = df_ng_temp_1.groupby(
            ['categories'], as_index=False).sum()
        df_ng_temp_1 = df_ng_temp_1.sort_values(
            by='count', ascending=False)
        fig_1 = px.bar(df_ng_temp_1, x='categories', y='count')
        fig_1.update_layout(layout_2)

        fig_2 = px.sunburst(df_ng_temp_month, path=['process', 'categories'],
                            values='count')
        fig_2.update_layout(layout_2)
        fig_2.update_traces(marker=dict(line=dict(color='white', width=1)))

        df_ng_temp_3 = df_ng_temp_month.copy().resample('D').sum(numeric_only=True)
        fig_3 = px.bar(df_ng_temp_3, x=df_ng_temp_3.index, y='count')
        fig_3.update_layout(layout_2)
        fig_3.update_layout(height=200)
        fig_3.update_xaxes(title_text=None, dtick='D',
                           tickformat='%d\n%m月')

        title_2 = f'不良集計 {start.month}月 : {product}'
        return fig_1, fig_2, fig_3, title_2

    match range:
        case 'all_range':
            df_ng_temp_1 = df_ng_temp.copy()
            df_ng_temp_1 = df_ng_temp_1.drop(
                columns='process').reset_index(drop=True)
            df_ng_temp_1 = df_ng_temp_1.groupby(
                ['categories'], as_index=False).sum()
            df_ng_temp_1 = df_ng_temp_1.sort_values(
                by='count', ascending=False)
            fig_1 = px.bar(df_ng_temp_1, x='categories', y='count')
            fig_1.update_layout(layout_2)

            fig_2 = px.sunburst(df_ng_temp, path=['process', 'categories'],
                                values='count')
            fig_2.update_layout(layout_2)
            fig_2.update_traces(marker=dict(line=dict(color='white', width=1)))

            df_ng_temp_3 = df_ng_temp.copy().resample('MS').sum(numeric_only=True)
            fig_3 = px.bar(df_ng_temp_3, x=df_ng_temp_3.index, y='count')
            fig_3.update_layout(layout_2)
            fig_3.update_layout(height=200)
            fig_3.update_xaxes(title_text=None, dtick='M1',
                               tickformat='%m月\n%Y年')

            # numdate = df_ng_temp.index.unique().astype(np.int64)
            # slider_min = numdate[0]
            # slider_max = numdate[-1]
            # slider_value = [numdate[0], numdate[-1]]
            # slider_marks = {numd: date.strftime(
            #     '%d/%m') for numd, date in zip(numdate, df_ng_temp.index.unique())}

            title_2 = f'不良集計 : {product}'
            return fig_1, fig_2, fig_3, title_2

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
