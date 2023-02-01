import pandas as pd
import tempfile

from dash import Input, Output, dcc, callback, exceptions

import PMS_helper

##############################
# ファイル出力
##############################


@callback(
    Output('download-file', 'data'),
    Input('dialog', 'submit_n_clicks')
)
def file_output(submit_n_clicks):
    if submit_n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = 'PMS'
            with pd.ExcelWriter(f'{tmpdir}/{filename}.xlsx') as writer:
                PMS_helper.df_results.to_excel(
                    writer, sheet_name='results')
                PMS_helper.df_plan.to_excel(
                    writer, sheet_name='plan')
                PMS_helper.df_CT.to_excel(
                    writer, sheet_name='CT')
            return dcc.send_file(f'{tmpdir}/{filename}.xlsx')
