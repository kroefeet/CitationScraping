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

def getArticles(url):
    # This chunk grabs all the HTML from the url passed as an argument"
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    f = urlopen(request_site)
    soup_page_html = str(f.read())
    f.close

    # This statement takes the HTML and passes it to the Beautiful Soup parser
    page_soup = soup(soup_page_html, 'html.parser')

    # This variable should grab all of the HTML that contains the group of items you are looking for
    results = page_soup.find("", class_="")
    #print(results)

    # This variable should identify each individual article chunk that you want to capture
    articles = results.find_all("", class_="")
    #print(articles)

    # This empty list will hold the data from each article to put in a JSON and in a CSV at the end
    incoming_articles = []

    # This for loop will analyze each article chunk to look for the data you want to capture
    for i, article in enumerate(articles):
        # uncomment the print statement below to print the counter to the console
        #print(i)
        # this variable should capture the HTML containing the title and the link to the article
        article_main = article.find("", class_="")
        # this variable will take just the text from the HTML captured above
        article_title = article_main.text
        #print(article_title)
        # this variable will grab the a tag from the HTML chunk captured in article.main
        article_link = article_main.find("")
        # this variable grabs only the url and drops the rest
        article_url = article_link.get("")
        #print(article_url)
        # this variable will grab the HTML containing the author's name
        article_author_main = article.find("", class_="")
        # this grabs just the text and drops the remainder of the HTML to keep just the name of the author
        article_author = article_author_main.text
        #print(article_author)
        # this variable captures the HTML containing the day of the month
        article_daynum = article.find("", class_="")
        # this variable captures just the text from the day of the month HTML
        article_day = article_daynum.text
        #print(article_day.text)
        # this variable captures year and month due to quirk in CSS for this site
        article_year_month = article.find_all("", class_="")
        # this variable returns a list so we need to separate the year from the month by using a list index
        #print(article_month[0].text)
        article_year = article_year_month[0].text
        article_month = article_year_month[1].text
        # this variable takes the pulled apart date and assembles in into a wikidata friendly version
        pub_date = article_day +" "+ article_year +" "+ article_month
        #print(pub_date)
        # this variable will grab the HTML of the clipped summary that is displayed
        short_summary = article.find("", class_="")
        # this variable will take just the text of that HTML summary
        short_summary_text = short_summary.text
        #print(short_summary_text)

        # this takes the individual article information and appends it to our previously empty list before moving on to the next article
        incoming_articles.append({"article url":article_url, "article title":article_title, "article author":article_author, "article day": article_day, "article month": article_month, "article year":article_year, "friendly publication date": pub_date, "article summary":short_summary_text})

    # this makes it so this whole function makes the resulting list of article items (as dictionaries) available for processing into a usable file format
    return incoming_articles

# this line calls the function on whatever URL is put in the parenthesis
articles_scraped = getArticles("https://www.inthelibrarywiththeleadpipe.org/")

# this prints the entire list of articles scraped
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
