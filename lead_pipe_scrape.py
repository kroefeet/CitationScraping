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

def getAllPages():
    # This is the base URL without accounting for pages
    base_url = "https://www.inthelibrarywiththeleadpipe.org/"
    request_site = Request(base_url, headers={"User-Agent": "Mozilla/5.0"})
    f = urlopen(request_site)
    base_soup_html = str(f.read())
    f.close
    base_soup = soup(base_soup_html, 'html.parser')
    #print(base_soup)
    #print(base_soup.find_all("a", class_="page-numbers")[-2])
    last_page = base_soup.find_all("a", class_="page-numbers")[-2]
    print(int(last_page.text))
    all_pages_list = [base_url]
    for index in range(int(last_page.text)-1):
        page_num = index + 2
        page_url=base_url+"page/"+str(page_num)+"/"
        all_pages_list.append(page_url)
    print(all_pages_list)
    return all_pages_list

def getArticles(url):
    # This chunk grabs all the HTML from the url passed as an argument"
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    f = urlopen(request_site)
    soup_page_html = str(f.read())
    f.close

    # This statement takes the HTML and passes it to the Beautiful Soup parser
    page_soup = soup(soup_page_html, 'html.parser')
 
    results = page_soup.find("div", class_="blog-item-holder")
    #print(results)
    
    articles = results.find_all("div", class_="gdlr-item gdlr-blog-full")
    #print(articles)
    
    incoming_articles = []

    for i, article in enumerate(articles):
        #print(i)
        article_main = article.find("h3", class_="gdlr-blog-title")
        article_title = article_main.text
        #print(article_title)
        article_link = article_main.find("a")
        article_url = article_link.get("href")
        #print(article_url)
        article_author_main = article.find("a", class_="author")
        article_author = article_author_main.text
        #print(article_author)
        article_daynum = article.find("div", class_="gdlr-blog-day")
        article_day = article_daynum.text
        #print(article_day.text)
        article_year_month = article.find_all("div", class_="gdlr-blog-month")
        #print(article_month[0].text)
        article_year = article_year_month[0].text
        article_month = article_year_month[1].text
        pub_date = article_day +" "+ article_month +" "+ article_year
        #print(pub_date)
        short_summary = article.find("div", class_="gdlr-blog-content")
        short_summary_text = short_summary.text
        #print(short_summary_text)

        incoming_articles.append({"article url":article_url, "article title":article_title, "article author":article_author, "article day": article_day, "article month": article_month, "article year":article_year, "friendly publication date": pub_date, "article summary":short_summary_text})

    return incoming_articles

articles_scraped = getArticles("https://www.inthelibrarywiththeleadpipe.org/")

print(articles_scraped)
# Append the results to a JSON file
filename = "lead_pipe_List.json"
with open(filename, 'a') as f:
    json.dump(articles_scraped, f)

# Append results into a CSV file with headers
updater = "lead_pipe_List.csv"
field_names=["article url", "article title", "article author", "article day", "article month", "article year", "friendly publication date", "article summary"]

with open(updater, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(articles_scraped)

