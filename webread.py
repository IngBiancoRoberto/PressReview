# This package contains the functions to read titles from news websites

# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import requests
from bs4 import BeautifulSoup
import re

# ## Repubblica

def generic_read(website_url):
    "Generic function for reading from websites"
    try:
        page_html = requests.get(website_url)
        page= BeautifulSoup(page_html.content,'html.parser')
        return page
    except:
        return []

def repubblica_read(website_url = 'https://www.repubblica.it/index.html',website_name='Repubblica',media=2,no_media=1):
    #
    websites, titles,links = [],[],[]
    
    # try to read the page
    page = generic_read(website_url)

    #
    if page == []:
        return websites, titles,links
    
    # last number is number of articles to extract
    fields = [['article','entry gs-morebuttons-container sequence-8 media-8',media],
              ['article','entry gs-morebuttons-container sequence-8 no-media',no_media]]

    
    for field in fields:
        arts = page.find_all(field[0],class_=field[1])
        # ensure the number of required articles does not exceed the number of articles available
        for k in range( min(len(arts),field[2]) ):
            head2 = arts[k].find('h2')
            # titles
            titles.append(head2.find('a').get_text().strip())
            # links
            links.append(head2.find('a').get('href'))
    
    # website
    websites = [website_name for _ in range(len(titles))]
    
    #
    return websites, titles, links


# ## Corriere

def get_multiline_text(inp):
    "Reads article text if the href text is spread in different hyperlinks"
    subt = ''

    for xx in inp.find_all('a'):
        elem = xx.get_text().strip()
        if elem == '':
            elem = ' '
        subt=subt+elem

    return subt


def corriere_read(website_url = 'http://corriere.it',website_name='Corriere',xmedium=2,medium=1):

    websites, titles,links = [],[],[]
    
    page = generic_read(website_url)

    #
    if page == []:
        return websites, titles,links

    fields = [["title-art-hp is-xmedium is-line-h-106",xmedium],
              ["title-art-hp is-medium is-line-h-106",medium]]

    
    for field in fields:
        arts = page.find_all('h4', class_=field[0])
        for k in range( min(field[1],len(arts)) ):
            # titles
            #titles.append(arts[k].find('a').get_text().strip())
            titles.append( get_multiline_text(arts[k]) )
            # links
            links.append(arts[k].find('a').get('href'))

     # website
    websites = [website_name for _ in range(len(titles))]
    #
    return websites, titles, links

def bbcnews_read(website_url = 'https://www.bbc.co.uk', website_name = 'BBC News'):
    "reads from BBC News"
    # init
    websites, titles,links = [],[],[]

    #
    page = generic_read(website_url+'/news')
    if page == []:
        return websites,titles,links
    
    # Main article
    main_art = page.find('a',class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold nw-o-link-split__anchor')
    main_art_link = website_url + main_art.get('href')
    main_art_title = main_art.find('h3').get_text()
    # Secondary article
    sec_art = page.find('a',class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    sec_art_link= website_url + sec_art.get('href')
    sec_art_title = sec_art.find('h3').get_text()
    #
    websites = [website_name, website_name]
    titles = [main_art_title, sec_art_title]
    links = [main_art_link, sec_art_link]
    #
    return websites, titles, links

def sole24ore_read(website_url = 'https://www.ilsole24ore.com/',website_name = 'Sole 24 Ore',narts =2):
    # init
    websites, titles,links = [],[],[]

    #
    page = generic_read(website_url)
    if page == []:
        return websites,titles,links

    #
    all_articles = page.find_all('h3',class_='aprev-title')

    for k in range( min(narts,len(all_articles)) ):
        art = all_articles[k].find('a')
        titles.append(art.get_text())
        links.append(website_url+art.get('href'))

    websites = [website_name for _ in range(len(titles))]

    return websites,titles,links


def nytimes_read(website_url='https://www.nytimes.com',website_name='NY Times',narts=2):
    # init
    websites, titles,links = [],[],[]

    #
    page = generic_read(website_url)
    if page == []:
        return websites,titles,links
    #articles
    arts =page.find_all('article',class_='css-8atqhb')
    #
    k=0
    #collect info from articles
    for art in arts:
        span = art.find('span')
        if span != None:
            spantext = span.get_text().strip()
            if spantext != '':
                # append title
                titles.append(spantext)
                #find link
                links.append(website_url+ art.find('a').get('href'))
                k=k+1
        if k== min(narts, len(arts)):
            break
    #
    websites = [website_name for _ in range(len(titles))]
    #
    return websites,titles,links
