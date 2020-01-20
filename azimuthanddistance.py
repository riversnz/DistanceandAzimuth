import pyproj
import random
import sys
import math
import pandas as pd
from faker import Faker
geod = pyproj.Geod(ellps='WGS84')
faker = Faker()
faker.name()

df = []
df1 = []

for n in range(10):
    df.append({'Lat': faker.coordinate(center=74.0, radius=0.10),
               'Lon': faker.coordinate(center=40.8, radius=0.10),
               'Txt': faker.sentence(),
               'Nam': faker.name(),
               'Add': faker.address(),
               'Job': faker.job()
              })

df = pd.DataFrame(df)
df = df[['Nam', 'Job', 'Txt', 'Add', 'Lat', 'Lon']]

for n in range(10):
    df1.append({'Lat1': faker.coordinate(center=74.0, radius=0.10),
               'Lon1': faker.coordinate(center=40.8, radius=0.10),
               'Txt1': faker.sentence(),
               'Nam1': faker.name(),
               'Add1': faker.address(),
               'Job1': faker.job()
              })

df1 = pd.DataFrame(df1)
df1 = df1[['Nam1', 'Job1', 'Txt1', 'Add1', 'Lat1', 'Lon1']]

df['index_col'] = df.index
df1['index_col'] = df1.index

df_merge_col = pd.merge(df, df1, on='index_col')
df_merge_col['Lat1'] = df_merge_col['Lat1'].astype(float)
df_merge_col['Lon1'] = df_merge_col['Lon1'].astype(float)
df_merge_col['Lat'] = df_merge_col['Lat'].astype(float)
df_merge_col['Lon'] = df_merge_col['Lon'].astype(float)
df_merge_col = df_merge_col.iloc[1:]

def calcdist(x):

    return geod.inv(x['Lon1'], x['Lat1'], x['Lon'], x['Lat'])[2]

def azimuthcalc(x):    
    azimuth1 = geod.inv(x['Lon1'], x['Lat1'], x['Lon'], x['Lat'])[0]
    return azimuth1


df_merge_col['dist'] = df_merge_col.apply(calcdist, axis=1)
df_merge_col['azimuth1'] = df_merge_col.apply(azimuthcalc, axis=1)



print(df_merge_col['dist']) 
print(df_merge_col['azimuth1']) 

def towtogps(x):
   return x['azimuth1'].add(360)

df_merge_col['azimuth1'] = df_merge_col.loc[df_merge_col.azimuth1 < 0, 'azimuth1'] + 360

print(df_merge_col['azimuth1'])

df_merge_col.to_csv('testdist.csv')

