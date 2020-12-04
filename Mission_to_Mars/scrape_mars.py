
# Import Dependencies
# YOUR MISSION: To scrape the mars website

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # MARS HEADLINE SCRAPE

    url = 'https://mars.nasa.gov/'

    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    result = soup.find('div', class_='box floating_text_area left ms-layer')

    news_title = result.find('h1', class_='media_feature_title').text
    news_p = result.find('div', class_='description').text

    # MARS IMAGE SCRAPE

    mars_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_url)

    browser.find_by_id("full_image").click()
    browser.find_by_text("more info     ").click()

    soup = bs(browser.html, 'html.parser')

    relative_image_path = soup.find("img", class_="main_image")["src"]

    mars_img = "https://www.jpl.nasa.gov" + relative_image_path

    # Mars Facts

    facts_url = "https://space-facts.com/mars/"

    # make table into html string

    tables = pd.read_html(facts_url)

    df = tables[2]
    df.columns = ['Stat', 'Facts']

    html_tbl = df.to_html()

    mars_table = html_tbl.replace('\n', '')

    # Mars Hemisphere pics

    img_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(img_url)

    all_hems = []

    for i in range(4):

        browser.find_by_tag('h3')[i].click()

        html = browser.html
        soup = bs(html, 'html.parser')

        title = soup.find('h2', class_='title').text

        img_url = soup.find('a', text='Sample')['href']

        hem_urls = {
            "title": title,
            "img_url": img_url
        }

        all_hems.append(hem_urls)

        browser.back()

    mars_dict = {"news_title": news_title,
                    "news_p": news_p,
                    "mars_img": mars_img,
                    "mars_table": mars_table,
                    "all_hems": all_hems}

    # quit browser
    browser.quit()

    return(mars_dict)

