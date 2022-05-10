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

    '''
        A class used for acquiring news article data from inshorts.com.
    
        Instance Fields
        ---------------
        file_name: str
    
        Instance Methods
        ----------------
        __init__: Returns None
        read_from_source: Returns DataFrame
        get_news_articles: Returns DataFrame
        get_category_links: Returns list[str]
        get_article_info: Returns dict
    '''

    ################################################################################

    def __init__(self, file_name: str = 'inshorts_articles.csv'):
        '''
            Parameters
            ----------
            file_name: str
                The file name to use when cacheing the data.
        '''

        self.file_name = file_name

    ################################################################################

    def read_from_source(self) -> pd.DataFrame:
        '''
            Acquire the inshorts news articles data from the source.
        
            Parameters
            ----------
            parameter: parameter_type
                parameter_description
        
            Returns
            -------
            DataFrame: A dataframe containing the title, content, and category 
                for the categories business, sports, technology, and 
                entertainment.
        '''

        return self.get_news_articles([
            'business',
            'sports',
            'technology',
            'entertainment'
        ])

    ################################################################################

    def get_news_articles(self, categories: list[str]) -> pd.DataFrame:
        '''
            Return a dataframe containing the title, content, and category for 
            each news article in the provided categories.
        
            Parameters
            ----------
            categories: list[str]
                A list of categories to acquire data from on inshorts.com.
        
            Returns
            -------
            DataFrame: A dataframe containing the title, content, and caegory
                for each new article.
        '''

        articles = []

        # For each category, and each link in each category, get the article info that we need.
        for category in categories:
            for link in self.get_category_links(category):
                articles.append(self.get_article_info(link, category))

        return pd.DataFrame(articles)

    ################################################################################

    def get_category_links(self, category: str) -> list[str]:
        '''
            Get the links for all articles in the provided category page.
        
            Parameters
            ----------
            category: str
                The category page to scrape.
        
            Returns
            -------
            list[str]: A list of URLs containing links to all news articles on 
                the category page.
        '''

        # Build the URL we need to scrape and ping the server.
        base_domain = 'https://inshorts.com'
        url = f'{base_domain}/en/read/{category}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # For each news card acquire the link to the article and build the URL by adding the base domain to the link.
        links = [base_domain + card.find('a')['href'] for card in soup.find_all('div', class_ = 'news-card-title')]
            
        return links

    ################################################################################

    def get_article_info(self, url: str, category: str) -> dict:
        '''
            Return a dictionary containing the title, content, and category for 
            the provided news article URL.
        
            Parameters
            ----------
            url: str
                A URL linking to a news article.

            category: str
                The category of the news article.
        
            Returns
            -------
            dict: A dictionary containing the title, content, and category for 
                the news article.
        '''

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return {
            'title' : soup.find('div', class_ = 'news-card-title').find('span').text,
            'content' : soup.find('div', class_ = 'news-card-content').find('div').text,
            'category' : category
        }