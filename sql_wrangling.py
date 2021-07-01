import psycopg2

import pandas as pd

def connect(sql_query):
    conn = psycopg2.connect(
        host="localhost",
        database="dbs_project",
        user="postgres",
        password="1234")

    return pd.read_sql_query(sql_query, con=conn)

def getcountries():
    df = connect("SELECT * FROM project.commoncountries")
    df.rename(columns={"countryname": "label", "countrycode":"value"},  inplace = True)
    
    #Welt, statt Countries auswählen
    df.loc[-1] = ["World", "WRD"]
    df.index = df.index + 1
    df = df.sort_index()

    return df.to_dict("records")


def get_df_for_button1():
    return connect(open("sql_queries/btn1_query.sql", "r").read())

def get_df_for_button2():
    return connect(open("sql_queries/btn2_query.sql", "r").read())

def get_df_for_button3():
    return connect(open("sql_queries/btn3_query.sql", "r").read())


def fix_df_rows(df):
    
    return df