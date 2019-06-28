#!/usr/bin/env python
# coding: utf-8

# ### Multiple dimension
# #### This tutorial is continuation of second tutorial
# #### In this tutorial you learn about 
# #### Multiple dimension in hierarchy
# #### Missing dimension in hierarchy
# #### Remove unwanted labels in dimension

# #### Load data
# #### This note book describes about Total International Trade in Services analysed by continents and countries 
# #### Continets and Countries were in hierrachy but specifically in Europe data an extra hierarchy introduced with various 
# #### organisations in extra column but not for other continents, due to table format that create a wrong selection of hierarchy in a specific dimension
# 
# #### Follow similar step in tidy data generation look for area dimension

# In[ ]:


from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.ons.gov.uk/businessindustryandtrade/internationaltrade/datasets/internationaltradeinservicesreferencetables')
    tabs = { tab.name: tab for tab in scraper.distribution().as_databaker() }


# In[ ]:


tab = tabs['Table A0']
savepreviewhtml(tab)


# In[ ]:


Flow = tab.one_of(['Exports','Imports','Balance'])
savepreviewhtml(Flow)


# In[ ]:


Year = Flow.shift(0,1).expand(RIGHT).is_not_whitespace().is_not_blank()
savepreviewhtml(Year)


# In[ ]:


observations = Year.fill(DOWN).is_not_whitespace().is_not_blank()
savepreviewhtml(observations)


# In[ ]:


cell = tab.filter('AO')
cell.assert_one()


# In[ ]:


continents = cell.fill(DOWN).is_not_whitespace().is_not_blank()
savepreviewhtml(continents)


# country = cell.shift(2,0).fill(DOWN).is_not_whitespace().is_not_blank()
# savepreviewhtml(country)

# In[ ]:


area = cell.shift(1,0).fill(DOWN).is_not_whitespace().is_not_blank()
savepreviewhtml(area)


# In[ ]:


Dimensions = [
            HDim(Year,'Year',DIRECTLY,ABOVE),
            HDim(continents,'Continent',CLOSEST,ABOVE),
            HDim(country,'Country',CLOSEST,ABOVE),
            HDim(area, 'Area', CLOSEST, ABOVE),
            HDim(Flow, 'Flow',CLOSEST,LEFT),
            HDimConst('Measure Type', 'GBP Total'),
            HDimConst('Unit','gbp-million')
            ]


# #### From here important to understand how dimensions were selected for specific observations were all dimensions are correct?
# #### Because of Area dimension some observations below `Total Europe` were shown error

# In[ ]:


c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)


# #### A comparative look between source Table and Tidy table can able to view errors more precisely
# #### These errors should be communicated or discuused prior to Tidy data generation

# In[ ]:


new_table = c1.topandas()
new_table


# #### You learn about data manipulation in future tutorials
