import pandas as pd

#df = pd.read_csv("population_growth.csv")
df = pd.read_csv('gdp.csv')

i = 0
data_new = pd.DataFrame(columns = ['Country Name','Country Code','Indicator Name','Indicator Code','Year'])

index = 0
while index < 264:
    row = df.loc[index]
    gdp = row[4:66]
    country = row[0]
    code = row[1]
    iname = row[2]
    icode = row[3]

    y = 1960
    for x in gdp:
        data_new.loc[i]=([country,code,iname,icode,y])
        i += 1
        y += 1
    index += 1
data_new.to_csv("newgdp.csv",index = 0)

