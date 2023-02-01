import sqlite3
import pandas as pd

##############################
# データ取得
##############################


def df_product_init():
    global vars_product
    with sqlite3.connect('data/demo.sqlite3') as conn:
        df_results = pd.read_sql_query('SELECT * FROM results', conn)
    vars_product = df_results['product'].unique()


def df_update():
    global df_plan, df_results, df_ct, vars_product
    with sqlite3.connect('data/demo.sqlite3') as conn:
        df_plan = pd.read_sql_query('SELECT * FROM plan', conn)
        df_results = pd.read_sql_query('SELECT * FROM results', conn)
        df_ct = pd.read_sql_query('SELECT * FROM ct', conn)
    vars_product = df_results['product'].unique()
    # conn = sqlite3.connect('data/demo.sqlite3')
    # df_plan = pd.read_sql_query('SELECT * FROM plan', conn)
    # df_results = pd.read_sql_query('SELECT * FROM results', conn)
    # df_ct = pd.read_sql_query('SELECT * FROM ct', conn)
    # vars_product = df_results['product'].unique()
    # conn.close()


def df_update_ng():
    global df_ng
    with sqlite3.connect('data/demo.sqlite3') as conn:
        df_ng = pd.read_sql_query('SELECT * FROM ng', conn)
