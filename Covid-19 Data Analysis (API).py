#!/usr/bin/env python
# coding: utf-8

# ![image.png](attachment:image.png)

# # Analysis of Covid-19 Data
# 
# The data is collected from 232 countries across 6 continents. The data has 16 attributes related to covid-19. Not all attributes are used in data analysis due to its low significance and shall check the level of presence of null value and decide whether to drop any attributes. The data is collected starting from March, 2020 to Jan 3,2021.
# The data is used from API available at rapidAPI.

# In[1]:


# importing libraries
import plotly
import plotly.express as px
import plotly.graph_objects as go
import chart_studio.plotly as py
import cufflinks as cf
from plotly.offline import iplot, init_notebook_mode
#--------------------------------------------#

import pandas as pd
import numpy as np
import seaborn as sns
import requests

import json

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt

# option for pandas to display the columns
pd.options.display.max_columns=30

# setting the notebook mode for plotly

init_notebook_mode(connected=True)
cf.go_offline(connected=True)

# setting theme in cufflinks

cf.set_config_file(theme="pearl")


# In[2]:




url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-key': "7f8c50217bmshc6db892348f515bp11c9d6jsnf3cbacf03a02",
    'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers)

print(response)


# In[3]:


data = json.loads(response.content.decode())


# In[4]:


data


# In[5]:


df = pd.json_normalize(data['response'])


# In[6]:


df


# In[7]:


df['country'].nunique()


# In[8]:


df['continent'].unique()


# In[9]:


df.shape


# In[10]:


df.columns


# Columns Needed

# In[11]:


columns_ = ['continent', 'country', 'cases.active','cases.critical','cases.recovered','cases.new',
       'cases.1M_pop',
       'cases.total', 'deaths.new', 'deaths.1M_pop', 'deaths.total',
       'tests.1M_pop', 'tests.total']


# In[12]:


df1 = df[columns_]


# In[13]:


df1


# # Data Cleaning

# In[14]:


#Dropping the null value
df1.dropna(inplace = True)


# In[15]:


df1


# In[16]:


df1.info()


# In[17]:


df1.describe()


# In[18]:


df1.describe(include = ['object'])


# In[19]:


# Correlation
def color(x):
    if x>0.8:
        color ='blue'
    else:
        color ='black'
    return 'color:%s'%color


# In[20]:


#correlation
df1.corr().style.applymap(color)


# Since all the attributes are directly related to  Covid-19, Correlation between all the elements are generally high.

# In[21]:


corr=df1.corr()


# In[22]:


import plotly.figure_factory as ff


# In[23]:


fig=ff.create_annotated_heatmap(z=corr.values,
                           x=list(corr.columns),
                           y=list(corr.index),
                           annotation_text=corr.round(2).values,
                           showscale=True,
                               colorscale='Earth',)
fig.layout.margin=dict(l=200,t=200)
fig.layout.height=800
fig.layout.width=1000
iplot(fig)


# # Tidying the Dataset

# Analyzing the data set accordance to categorical variable with other attributes

# In[24]:


# Attributes accordance to Continent
df1.groupby(["continent"]).mean().iplot(kind='bar', yTitle="no of count",
                    xTitle="continent",
                    linecolor="white",
                    title="Total count of  accidents based on infrastructure by state ", theme='pearl',
            )


# From the figure, we can see that Europe has done the most testing of corona virus but has the moderate number of deaths. If we compare the graph with  the population size of the continent, it would not be wrong to say that the continent with high number of testing tend to show the high number of cases and deaths. Asia being the largest continent and constitutes more than half of the world population has very low number of testing thus resulting in low number of death related to corona. Low number of testing  in highest population size ultimately results in huge loss of actual data and create difficulty in interpreting  the actual scenario. Africa being the continent with second highest population, it has low number in all paramaters. It may be due to lack of resources.

# In[25]:


# Total cases and deaths accordance to country
df1.groupby(["country"])[['cases.total', 'deaths.total']].sum().iplot(kind='bar')


# US and Brazil has the highest number of cases followed by Russia, France, Tunisia and Italy.

# In[26]:


from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


# In[27]:


# Attributes accordance to countries
data_by_country = df1.groupby('country')[['cases.active','cases.critical','cases.recovered','cases.total','deaths.total','tests.total']].sum()


# In[28]:


chart = data_by_country.T


# In[29]:


def data_country(country):
    fig = chart[country].iplot(kind = 'bar',
                             layout = dict(
                             title = 'Covid Data by country  ' ))


# In[30]:


interact(data_country, country = chart.columns)


# The figure above shows that US, Brazil, Russia, France and Italy are the countries with high number in most of the attributes where US is leading with high margin compared to other countries in cases, test count and deeath wise.

# In[66]:


c = df1.groupby('country')['cases.total'].sum()


# In[67]:


a = c.reset_index()


# In[68]:


import plotly.express as px
data = dict(type = "choropleth",
          
           locations = a["country"],
            z = a["cases.total"],
            text = a['country'],
            marker = dict(line = dict(color = "rgb(255,255,255)", width = 2)),
            locationmode = "country names",
            colorbar = {"title": " Total Cases"}
           )


# In[69]:


layout = dict(title = "Covid-19",
             geo = dict(scope = "world",
                         showframe = False,
                         showlakes = True,
                        
            
                      lakecolor = "rgb(85,173,240)"))


# In[70]:


choromap = go.Figure(data =[data], layout = layout)


# In[71]:


iplot(choromap)


# # Conclusion

# From the Data we analyzed, we see a pattern that Developed Countries have tested most and also have the high number of covid cases and death counts. It would be wrong to believe that the developing countries have lower number of covid related case. More testing should be available in developing countries and countries with high population in order to get the real picture of effect of corona virus on global level. And not to forget, accurate data helps to track and prevent virus from spreading 

# In[ ]:




