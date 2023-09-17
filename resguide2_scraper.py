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
    url =  "https://sis.wayne.edu/diversity/literature-on-diversity"
    request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    f = urlopen(request_site)
    soup_page_html = str(f.read())
    f.close

    # This statement takes the HTML and passes it to the Beautiful Soup parser
    page_soup = soup(soup_page_html, 'html.parser')
    #print(page_soup)
    
    results = page_soup.find("div", class_="content")
    #print(results)
    
    articles = results.find_all("p", class_="")
    #print(articles)
    
    incoming_articles = []
    item_data = 0
    item_summary = 0
    for i, article in enumerate(articles):
        print(i)
        list_content = article.text.strip()
        #print(list_content)
        #print(len(list_content))

        if len(list_content) > 0:
            #print(list_content)
            article_url = article.find("a")
            article_dict = {}
            if i % 4 == 0:
                #print(f'This is a summary')
                item_summary += 1
                article_no = "article_" + str(item_summary)
                article_dict['article_number'] = article_no
                #print(f'this is the article {article_no}')
            else:
                #print(f'This is not a summary')
                item_data += 1
                article_no = "article_" + str(item_data)
                article_dict['article_number'] = article_no
                #print(f'this is the article {article_no}')
            if article_url:
                article_information = list_content
                article_link = article_url.get("href")
                article_dict['article_link'] = article_link
                #print(f'The link to the article is {article_link}')
                #print(f'The information about this article is {article_information}')
                article_dict['article_info'] = article_information
                match_citation = re.match(r'(\D+, \D+\s?\&?)\s?\((\d{4})\)\. (.+)\. ([\D:]+), (\d{1,4})\s?\((.+)\), (\d+-?\d*)\.?',article_information)
                #print(match_citation)
                if match_citation:
                    authors = match_citation.group(1)
                    article_dict['article_authors'] = authors
                    #print(f'these are the authors {authors}')
                    pub_year = match_citation.group(2)
                    article_dict['article_year'] = pub_year
                    #print(f'this is the year of publication {pub_year}')
                    article_title = match_citation.group(3)
                    article_dict['article_title'] = article_title
                    #print(f'this is the article title {article_title}')
                    publication = match_citation.group(4)
                    article_dict['article_publication'] = publication
                    #print(f'this is the publication {publication}')
                    vol_num = match_citation.group(5)
                    article_dict['article_volume'] = vol_num
                    #print(f'this is the volume number {vol_num}')
                    iss_num = match_citation.group(6)
                    article_dict['article_issue'] = iss_num
                    #print(f'this is the issue number {iss_num}')
                    pages = match_citation.group(7)
                    article_dict['article_pages'] = pages
                    #print(f'this is the page number {pages}')
                    
                else:
                    print(f'there is a problem parsing this citation')
            
            else:
                article_summary = list_content
                #print(f'This is either a summary or information without a URL')
                article_dict['article_summary'] = article_summary
                #print(article_summary)
            #print(article_dict)
            incoming_articles.append(article_dict)
            

    return incoming_articles


articles_scraped = getArticles()


print(articles_scraped)
# Append the results to a JSON file
filename = "resguide2_List.json"
with open(filename, 'a') as f:
    json.dump(articles_scraped, f)


# Append results into a CSV file with headers
updater = "resguide2_List.csv"
field_names=["article_number", "article_info", "article_link", "article_authors", "article_year", "article_title", "article_publication", "article_volume", "article_issue", "article_pages", "article_summary"]

with open(updater, 'a') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(articles_scraped)
