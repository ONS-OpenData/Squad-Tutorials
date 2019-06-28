#!/usr/bin/env python
# coding: utf-8

# ### Messy Data
# #### In this note book you learn about
# #### Understanding of messy table(not source data Table) related to Tidy data
# #### Understanding of multiple Tables in a data set tab
# #### Multiple measures in a data set tab
# #### Artificial dimension to unify multiple tables data

# #### Load Data
# #### This spreadsheet contains Annual Business Survey Importers and exporters of goods and services in Great Britain by employment size, turnover size, ownership and age
# #### Observations of employment size, turnover size, ownership and age were differentiated into seperate tables 
# #### Following steps in Tidy data explains unifying various specific tables into one Tidy data further that will ease creating one tube for one data set

# In[ ]:


from gssutils import *

scraper = Scraper('https://www.ons.gov.uk/businessindustryandtrade/' +                   'business/businessservices/datasets/annualbusinesssurveyimportersandexporters')
scraper


# In[ ]:


tabs = { tab.name: tab for tab in scraper.distribution().as_databaker() }
tab = tabs['2016 Goods and Services']
savepreviewhtml(tab)


# In[ ]:


year = tab.name[:4]
year


# In[ ]:


cell = tab.filter('Detailed employment 3')
cell.assert_one()


# In[ ]:


trade = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
savepreviewhtml(trade)


# In[ ]:


observations = trade.fill(DOWN).is_not_blank().is_not_whitespace().is_number()
savepreviewhtml(observations)


# #### `measuretype` dimension generated further to create further dimension

# In[ ]:


measuretype = tab.filter(contains_string('Number of 5')).expand(RIGHT).is_not_blank().is_not_whitespace()
savepreviewhtml(measuretype)


# In[ ]:


businessstatistics = observations.shift(LEFT).is_not_blank().is_not_whitespace() - observations
savepreviewhtml(businessstatistics)


# In[ ]:


activity = measuretype.shift(-1,1).is_not_blank().is_not_whitespace()
savepreviewhtml(activity)


# #### `measure` is dimension as observations has multiple measures

# In[ ]:


measure = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()
savepreviewhtml(measure)


# #### Multiple tables unified with creation of `Business Activity` that includes Observations of employment size, turnover size, ownership and age

# In[ ]:


Dimensions = [
                HDimConst('Geography', 'K02000001'),
                HDimConst('Year', tab.name[:4]),
                HDim(activity,'Business Activity',CLOSEST,ABOVE),
                HDim(measure,'Measure Type', CLOSEST, RIGHT), 
                HDim(businessstatistics,'Business Statistics', CLOSEST,ABOVE),
                HDim(trade,'Flow',DIRECTLY,ABOVE)

    ] 


# #### The below tidy data could be achieved in various ways, the above and below steps are guidance purpose only as final data can be generated in other ways as well

# In[ ]:


c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)


# #### Errors and strings need to be cleaned 

# In[ ]:


new_table = c1.topandas()
new_table


# In[ ]:




