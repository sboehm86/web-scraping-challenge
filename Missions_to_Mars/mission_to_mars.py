#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests


# In[17]:


# Set up soup to scrape
ex_path = {'executable_path': 'C:/Users/Shawn\Documents/Analytics Bootcamp/chromedriver.exe'}
browser = Browser('chrome', **ex_path, headless=False)


# In[8]:


nasa_url='https://mars.nasa.gov/news/'
browser.visit(nasa_url)


# In[9]:


#Save title and paragraph as objects
#inspector
html=browser.html
soup=bs(html,'html.parser')

#article=soup.find('li', class_='slide')
slide=soup.select_one('ul.item_list li.slide')
#head_body=soup.find('div',class_='article_teaser_body') don't need to grap individual pieces, just the whole slide


# In[15]:


#find elements required, headline body
headline=slide.find('div',class_='content_title').get_text()
body=slide.find('div',class_='article_teaser_body').get_text()
print(headline)
print(body)


# JPL Mars Space Images - Featured Image

# In[18]:


#visit page
image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(image_url)


# In[20]:


#find, click, save full image
#full image
elem1=browser.find_by_id("full_image")
elem1.click()


# In[21]:


#more info
more_info=browser.links.find_by_partial_text('more info')
more_info.click()


# In[22]:


#need to parse this page to search it
html2=browser.html
soup2=bs(html2,'html.parser')


# In[23]:


#scrape the full image
img_rel=soup2.select_one('figure.lede a img').get("src")
img_rel
#full res jpg found via inspector <a href="//photojournal.jpl.nasa.gov/jpeg/PIA19637.jpg">PIA19637.jpg</a>
#img_url=f'//photojournal.jpl.nasa.gov/jpeg/PIA19637.jpg'


# In[24]:


#convert to permenant link
img_link=f'https://www.jpl.nasa.gov{img_rel}'
img_link


# Mars Facts

# In[31]:


#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#Use Pandas to convert the data to a HTML table string.

url3='https://space-facts.com/mars/'
mars_df=pd.read_html(url3)
mars1=mars_df[0]
mars1


# In[39]:


#mars1.columns=['Description','Mars']
mars1.rename(columns={"0":"Description", "1": "Mars"})
#mars1.set_index('Description', inplace=True)
mars1


# Mars Hemi-Spheres

# In[57]:


hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)


# In[59]:


# make my html object...
html_hemi = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_hemi, 'html.parser')

# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')

# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Store the main_ul 
hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
for i in items: 
    # Store title
    title = i.find('h3').text
    
    # Store link that leads to full image website
    partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
    # Visit the link that contains the full image website 
    browser.visit(hemispheres_main_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve full image source 
    img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
hemisphere_image_urls


# In[60]:

browser.quit()