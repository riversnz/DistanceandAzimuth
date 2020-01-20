import pyproj
import random
import sys
import math
import pandas as pd
from faker import Faker
# Importing done, check if any are not needed.
# setting the projection to WGS84.
geod = pyproj.Geod(ellps='WGS84')

# Starts a Faker instance for creating some lat long data to work with.
faker = Faker()
faker.name()

# Sets up some dataframes for later, do i need to do this?
df = []
df1 = []

# create two random test data sets for combining later. this also adds the data to the dataframe.
for n in range(10):
    df.append({'Lat': faker.coordinate(center=74.0, radius=0.10),
               'Lon': faker.coordinate(center=40.8, radius=0.10),
               'Txt': faker.sentence(),
               'Nam': faker.name(),
               'Add': faker.address(),
               'Job': faker.job()
              })
# dataframe and assign the headers/column names.
df = pd.DataFrame(df)
df = df[['Nam', 'Job', 'Txt', 'Add', 'Lat', 'Lon']]

# same as above just the second dataframe.
for n in range(10):
    df1.append({'Lat1': faker.coordinate(center=74.0, radius=0.10),
               'Lon1': faker.coordinate(center=40.8, radius=0.10),
               'Txt1': faker.sentence(),
               'Nam1': faker.name(),
               'Add1': faker.address(),
               'Job1': faker.job()
              })

# dataframe and assign the headers/column names.
df1 = pd.DataFrame(df1)
df1 = df1[['Nam1', 'Job1', 'Txt1', 'Add1', 'Lat1', 'Lon1']]

# assigns a index for merging the two dfs soon. think i could just use the index rather than assigning it.
df['index_col'] = df.index
df1['index_col'] = df1.index

# merge two dfs on index col
df_merge_col = pd.merge(df, df1, on='index_col')

# changed lat lons from objects to float. will have to test if this needs to be done.
df_merge_col['Lat1'] = df_merge_col['Lat1'].astype(float)
df_merge_col['Lon1'] = df_merge_col['Lon1'].astype(float)
df_merge_col['Lat'] = df_merge_col['Lat'].astype(float)
df_merge_col['Lon'] = df_merge_col['Lon'].astype(float)


# by calling the 2 result from Geod.inv it give the distance from one set of lat lon to the other.
def calcdist(x):

    return geod.inv(x['Lon1'], x['Lat1'], x['Lon'], x['Lat'])[2]
# by calling the 0 result from Geod.inv it give the fwd azimuth from one set of lat lon to the other.
# the 1 result would give the back bering or azimuth if needed 
def azimuthcalc(x):    
    azimuth1 = geod.inv(x['Lon1'], x['Lat1'], x['Lon'], x['Lat'])[0]
    return azimuth1

# applys the above function to two new cols. 
df_merge_col['dist'] = df_merge_col.apply(calcdist, axis=1)
df_merge_col['azimuth1'] = df_merge_col.apply(azimuthcalc, axis=1)

# below still needs to be sorted 
print(df_merge_col['dist']) 
print(df_merge_col['azimuth1']) 

def towtogps(x):
   return x['azimuth1'].add(360)

df_merge_col['azimuth1'] = df_merge_col.loc[df_merge_col.azimuth1 < 0, 'azimuth1'] + 360

print(df_merge_col['azimuth1'])

df_merge_col.to_csv('testdist.csv')

