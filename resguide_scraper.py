""" This script is intended to demonstrate how to scrape citation data from a research guide to prepare for Wikidata uploads.
"""
# import necessary packages
from bs4 import BeautifulSoup as soup
#from urllib import request
from urllib.request import Request, urlopen
import requests
import re
import json
import csv



def getArticles():
    # This chunk grabs all the HTML from the url below"
    url =  "https://research.lib.buffalo.edu/esjag-reading/whiteness-librarianship"
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    f = urlopen(request_site)
    soup_page_html = str(f.read())
    f.close

    # This statement takes the HTML and passes it to the Beautiful Soup parser
    page_soup = soup(soup_page_html, 'html.parser')
 
    results = page_soup.find("ul", class_="s-lg-link-list")
    
    articles = results.find_all("div", class_="")
    #print(articles)
    
    incoming_articles = []
    
    for i, article in enumerate(articles):
        print(i)
        article_url = article.find("a")
        article_link = article_url.get("href")
        print(f'The link to the article is {article_link}')
        article_title = article_url.text.strip('\\n ')
        print(article_title)
        article_summary = article.find("div", class_="s-lg-link-desc")
        article_abstract = article_summary.text.strip('\\n, \n')
        print(f'The article abstract is {article_abstract}')
        
        article_info = article.find("div", class_="s-lg-content-moreinfo")
        if article_info:
            article_cite = article_info.text
        else:
            article_cite = "no citation given"
        

        incoming_articles.append({"article link":article_link, "article title":article_title, "article summary":article_abstract, "article citation":article_cite})

    return incoming_articles


articles_scraped = getArticles()


print(articles_scraped)
# Append the results to a JSON file
filename = "resguide_List.json"
with open(filename, 'a') as f:
    json.dump(articles_scraped, f)


# Append results into a CSV file with headers
updater = "resguide_List.csv"
field_names=["article link", "article title", "article summary", "article citation"]

with open(updater, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(articles_scraped)
