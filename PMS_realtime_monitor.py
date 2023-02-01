import datetime
import pandas as pd
import numpy as np

from dash import Input, Output, callback
import plotly.graph_objects as go

##############################
# リアルタイムモニタ
##############################

start = pd.Timestamp(datetime.datetime.now()).round(
    's') - datetime.timedelta(seconds=300)

df_rt = []
for i in range(5):
    df_rt.append(pd.DataFrame(
        {'value': np.random.randn(10000).cumsum()},
        index=pd.date_range(start, freq='s', periods=10000)
    ))

layout_3 = dict(margin=dict(l=40, r=20, t=20, b=30),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                width=None,
                height=280,
                autosize=True,
                hovermode='x',
                xaxis=dict(spikemode='across',
                           spikedash='solid', spikethickness=1,
                           tickformat='%H:%M:%S'),
                )


def realtimemonitor(number):
    now = pd.Timestamp(datetime.datetime.now()).round('s')
    past = now - datetime.timedelta(seconds=120)
    plot_df = df_rt[number].loc[past:now]

    fig_scatter = go.Figure(
        data=go.Scatter(x=plot_df.index, y=plot_df['value']),
        layout=layout_3)

    title_scatter = f'リアルタイムモニタ_{number} : {now}',
    return title_scatter, fig_scatter


@callback(
    Output('title-3-1', 'children'),
    Output('graph-3-1', 'figure'),
    Input('interval-3-1', 'n_intervals')
)
def update_3_1(_):
    return realtimemonitor(0)


@callback(
    Output('title-3-2', 'children'),
    Output('graph-3-2', 'figure'),
    Input('interval-3-2', 'n_intervals')
)
def update_3_2(_):
    return realtimemonitor(1)


@callback(
    Output('title-3-3', 'children'),
    Output('graph-3-3', 'figure'),
    Input('interval-3-3', 'n_intervals')
)
def update_3_3(_):
    return realtimemonitor(2)


@callback(
    Output('title-3-4', 'children'),
    Output('graph-3-4', 'figure'),
    Input('interval-3-4', 'n_intervals')
)
def update_3_4(_):
    return realtimemonitor(3)
