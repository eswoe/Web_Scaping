#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import csv
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


def load_page(url):
    with requests.get(url) as f:
        page = f.text
    return page


# In[3]:


def get_element_text(element):
    try:
        return element.text.strip()
    except AttributeError as e:                     
        print('Element not found, error: {}'.format(e), file=sys.stderr)
        return ''


# In[4]:


def get_song_info(url):
    song_page = BeautifulSoup(load_page(url), 'lxml')                  
    interesting_html = song_page.find('article')                       
    if not interesting_html:                                           
        print('No information availible for song at {}'.format(url), file=sys.stderr)
        return {}                                                     
    credits = get_element_text(interesting_html.find(class_='credit'))
    lyrics = get_element_text(interesting_html.find(class_='lyrics'))
    lyrics = lyrics.replace('\r\n', '\n')                              
    lyrics = re.sub('\t\t+', '\n', lyrics)
    return {'credits': credits, 'lyrics': lyrics}


# In[5]:


song_url = 'https://www.bobdylan.com/songs/10000-men/'
song_info = get_song_info(song_url)
for key, value in song_info.items():
    if key == 'lyrics':
        print(value)


# In[6]:


def get_songs(url):
    index_page = BeautifulSoup(load_page(url), 'lxml')        
    items = index_page.find(id='item-list')                  
    if not items:
        print('Something went wrong!', file=sys.stderr)
        sys.exit()
    data = []
    for row in items.find_all(class_='line_detail'):          
        song = row.find(class_='song').find('a').text.strip() 
        link = row.find(class_='song').find('a').get('href')
        album_name = row.find(class_='release').text.strip()
        first_played = row.find_all(class_='played')[0].text.strip()
        last_played = row.find_all(class_='played')[1].text.strip()
        times_played = row.find(class_='times').text.strip()
        data.append({                                         
                     'song': song,
                     'link': link,
                     'album name': album_name,
                     'first played': first_played,
                     'last played': last_played,
                     'times played': times_played
                    })
    return data


# In[7]:


index_url = 'https://www.bobdylan.com/songs/'         
song_data = get_songs(index_url)                      
for row in song_data:
    print('Scraping info on {}.'.format(row['song'])) 
    url = row['link']
    song_info = get_song_info(url)                    
    for key, value in song_info.items():
        row[key] = value                              


# In[8]:


with open('songs.csv', 'w', encoding='utf-8') as f:       
    fieldnames=['song', 'album name', 'first played', 'last played',
                'times played', 'credits', 'lyrics']
    writer = csv.DictWriter(f,
                            delimiter=',',                
                            quotechar='"',                
                            quoting=csv.QUOTE_NONNUMERIC, 
                            fieldnames=fieldnames
                            )
    writer.writeheader()
    for row in song_data:
        writer.writerow({k:v for k,v in row.items() if k in fieldnames})


# In[9]:


dataset = pd.read_csv('songs.csv') 
dataset[['song','lyrics', 'times played']].dropna()


# In[10]:


dataset.describe()


# In[11]:


top_ten = dataset.nlargest(10, 'times played')


# In[12]:


top_ten


# In[ ]:





# In[13]:


dataset = pd.read_csv('songs.csv') 
dataset[['song','lyrics']].dropna()


# In[74]:


plotdata = pd.DataFrame(
    {"times played": [975, 1051, 1070, 1086, 1253, 1585, 1685, 2000, 2075,2268]}, 
    index=["Things Have Changed", "Maggie's Farm", "It Ain't Me Babe",
         "Don't Think Twice, It's Alright", "Ballad of a Thin Man", "Blowin' in the Wind",
         "Tangled Up in Blue", "Highway 61 Revisited", "Like a Rolling Stone", "All Along the Watchtower"])
# Plot a bar chart
plotdata.plot(kind="bar");


# In[79]:


plotdata['times played'].plot(kind="bar", title="Bob Dylan's Most Performed Songs")
plt.xticks(rotation=30, horizontalalignment="right")
plt.title("Bob Dylan's Most Performed Songs")
plt.xlabel("Song Title")
plt.ylabel("Times Played");


# In[82]:


dataset.groupby('song')['times played'].sum().nlargest(n = 10).sort_values().plot(kind='bar', figsize = (10, 10), title = "Bob Dylan's Most Performed Songs");


# In[91]:


dataset.groupby('song')['times played'].sum().nlargest(n = 10).sort_values().plot(kind='pie', figsize = (10, 10), title = "Bob Dylan's Top Performed Songs");


# In[17]:


def get_song_info(url):
    song_page = BeautifulSoup(load_page(url), 'lxml')                  
    interesting_html = song_page.find(id='listAlbum')                       
    if not interesting_html:                                       
        print('No information availible for song at {}'.format(url), file=sys.stderr)
        return {}                                                      
    album_name = get_element_text(interesting_html.find(class_='album')) 
    song = get_element_text(interesting_html.find(class_='listalbum-item'))
    song = song.replace('\r\n', '\n')                              
    songs = re.sub('\t\t+', '\n', song)
    return {'album': album_name, 'listalbum-item': song}


# In[18]:


song_url = 'https://www.azlyrics.com/j/jones.html'
song_info = get_song_info(song_url)
for key, value in song_info.items():
    if key == 'listalbum-item':
        print(value)
#Not really sure why the only listalbum-item that prints is this first one, because there are many more on the
#page. Same thing happens for 'album'. The only album name returned is the first one on the list on the web page.

