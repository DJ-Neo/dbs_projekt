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

def get_df_for_init():
    return connect(open("sql_queries/init_query.sql", "r").read())


#ToDo: Reihen fixen, wegen Verbindung letzter und erster Punkt

def mask_df_gdp(df, bip, ernEnergie, per_capita):
    
    bip_min, bip_max = bip
    ernEn_min, ernEn_max = ernEnergie

    if per_capita:
        factor_for_bip = 100
    else: factor_for_bip = 1000000000
    
    if per_capita:
        filter_by_bip = (df["gdp_per_capita"] >= bip_min) & (df["gdp_per_capita"] < bip_max*factor_for_bip)  
    else: filter_by_bip = (df["gdp"] >= bip_min) & (df["gdp"] < bip_max*factor_for_bip) 
    filter_by_ernEn = (df["perc_renen"] >= ernEn_min) & (df["perc_renen"] < ernEn_max)
    
    rslt_df = df[filter_by_ernEn & filter_by_bip] #filter_by_year &
    
    return rslt_df

def mask_df_emi(df, emission, ernEnergie):
    
    emission_min, emission_max = emission
    ernEn_min, ernEn_max = ernEnergie

    factor_for_emi = 1e6
    
    filter_by_emission = (df["annualemissions"] >= emission_min) & (df["annualemissions"] < emission_max*factor_for_emi)
    filter_by_ernEn = (df["perc_renen"] >= ernEn_min) & (df["perc_renen"] < ernEn_max)
    
    rslt_df = df[filter_by_emission & filter_by_ernEn] #filter_by_year & 
    
    return rslt_df
