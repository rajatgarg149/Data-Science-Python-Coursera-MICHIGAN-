
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[101]:

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')


# In[102]:

df.sort(['Date', 'ID'], inplace=True)
df.shape


# In[103]:

df.replace('\d{4}\-02\-29', '', inplace=True, regex=True)


# In[104]:

df = df[df['Date'] != '']


# In[105]:

df['Month Date'] = df.Date.apply(lambda x: x[5:])
df['Year'] = df.Date.apply(lambda x: x[:4])


# In[154]:

df_2014 = df[df['Year'] != '2015']
df_2015 = df[df['Year'] == '2015']


# In[155]:

df_min = df_2014[df_2014['Element'] == 'TMIN']
df_max = df_2014[df_2014['Element'] == 'TMAX']
df_min = df_min.groupby('Month Date').agg({'Data_Value' : np.min})
df_max = df_max.groupby('Month Date').agg({'Data_Value' : np.max})


# In[157]:

import numpy as np


# In[166]:

min_2015 = df_2015[df_2015['Element'] == 'TMIN'].groupby('Month Date').agg({'Data_Value' : np.min})
max_2015 = df_2015[df_2015['Element'] == 'TMAX'].groupby('Month Date').agg({'Data_Value' : np.max})


# In[170]:

record_min = np.where(min_2015['Data_Value'] < df_min['Data_Value'])
record_max = np.where(max_2015['Data_Value'] > df_max['Data_Value'])


# In[217]:

plt.figure(figsize = (20,9))
plt.scatter(record_min, min_2015.iloc[record_min]['Data_Value'], marker='o', c='brown', label='Record Low')
plt.scatter(record_max, max_2015.iloc[record_max]['Data_Value'], marker='o', c='black', label='Record High')
plt.plot(df_min.values, 'b', label='Temp(min)')
plt.plot(df_max.values, 'r', label='Temp(max)')
plt.ylim([-600, 600])
plt.gca().fill_between(range(len(df_min)), df_min['Data_Value'], df_max['Data_Value'], facecolor='yellow')
plt.xticks(range(0, len(df_min), 30), df_min[::30].index, rotation='45')
plt.xlabel('Month-Date of a Year')
plt.ylabel('Temparature (in degrees Celsius)')
plt.legend()
plt.title('Ann Arbor Month-Date Temp')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()


# In[ ]:



