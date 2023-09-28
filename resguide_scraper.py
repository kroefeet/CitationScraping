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
            match_citation = re.match(r'(\D+, \D+\s?\&?) \\xe2\\x80\\x9c(\D+)\s?\\xe2\\x80\\x9d\s?(\D+)\s?(\d+),\s?(no\.\s?\d+)\s?\((.+)\):\s?(\d+).*(https:.*)\.',article_cite)
            print(match_citation)
            if match_citation:
                    authors = match_citation.group(1)
                    article_authors = authors
                    #print(f'these are the authors {authors}')
                    title = match_citation.group(2)
                    article_title = title
                    #print(f'this is the article title {article_title}')
                    publication = match_citation.group(3)
                    article_publication = publication
                    #print(f'this is the publication {publication}')
                    vol_num = match_citation.group(4)
                    article_volume = vol_num
                    #print(f'this is the volume number {vol_num}')
                    iss_num = match_citation.group(5)
                    article_issue = iss_num
                    #print(f'this is the issue number {iss_num}')
                    pages = match_citation.group(7)
                    article_pages = pages
                    #print(f'this is the page number {pages}')
                    pub_date = match_citation.group(6)
                    article_date = pub_date
                    #print(f'this is the year of publication {pub_year}')
                    doi = match_citation.group(8)
                    article_doi = doi
                    #print(f'this is the article doi {article_doi}')
                    
                  
            else:
                    error_note = "there is a problem parsing this citation"
                    article_authors = error_note
                    article_title = error_note
                    article_publication = error_note
                    article_volume = error_note
                    article_issue = error_note
                    article_pages = error_note
                    article_date = error_note
                    article_doi = error_note
        else:
            article_cite = "no citation given"
            error_note = "this item has no citation"
            article_authors = error_note
            article_publication = error_note
            article_volume = error_note
            article_issue = error_note
            article_pages = error_note
            article_date = error_note
            article_doi = error_note
        

        incoming_articles.append({"article link":article_link, "article title":article_title, "article summary":article_abstract, "article citation":article_cite, "article authors":article_authors, "article title":article_title, "article publication":article_publication, "article volume":article_volume, "article issue":article_issue, "article pages":article_pages, "article date":article_date, "article doi":article_doi})

    return incoming_articles


articles_scraped = getArticles()


print(articles_scraped)
# Append the results to a JSON file
filename = "resguide_List.json"
with open(filename, 'a') as f:
    json.dump(articles_scraped, f)


# Append results into a CSV file with headers
updater = "resguide_List.csv"
field_names=["article link", "article title", "article summary", "article citation", "article authors", "article title", "article publication", "article volume", "article issue", "article pages", "article date", "article doi"]

with open(updater, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(articles_scraped)
