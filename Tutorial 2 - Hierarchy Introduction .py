#!/usr/bin/env python
# coding: utf-8

# ## Hierarchy Introduction 
# 
# #### This note book illustrates hierarchy in data sets, Second Tutorial is continuation of First Tutorial
# #### Please follow similar steps as according to First Tutorial data set from [Pinkbook](https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/3tradeinservicesthepinkbook2016) released by ONS
# #### Tab 3.10 Government services
# 
# ### In this note book you learn about 
# #### Dimensional hierarchy

# #### Tab 3.10 Goverment services were disrubuted into Exports(Credit), Imports(Debits) and Balances, this section  ot covered in First Tutorial. So this is flow of money can be called as `Flow` dimension
# #### Here in this note book `Flow` dimension is parent heirarchy to services, eg: services under export and services under import

# In[ ]:


from gssutils import *

scraper = Scraper('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/3tradeinservicesthepinkbook2016')
scraper


# #### Pull Tab 3.10 data table from dataset by using below databaker scraper distrubution code, you can view tab using `savepreviewhtml()`.  
# #### As data tab implemented in databaker way further steps to generate tidy data work based on databaker package code along with other python packages for data wrangling.

# In[ ]:


tabs = { tab.name: tab for tab in scraper.distribution().as_databaker() }
tab = tabs['3.10']
savepreviewhtml(tab)


# #### Data in this tab distrubuted in a human readable table with various columns and rows, observations are numerical numbers defined by various dimensions, in human readable table format dimensions could be in rows or in columns to understand observations and in this format various dimensions could be in same column like services and export or imports. 
# ####  Observation in Tab 3.10 data defined with following dimension Year, Services, Code,  Imports or Exports. So here a dimension is a list of specific attributes that define observation related to dimension.  
# #### First step to generate tidy data is  to map observations with dimensions, we can do that by defining various dimensions as variable.
# #### Below steps describe variables with their attributes, those are year, service, code.
# #### cell value defined as start point further to pull dimesions  

# In[ ]:


cell = tab.filter('Government services')
cell.assert_one()


# In[ ]:


year = cell.shift(0,2).expand(RIGHT).is_not_blank().is_not_whitespace()


# In[ ]:


service = cell.fill(DOWN).is_not_blank().is_not_whitespace()


# In[ ]:


code = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()


# #### Select `Flow` dimension, `Flow` dimension is next in hierarchy to services

# In[ ]:


flow = cell.fill(DOWN).one_of(['Exports (Credits)', 'Imports (Debits)', 'Balances' ])
savepreviewhtml(flow)


# #### Define observations

# In[ ]:


observations = year.fill(DOWN).is_not_blank().is_not_whitespace()
savepreviewhtml(observations)


# #### Define how each observation is connected to it's dimension by `HDim()` and   some of dimensions defined as constants as they are taken from source data that will be same for all observations `HDimConst()` 

# In[ ]:


Dimensions = [
            HDimConst('Geography', 'K02000001'),
            HDim(year,'Year', DIRECTLY,ABOVE),
            HDim(code,'CDID',DIRECTLY,LEFT),
            HDimConst('Unit','£ Million'),  
            HDimConst('Measure Type','GBP Total'),
            HDim(service, 'Product', DIRECTLY, LEFT),
            HDim(flow, 'Flow', CLOSEST, ABOVE)
]


# #### `conversionsegment` is observations with all dimension

# In[ ]:


c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)


# In[ ]:


savepreviewhtml(c1)


# #### Below cell convert conversion segment to panda data frame further for data manipulation

# In[ ]:


new_table = c1.topandas()
new_table


# In[ ]:




