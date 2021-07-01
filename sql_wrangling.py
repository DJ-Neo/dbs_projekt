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

# Einfluss BIP auf erneuerbare Energien
def get_df_for_button1(): #country_code, zeit_min, zeit_max, bip_min, bip_max, ernEn_min, ernEn_max
    
    sql_query = open("sql_queries/btn1_test.sql", "r")
    return connect(sql_query.read())

