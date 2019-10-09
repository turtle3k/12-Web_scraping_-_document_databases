# Imports
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import browser
import time


def init_browser():
    # MAC users different setup.  Windows splinter setup:
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    # Setup a dictionary to hold all the scraped data
    scraped_data = {}

    # ### Site 1 - NASA Mars News
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    # use beautufil soup to parse the URL 
    html = browser.html
    #soup = bs(response.text, 'html.parser')
    soup = bs(html, 'html.parser')

    # use bs to find() the example_title_div and filter on the class_='content_tile'
    news_title = soup.find("div", class_="content_title").text
    scraped_data['news_title'] = news_title

    # use bs to find() the example_title_div and filter on the class_='article_teaser_body'

    #news_p = soup.find("div", class_="rollover_description_inner").text
    news_p = soup.find("div", class_="article_teaser_body").text
    scraped_data['news_p'] = news_p


    print(scraped_data)


    # ### Site 2 - JPL Mars Space Images - Featured Image
    # site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
    # use splinter to connect to the url and navigate - current featured Mars Image - 
    # then use bs4 to repeat what you did in site 1

    # Example:
    #featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
    #scraped_data['featured_image_url'] = featured_image_url


    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')


    html = browser.html
    soup = bs(html, 'html.parser')
    # https://stackoverflow.com/questions/8289957/python-2-7-beautiful-soup-img-src-extract
    featured_image_url = soup.find('img')['src']
    scraped_data['featured_image_url'] = featured_image_url

    print(scraped_data)


    # ### Site 3 - Mars Weather twitter account

    # site 3 - https://twitter.com/marswxreport?lang=en
    # grab the latest tweet and be careful its a weather tweet
    # Example:
    #mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)

    tweet_html = browser.html
    tweet_soup = bs(tweet_html, 'html.parser')

    mars_weather = tweet_soup.find("p", class_="TweetTextSize").text
    scraped_data['mars_weather'] = mars_weather

    print(scraped_data)


    # ### Site 4 - Mars Facts webpage
    # site 4 - 
    facts_url = 'https://space-facts.com/mars/'

    # use pandas to parse the table
    # Ref ex Ch12-day2-ex09
    facts_df = pd.read_html(facts_url)[1]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index('Description', inplace=True)

    # convert facts_df to a html string and add to dictionary.
    facts_html = facts_df.to_html()
    facts_html.replace('/n', '')

    scraped_data['facts_html'] = facts_html


    # ### Site 5 - Mars Hemispheres from USGS Astrogeology site
    # use bs4 to scrape the title and url and add to dictionary

    # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    hemisphere_list = []
    links = browser.find_by_css("a.product-item h3")
    for h in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[h].click()
        element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"]=element["href"]
    
        hemisphere["title"]=browser.find_by_css("h2.title").text
    
        hemisphere_list.append(hemisphere)
        browser.back()

    #print(hemisphere_list)
    scraped_data['hemisphere_list'] = hemisphere_list

    return scraped_data


