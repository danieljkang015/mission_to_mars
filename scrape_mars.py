from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

# NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

#  Featured Image
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)

    featured_image_button = browser.find_by_id("full_image")
    featured_image_button.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov" + soup.find("img", class_="fancybox-image")["src"]
    featured_image_url

    mars_data['featured_image_url'] = featured_image_url

# Mars Weather
    url_3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet=soup.find("div", attrs={"data-screen-name":"MarsWxReport", "class":"tweet"})

    mars_weather=soup.find("p", class_="TweetTextSize")
    mars_weather=mars_weather.get_text()
    mars_weather

    mars_data['mars_weather'] = mars_weather

# Mars Facts
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]

    mars_df.columns = ["Description", "Values"]
    mars_df.set_index(["Description"], inplace=False)

    mars_df.to_html()
    data = mars_df.to_dict(orient='records')
    mars_data['mars_df'] = mars_df

# Mars Hemispheres

    url_4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_4)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls=[]

    links = soup.findAll("a", class_="product-item")

    base_url = "https://astrogeology.usgs.gov"
    for i in links:
        if i.find("h3"):
            browser.visit(base_url + i["href"])
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            imgurl= base_url + soup.find("img", class_="wide-image")['src']
            title = soup.find("h2", class_="title").get_text()
            hemisphere_image_urls.append({"title": title, "img": imgurl})
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data