'''

    acquire_news_articles.py

    Description: This file contains a class that can be used for acquiring
        news articles from inshorts.com.

        Example: df = AcquireNewsArticles().get_data(categories)

    Class:

        AcquireNewsArticles

    Class Fields:

        file_name

    Class Methods:

        __init__(self, file_name = 'inshorts_articles.csv')
        read_from_source(self)
        get_news_articles(self, categories)
        get_category_links(self, category)
        get_article_info(self, url, category)

'''

################################################################################

import requests

import pandas as pd
from bs4 import BeautifulSoup

from _acquire import Acquire

################################################################################

class AcquireNewsArticles(Acquire):

    ################################################################################

    def __init__(self, file_name: str = 'inshorts_articles.csv'):
        self.file_name = file_name

    ################################################################################

    def read_from_source(self):
        return self.get_news_articles([
            'business',
            'sports',
            'technology',
            'entertainment'
        ])

    ################################################################################

    def get_news_articles(self, categories):
        articles = []

        for category in categories:
            for link in self.get_category_links(category):
                articles.append(self.get_article_info(link, category))

        return pd.DataFrame(articles)

    ################################################################################

    def get_category_links(self, category):
        links = []
        base_domain = 'https://inshorts.com'
        url = f'{base_domain}/en/read/{category}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for card in soup.find_all('div', class_ = 'news-card-title'):
            links.append(base_domain + card.find('a')['href'])
            
        return links

    ################################################################################

    def get_article_info(self, url, category):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return {
            'title' : soup.find('div', class_ = 'news-card-title').find('span').text,
            'content' : soup.find('div', class_ = 'news-card-content').find('div').text,
            'category' : category
        }