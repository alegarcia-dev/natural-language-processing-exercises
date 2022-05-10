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

        __init__(self, file_name = 'codeup_blog.csv')
        read_from_source(self)
        get_all_article_links(self, url)
        get_blog_articles(self, urls)
        get_article_info(self, soup)

'''

################################################################################

import requests

import pandas as pd
from bs4 import BeautifulSoup

from _acquire import Acquire

################################################################################

class AcquireCodeupBlog(Acquire):

    '''
        A class used for acquiring the Codeup blog articles from the Codeup 
        website.
    
        Instance Fields
        ---------------
        file_name: str
    
        Instance Methods
        ----------------
        __init__: Returns None
        read_from_source: Returns DataFrame
        get_all_article_links: Returns list[str]
        get_blog_articles: Returns list[dict]
        get_article_info: Returns dict
    '''

    ################################################################################

    def __init__(self, file_name: str = 'codeup_blog.csv'):
        '''
            Parameters
            ----------
            file_name: str, optional
                The file name to use when cacheing the data. Default value is 
                "codeup_blog.csv".
        '''

        self.file_name = file_name

    ################################################################################

    def read_from_source(self) -> pd.DataFrame:
        '''
            Acquire the Codeup blog articles data from the source (Codeup website).
            Return a dataframe containing the data.
        
            Returns
            -------
            DataFrame: A dataframe containing the title, date, and content for 
                all Codeup blog articles.
        '''

        url = 'https://codeup.com/blog/'
        links = self.get_all_article_links(url)

        # Remove all duplicates by turning the list into a set and return as a dataframe.
        return pd.DataFrame(self.get_blog_articles(set(links)))

    ################################################################################

    def get_all_article_links(self, url: str) -> list[str]:
        '''
            Recursively acquire the links to all Codeup blog posts and return 
            a list containing all the URLs. This function will recursively 
            call itself until it reaches the final page of blog articles.
        
            Parameters
            ----------
            url: str
                The URL of the blog page containing links to Codeup blog posts.
        
            Returns
            -------
            list[str]: A list of URLs linking to all Codeup blog posts.
        '''

        # Set the header so we can have access to scrape the Codeup website and acquire the HTML code
        headers = {'user-agent' : 'Innis Data Science Cohort'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # For each article element on the page get the href attribute of the link element.
        # Create a list of all the URLs.
        links = [article.find('a')['href'] for article in soup.find_all('article')]
            
        # If an Older Entries link exists on the page, call this function again with that URL.
        # Add the returned list to the list of links.
        if (link := soup.find('a', string = '« Older Entries')):
            links += self.get_all_article_links(link['href'])
        
        return links

    ################################################################################

    def get_blog_articles(self, urls: list[str]) -> list[dict]:
        '''
            Acquire the article info for all the URLs provided and return as a 
            list of dictionaries.
        
            Parameters
            ----------
            urls: list[str]
                A list of URLs to scrape.
        
            Returns
            -------
            list[dict]: A list of dictionaries containing the article info for 
                each article linked by the provided URLs.
        '''

        articles = []

        # Set the headers so we have access to scrape the Codeup website.
        headers = {'user-agent' : 'Innis Data Science Cohort'}
        
        for url in urls:

            # Attempt to get a response from the server. If something goes 
            # wrong skip ahead to the next URL.
            try:
                response = requests.get(url, headers = headers)
            except requests.exceptions.RequestException:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Make sure the URL that we received is the same as the one we sent the request
            # for, in case the server redirects us.
            if url == response.url:
                articles.append(self.get_article_info(soup))
            
        return articles

    ################################################################################

    def get_article_info(self, soup: BeautifulSoup) -> dict:
        '''
            Return a dictionary containing the title, date, and content of the 
            Codeup blog post used to create the BeautifulSoup object soup.
        
            Parameters
            ----------
            soup: BeautifulSoup
                A BeautifulSoup object that was created using the requests 
                response from a Codeup blog article.
        
            Returns
            -------
            dict: A dictionary containing the title, date, and content of a 
                Codeup blog article.
        '''

        return {
            'title' : soup.find('h1', class_ = 'entry-title').text,
            'date' : soup.find('p', class_ = 'post-meta').find('span').text,
            'content' : soup.find('div', class_ = 'entry-content').text.strip()
        }