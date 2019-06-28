#!/usr/bin/env python
# coding: utf-8

# ## Tidy Data Generation ## 
# 
# #### This note book illustrates tidy data generation from data set and that tidy data get published as a data cube. The main key point is the generation of csv table from human readable data that can be readable and processed by computer. Human readable messy tables of various heirarchies get flattened in this process. 
# 
# ### In this notebook you learn about 
# #### Finding data
# #### Load data
# #### Selecting required tabs from data set
# #### Selecting dimensions and observations
# #### Mapping observation to dimensions
# #### Converting set of observation together with dimensions
# #### Generate tidy table

# #### Here we will use data from  [Pinkbook](https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/3tradeinservicesthepinkbook2016) released by ONS, 
# #### Pink book data distributed into various tabs based on services, this book for explain tidy data generation from tab 3.10 Government services
# 
# 

# ### Load Files
# #### Here we download data set using gssutils, using https dataset url link, gssutils and other required packages installation link available from [Git Link](https://github.com/ONS-OpenData/gss-data-docs/wiki/Installation-Guide)

# In[ ]:


from gssutils import *

scraper = Scraper('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/3tradeinservicesthepinkbook2016')
scraper


# ### Selecting required tabs from data set
# 
# #### Pull Tab 3.10 data table from dataset by using below databaker scraper distrubution code, you can view tab using `savepreviewhtml()`.  
# #### As data tab implemented in databaker way further steps to generate tidy data work based on databaker package code along with other python packages for data wrangling.

# In[ ]:


tabs = { tab.name: tab for tab in scraper.distribution().as_databaker() }
tab = tabs['3.10']
savepreviewhtml(tab)


# ### Select Dimensions
# 
# #### Data in this tab distrubuted in a human readable table with various columns and rows, observations are numerical numbers defined by various dimensions, in human readable table format dimensions could be in rows or in columns 
# #### In human readable format various dimensions could be in same column like services and export or imports. 
# ####  Observation in Tab 3.10 data defined with following dimension Year, Services, Code,  Imports or Exports. So here a dimension is a list of specific attributes that define observation related to dimension.  
# #### First step to generate tidy data is  to map observations with dimensions, we can do that by defining various dimensions as variable.
# #### Below steps describe variables with their attributes, those are year, service, code.
# #### cell value defined as start point reference in tab, further to pull down dimesions 

# In[ ]:


cell = tab.filter('Government services')
cell.assert_one()


# #### Select year dimension

# In[ ]:


year = tab.filter('year')
savepreviewhtml(year)


# #### Select services dimension

# In[ ]:


service = cell.fill(DOWN).is_not_blank().is_not_whitespace()
savepreviewhtml(service)


# #### Select code dimension

# In[ ]:


code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
savepreviewhtml(code)


# #### Define observations

# In[ ]:


observations = year.fill(DOWN).is_not_blank().is_not_whitespace()
savepreviewhtml(observations)


# #### Define how each observation is connected to it's dimension by `HDim()` and   some of dimensions defined as constants as they are taken from source data that will be same for all observations `HDimConst()` 
# #### Give a `Heading` to each dimension
# #### Map dimension to observation, how observations connected with a specific dimension
# #### Dimension `Geography`, `Unit`, `Measure Type` are constants, those will be same for all observations

# In[ ]:


Dimensions = [
            HDimConst('Geography', 'K02000001'),
            HDim(year,'Year', DIRECTLY,ABOVE),
            HDim(code,'CDID',DIRECTLY,LEFT),
            HDimConst('Unit','£ Million'),  
            HDimConst('Measure Type','GBP Total'),
            HDim(service, 'Product', DIRECTLY, LEFT)
]


# #### `conversionsegment` is each observations with all dimension

# In[ ]:


c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)


# In[ ]:


savepreviewhtml(c1)


# #### Below cell convert conversion segment to panda data frame further for data manipulation

# In[ ]:


new_table = c1.topandas()
new_table


# #### These are basic steps in first tidy data generation, further clean the data as according to requirements
