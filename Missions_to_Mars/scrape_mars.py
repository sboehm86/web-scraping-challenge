#import dependencies
import pandas as pd 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests


def init_browser():
    ex_path = {'executable_path': 'C:/Users/Shawn\Documents/Analytics Bootcamp/chromedriver.exe'}
    browser = Browser('chrome', **ex_path, headless=True)
    #return Browser('chrome',**ex_path,headless=True)

mars_data={}
#dictionary to be exported to mongod

def mars_scrape():
    try:
        browser=init_browser()
        