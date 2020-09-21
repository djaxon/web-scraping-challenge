from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_all():
    # Latest news scrape
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    listings={}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings['headline']=soup.find('div', class_='content_title').get_text().replace('\n', '')
    listings['summary']=soup.find('div', class_='rollover_description_inner').get_text().replace('\n', '')
    
    # Featured Image Url scrape
    browser= init_browser()
    url_2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_href('largesize')
    featured_image_url= browser.url
    
    # Mars facts table 
    # table_url='https://space-facts.com/mars/'
    # Mars_table = pd.read_html(table_url)
    # df= Mars_table[0]
    # df.columns=['Characteristics', 'Stats']
    # Mars_facts=df.to_html().replace('\n', '')

    Mars_facts = 'file:///C:/Users/djack/Documents/LearnPython/web-scraping-challenge/Mission_to_Mars/Mars_table.html'
    
    # Mars hemisphere image URLs
    url_3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_3)
    browser.click_link_by_partial_text('Cerberus')
    browser.click_link_by_partial_text('Sample')
    Cerberus_image_url=browser.windows[1].url
    browser.back()
    browser.click_link_by_partial_text('Schiaparelli')
    browser.click_link_by_partial_text('Sample')
    Schiaparelli_image_url=browser.windows[2].url
    browser.back()
    browser.click_link_by_partial_text('Syrtis')
    browser.click_link_by_partial_text('Sample')
    Syrtis_image_url=browser.windows[3].url
    browser.back()
    browser.click_link_by_partial_text('Valles')
    browser.click_link_by_partial_text('Sample')
    Valles_image_url=browser.windows[4].url
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": Valles_image_url},
    {"title": "Cerberus Hemisphere", "img_url": Cerberus_image_url},
    {"title": "Schiaparelli Hemisphere", "img_url": Schiaparelli_image_url},
    {"title": "Syrtis Major Hemisphere", "img_url": Syrtis_image_url}
]

    mars_info_dict= {
        'latest_news': listings['headline'],
        'latest_summary': listings['summary'],
        'featured_image': featured_image_url,
        'Mars_facts_table': Mars_facts,
        'Mars_hemispheres_images': hemisphere_image_urls
        
    }
    

    return mars_info_dict

