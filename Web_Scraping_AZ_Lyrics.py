#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


# In[55]:


response = requests.get("https://www.azlyrics.com/j/jones.html")
html_string = response.text

document = BeautifulSoup(html_string, "html.parser")
document


# In[56]:


all_titles = document.find_all("div", attrs={"class": "listalbum-item"})
all_titles


# In[57]:


#all_titles1 = []
#for title in all_titles:
    #title_contents = title.text
    #all_titles1.append(title_contents)
    
all_titles1 = [title.text for title in all_titles]
all_titles1


# In[58]:


all_albums = document.find_all("div", attrs={"class": "album"})
all_albums


# In[59]:


all_albums1 = [album.text for album in all_albums]
all_albums1


# In[ ]:




