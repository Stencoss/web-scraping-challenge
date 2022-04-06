

# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser



# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)




# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)




#Define Database and collections
db = client.mars_db
collection = db.lastest




# URL for latest articles to be scrape
url = "https://redplanetscience.com/"



# Dynamically loaded page so it needs to use driver to pull the full source code.  With just soup
# it only pulls the static page information.

browser.visit(url)
html = browser.html




# Use driver html and parse ; parse with 'html.parser'
soup = BeautifulSoup(html, 'html.parser')




# Find the par tof the page that holds the information we need.
# div class = list_text             Main div 
# div class = content_title         sub div title
# div class = article_teaser_body   sub div paragraph

results = soup.find_all('div', class_='list_text')
print(len(results))




# Loop over the data that was collected and pull title and paragraph infromation from it

for result in results:
    try:
        # scrape article title
        news_title = result.find('div', class_='content_title').text
        # Scrape the div sub paragraph
        news_p = result.find('div', class_='article_teaser_body').text
        print( news_title)
        print(news_p)
        print("/n/n")

        data = {
            'title': news_title,
            'news_p': news_p
        }

    except Exception as e:
        print(e)



browser.quit()


# ## Part Two
# ### JPL Mars Space Images - Featured Image



url_jpl = "https://spaceimages-mars.com"





# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url_jpl)
html2 = browser.html
soup_jpl = BeautifulSoup(html2, 'html.parser')




# browser.links.find_by_partial_text('FULL IMAGE').click()
results_jpl = soup_jpl.findAll('img', class_='headerimage fade-in')
for image in results_jpl:
    part_url = image['src']

featured_image_url = url_jpl + '/' + part_url
print(featured_image_url)




browser.quit()


# ## Part 3
# ### Mars Facts



# Input the URL for mars fact table
url_facts = 'https://galaxyfacts-mars.com/'




# Pandas needs to read the table and then verify output.

tables = pd.read_html(url_facts)




# Confirm that data was pulled
df = tables[0]
df.head()



# Drop unneeded columns
df.drop(2, axis=1)


# ## Part 4
# ### Mars Hemispheres



# Url to inspect
url_hemi = 'https://marshemispheres.com'
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)




# Open URL so we can click links
# Need to click on the object 
# <a href="cerberus.html" class="itemLink product-item"><h3>Cerberus Hemisphere Enhanced</h3> </a>
# Then the open button on the next page - neeed a loop
browser.visit(url_hemi)
# html_list = browser.html
# soup_list = BeautifulSoup(html_list, 'html.parser')
# find_list = soup.find_all('a', class_='itemLink product-item')
# for link in find_list:
#     print(link.href)




# For loop for the 4 links we need to click on for the first page
import time
export_list = []
for x in range(4):
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')
    time.sleep(.5)
    browser.links.find_by_partial_text('Enhanced')[x].click()
    html_temp = browser.html
    soup = BeautifulSoup(html_temp, 'html.parser')
    time.sleep(.5)
    find_link = browser.find_link_by_partial_text('Sample')
    # print(find_link['html'])
    print(find_link['href'] + " " + browser.find_by_css("h2.title").text)
    # browser.links.find_by_partial_text('Sample').click()  find('div', class_='content_title').text)
    # browser.windows[1].close()
    export_list.append({'title': find_link['href'],
                        'link': browser.find_by_css("h2.title").text})


    browser.back()




browser.quit()

