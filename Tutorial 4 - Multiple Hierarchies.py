#!/usr/bin/env python
# coding: utf-8

#  ### Multiple Hierarchies
#  #### In this note book you learn about 
#  #### Understanding of Multile Hierarchy in source data
#  #### Creating Dimension in multiple hierarchy 

# #### Load Data

# In[ ]:


from gssutils import *

scraper = Scraper('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/3tradeinservicesthepinkbook2016')
scraper


# In[ ]:


tabs = { tab.name: tab for tab in scraper.distribution().as_databaker() }
tab = tabs['3.2']
savepreviewhtml(tab)


# #### This note book describes Trade revenue from different transport services 
# #### Hierarchy : observations/ Revenue/ Service/ Mode of Transport/ Flow

# In[ ]:


Flow = tab.one_of(['Exports (Credits)','Imports (Debits)','Balances'])
savepreviewhtml(Flow)


# In[ ]:


cell = tab.filter('Transport')
cell.assert_one()


# In[ ]:


Year = cell.shift(0,2).expand(RIGHT).is_not_whitespace().is_not_blank()
savepreviewhtml(Year)


# In[ ]:


observations = Year.fill(DOWN).is_not_whitespace().is_not_blank()
savepreviewhtml(observations)


# In[ ]:


modeoftransport = cell.fill(DOWN).one_of(['Sea transport', 'Air transport', 'Rail', 'Road'])
savepreviewhtml(modeoftransport)


# In[ ]:


service = cell.fill(DOWN).one_of(['Passenger', 'Dry cargo', 'Wet cargo', 'Other transport'])
savepreviewhtml(service)


# In[ ]:


revenue = cell.fill(DOWN).is_not_whitespace().is_not_blank() - service - modeoftransport
savepreviewhtml(revenue)


# In[ ]:


Dimensions = [
            HDim(Year,'Year',DIRECTLY,ABOVE),
            HDim(modeoftransport,'Mode of transport',CLOSEST,ABOVE),
            HDim(service,'Service',CLOSEST,ABOVE),
            HDim(revenue, 'Revenue',CLOSEST,ABOVE ),
            HDim(Flow, 'Flow',CLOSEST,ABOVE),    
            HDimConst('Measure Type', 'GBP Total'),
            HDimConst('Unit','gbp-million')
            ]


# In[ ]:


c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)


# #### Errors to be corrected as according to source data

# In[ ]:


new_table = c1.topandas()
new_table


# In[ ]:




