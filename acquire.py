'''

    acquire.py

    Description: This file contains all acquisition functions used for 
        natural language processing exercises.

    Variables:

        None

    Functions:

        get_codeup_blog()
        get_news_articles()

'''

################################################################################

from acquire_codeup_blog import AcquireCodeupBlog
from acquire_news_articles import AcquireNewsArticles

################################################################################

get_codeup_blog = lambda: AcquireCodeupBlog().get_data()
get_inshorts_articles = lambda: AcquireNewsArticles().get_data()