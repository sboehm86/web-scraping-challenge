#import dependencies
import pandas as pd 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests


def init_browser():
    ex_path = {'executable_path': '../Mission_to_Mars/chromedriver.exe'} #changed pc path to git forlder
    browser = Browser('chrome', **ex_path, headless=True)
    #return Browser('chrome',**ex_path,headless=True)

mars_data={}
#dictionary to be exported to mongod

#NEWS
def mars_scrape_news():
    try:
        browser=init_browser()
        
        nasa_url='https://mars.nasa.gov/news/'
        browser.visit(nasa_url)
        
        html=browser.html
        soup=bs(html,'html.parser')
        
        slide=soup.select_one('ul.item_list li.slide')
        headline=slide.find('div',class_='content_title').get_text()
        body=slide.find('div',class_='article_teaser_body').get_text()
        
        mars_data['news_headline']=headline
        mars_data['news_body']=body
        
        return mars_data
    finally:
        browser.quit()
        
        
#FEATURED IMAGE
def mars_scrape_image():
    try:
        browser=init_browser()
        
        image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)
        
        elem1=browser.find_by_id("full_image")
        elem1.click()
        
        more_info=browser.links.find_by_partial_text('more info')
        more_info.click()
        
        html_image=browser.html
        soup2=bs(html_image,'html.parser')
        
        img_rel=soup2.select_one('figure.lede a img').get("src")
        
        feat_img_link=f'https://www.jpl.nasa.gov{img_rel}'
        
        mars_data['feat_img_link']=feat_img_link
        
        return mars_data
    finally:
        browser.quit()
        
        
#MARS WEATHER
def mars_scrape_faq():
    try:
        browser=init_browser()
        url3='https://space-facts.com/mars/'

        mars_df=pd.read_html(url3)
        mars1=mars_df[0]
        
        mars1.rename(columns={"0":"Description", "1": "Mars"})
        
        return mars1.to_html(classes="table table striped")
    finally:
        browser.quit()
        
        
#MARS HEMISPHERES
def mars_scrape_hemi():
    try:
        browser=init_browser()
        hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemi_url)
        
        html_hemi = browser.html
        soup = bs(html_hemi, 'html.parser')
        
        items = soup.find_all('div', class_='item')
        hemisphere_image_urls = []
        
        hemi_main = 'https://astrogeology.usgs.gov'

        for i in items: 
            title = i.find('h3').text
    
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
            browser.visit(hemi_main + partial_img_url)
    
            partial_img_html = browser.html
     
            soup = bs( partial_img_html, 'html.parser')
    
            img_url = hemi_main + soup.find('img', class_='wide-image')['src'] 
        
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
        mars_data['hemi_main']=hemi_main
        return mars_data
    finally:   
        browser.quit()