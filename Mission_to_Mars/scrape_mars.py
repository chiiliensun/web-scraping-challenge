#!/usr/bin/env python
# coding: utf-8

# Dependencies
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape ():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # create dictionary to hold scraped data
    mars_dict = {}

    # Scrape the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # create a beautiful soup object
    html = browser.html
    soup = bs(html, "html.parser")

    # collect the latest News Title and Paragraph Text and assign the text to
    # to variables that I can reference later
    news_title = soup.find_all("div", class_="content_title")[1].text
    paragraph_text = soup.find("div", class_="article_teaser_body").text

    # move the print statements into dictionary created before scrape function
    mars_dict["News_Title"] = news_title
    mars_dict["Paragraph_Text"] = paragraph_text

    # browser.quit()

    # visit the url for image
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)

    # create a beautiful soup object
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, "html.parser")

    find_image = jpl_soup.find_all("img")[1]["src"]

    # assigning webpage url to later ensuring to get full size .jpg image url
    webpage_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"

    # assign the url string to a variable called featured_image_url
    featured_image_url = webpage_url + find_image

    # move the print statements into dictionary created before scrape function
    mars_dict["Featured_Image_Url"] = featured_image_url

    # browser.quit()

    # visit Mars Facts webpage and use pandas to scrape table
    facts_url = "https://space-facts.com/mars/"
    # browser.visit(facts_url)

    fact_table = pd.read_html(facts_url)

    # convert to pandas table before converting the data to a HTML table string
    facts_pdtable = fact_table[0]
    facts_pdtable.columns = ["Description", "Values"]

    # convert the data to a HTML table string
    html_table = facts_pdtable.to_html(index=False)

    # move the print statements into dictionary created before scrape function
    mars_dict["Mars_Table"] = html_table

    # browser.quit()

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    # create a beautiful soup object
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, "html.parser")

    # assigning webpage url to later ensuring to get full size .jpg image url for all hemispheres
    hemis_webpage_url = "https://astrogeology.usgs.gov"

    # create lists to hold Save both the image url string for the full resolution hemisphere image, and the Hemisphere
    # title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    hemispheres_titles = []
    all_urls = []

    # find the hemisphere titles
    hemispheres = hemisphere_soup.find_all("div", class_="item")
    # for hemi in hemispheres:
    #     hemispheres_titles.append(hemi.text)

    # Loop throught to meet all requirements
    print('hit for')
    for hemis in hemispheres:
        print('looping')
        browser.visit(hemisphere_url)
        # Click each of the links to the hemispheres in order to find the image url
        # browser.links.find_by_partial_text(hemis).click()
        # hemisphere_html = browser.html
        # hemisphere_soup = bs(hemisphere_html, "html.parser")
        # # Set variable and find the image links
        # title = hemisphere_soup.find("h2", class_="title").text
        # print(title)
        # img_url = hemisphere_soup.find("img", class_="wide-image")["scr"]
        # print(img_url)
        title = hemis.find("h3").text
        print(title)
        img_url = hemis.find("img")['src']
        print(img_url)
        # Use a Python dictionary
        hold_images = {
            'title':title,
            'hemi_url': hemis_webpage_url + img_url
        }
        # Store the data using the keys img_url and title
        # hold_images["Hemisphere_Title"]=hemispheres_titles
        # hold_images["Url"]=imgs
        # Append the dictionary with the image url string and the hemisphere title to a list
        all_urls.append(hold_images)

        # move the print statements into dictionary created before scrape function
        mars_dict["Hemisphere_Urls"] = all_urls

    browser.quit()

    print(all_urls)
    return mars_dict

if __name__ == '__main__':
    print(scrape())
