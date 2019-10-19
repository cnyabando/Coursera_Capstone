#!/usr/bin/env python
# coding: utf-8

# # Exploration of Memphis and Nashville Barbecue Venues

# # By 
# # C. J. Nyabando

#  
# The purpose of this project is to explore barbecue (BBQ) options in Memphis vs Nashville, Tennessee. Memphis is known for having great BBQ. There is even an annual BBQ festival held in May that attracts teams from all over the world. Is there an opportunity to popularize BBQ in Nashville in a similar manner? Memphis in May has been a great benefit for Memphis and the state of Tennessee. Is there an opportunity to bring a similar event to Nashville in the Fall to maximize the benefits for the state? The assumption of this exploratory study is that if there are as many BBQ restaurants in downtown Nashville as in downtown Memphis, there is a potential for introducing a comparable BBQ festival/completion in Nashville.
# 
# 

# In[2]:


import requests # library to handle requests
import pandas as pd # library for data analysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation


# In[3]:


get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# In[4]:


#Foursquare
CLIENT_ID = 'RGRGLZYY5GHF02UV52UKU2BWBQMOBQB3HD2NY24R3PRQCMC3' # my Foursquare ID
CLIENT_SECRET = 'YLJLRSD2O0OWUZ5ZLCHRIB1JVJFUHAAYXQCGZUNCZKGRVBHJ' # my Foursquare Secret
VERSION = '20191014' #this is a date
LIMIT = 30
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[18]:


bbq = pd.DataFrame()
address = [ 'Memphis, TN', 'Nashville, TN']
for city in address:
    #define a user_agent in order to define an instance of the geocoder
    geolocator = Nominatim(user_agent="foursquare_agent")
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude
    
    print(city, latitude, longitude)
    
    #Search for BBQ venues for each city
    search_query = ['BBQ','Barbeque']
    radius = 5000   
    url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
    # get results in json
    results = requests.get(url).json()
    # assign relevant part of JSON to venues
    venues = results['response']['venues']
    # tranform venues into a dataframe
    dataframe = json_normalize(venues)
    bbq= bbq.append(dataframe, sort=False)
bbq = bbq.reset_index(drop=True)
bbq.head()

bbq.shape


# In[6]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in bbq.columns if col.startswith('location.')] + ['id']
bbq_filtered = pd.DataFrame(bbq, columns=filtered_columns)

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
bbq_filtered['categories'] = bbq_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
bbq_filtered.columns = [column.split('.')[-1] for column in bbq_filtered.columns]

bbq_filtered.head()

bbq_filtered.shape


# In[7]:


#Count of restaurants by city and category
bbq_count = bbq_filtered.groupby(['city','categories']).id.count()
bbq_count


# In[42]:


#create Nashville BBQ joints map

#filter Nashville BBQ joints
nash_bbq = bbq_filtered.loc[(bbq_filtered['city']=='Nashville')&(bbq_filtered['categories']=='BBQ Joint')]

#Nashville geocoordinates
latitude = 36.1622296
longitude = -86.7743531

map_nashbbq = folium.Map(location=[latitude, longitude], zoom_start=12)

# add markers to map
for lat, lng, label in zip(nash_bbq['lat'], nash_bbq['lng'], nash_bbq['name']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='green',
        #fill=True,
        ##fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_nashbbq)  
    
map_nashbbq


# In[43]:


#create memphis BBQ joints map

#filter Memphis BBQ joints
memphis_bbq = bbq_filtered.loc[(bbq_filtered['city']=='Memphis')&(bbq_filtered['categories']=='BBQ Joint')]

#Memphis coordinates
latitude = 35.1490215
longitude = -90.0516285

map_membbq = folium.Map(location=[latitude, longitude], zoom_start=12)

# add markers to map
for lat, lng, label in zip(memphis_bbq['lat'], memphis_bbq['lng'], memphis_bbq['name']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='green',
        #fill=True,
        ##fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_membbq)  
    
map_membbq


# In[16]:


ids = bbq_filtered[['id']]
ids.head()


# In[44]:


#get data for each venue including ratings
for venue_id in ids ['id']:
    print (venue_id)
    #search for data for each venue using venue ID 
    url = 'https://api.foursquare.com/v2/venues/{}?client_id={}&client_secret={}&v={}'.format(venue_id,CLIENT_ID, CLIENT_SECRET,VERSION)
    # get results in json
    results = requests.get(url).json()
    try:
       print(result['response']['venue']['rating'])
    except:
       print('This venue has not been rated yet.')


# In[ ]:




