'''

    acquire_codeup_blog.py

    Description: This file contains a class that can be used for acquiring 
        all Codeup blog articles. 

        Example: df = AcquireCodeupBlog().get_data()

    Class:

        AcquireCodeupBlog

    Class Fields:

        file_name

    Class Methods:

        

'''

################################################################################

import requests

import pandas as pd
from bs4 import BeautifulSoup

from _acquire import Acquire

################################################################################

class AcquireCodeupBlog(Acquire):

    ################################################################################

    def __init__(self, file_name = 'codeup_blog.csv'):
        self.file_name = 'codeup_blog.csv'

    ################################################################################

    def read_from_source(self):
        return pd.DataFrame(self.get_all_blog_articles())

    ################################################################################

    def get_all_blog_articles(self):
        url = 'https://codeup.com/blog/'
        links = self.get_all_article_links(url)
        return self.get_blog_articles(set(links))

    ################################################################################

    def get_all_article_links(self, url):
        links = []
        headers = {'user-agent' : 'Innis Data Science Cohort'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for article in soup.find_all('article'):
            links.append(article.find('a')['href'])
            
        if (link := soup.find('a', string = '« Older Entries')):
            links += self.get_all_article_links(link['href'])
        
        return links

    ################################################################################

    def get_blog_articles(self, urls):
        articles = []
        headers = {'user-agent' : 'Innis Data Science Cohort'}
        
        for url in urls:
            try:
                response = requests.get(url, headers = headers)
            except requests.exceptions.RequestException:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if url == response.url:
                articles.append(self.get_article_info(soup))
            
        return articles

    ################################################################################

    def get_article_info(self, soup):
        return {
            'title' : soup.find('h1', class_ = 'entry-title').text,
            'date' : soup.find('p', class_ = 'post-meta').find('span').text,
            'content' : soup.find('div', class_ = 'entry-content').text.strip()
        }