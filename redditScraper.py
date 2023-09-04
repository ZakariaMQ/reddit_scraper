import sqlite3
from requests import get

class ScrapeSubReddits:
    """
    class to scrape subreddits and save them in SQL DB
    It saves the following data
    post_id, title, score, author, date, url
    instense take 2 params
    subreddit=name of subreddit to scrape
    DBname=name of the database to save scraped data
    ----------
    method scrape take 1 optional param
    sort= either "hot" or "top" It will scrape posts based on sort arg
    default is "hot"
    """

    def __init__(self, subreddit:str, DBname:str) -> None:
        
        if not DBname.endswith(".db"):
            DBname += ".db"
        
        self._connect   = sqlite3.connect(DBname)
        self._cursor    = self._connect.cursor()
        self.subreddit  = subreddit

    
    def __create_tables(self):
        self._connect.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                title TEXT,
                score INTEGER,
                author TEXT,
                date REAL,
                associatedUrl TEXT
            )
        ''')
        self._connect.commit()
    

    def __to_db(self, post_id, title, score, author, date, url):
        c = self._cursor
        c.execute('INSERT OR IGNORE INTO posts VALUES (?,?,?,?,?,?)',
                        (post_id, title, score, author, date, url))
        

    def __parse(self, subreddit, after='', sort:str="hot"):
        
        if sort not in ["top", "hot"]:
            raise ValueError(f"sort must be 'hot'/'top'")

        params = f'&after={after}' if after else ''
        url = f'https://www.reddit.com/r/{subreddit}/{sort}.json?t=year{params}&limit=100'
        headers = {
            'User-Agent': 'CODE'
        }
    

        try:
            response = get(url, headers=headers)

        except Exception as e:
            print(f'Exception: {e}')
            pass

        if response.ok:
            
            data = response.json()['data']
            
            for post in data['children']:
                pdata   = post['data']
                post_id = pdata['id']
                title   = pdata['title']
                score   = pdata['score']
                author  = pdata['author']
                date    = pdata['created_utc']
                url     = pdata.get('url_overridden_by_dest')
                __class__.__to_db(self, post_id, title, score, author, date, url)
            
            self._connect.commit()
            print(f"{len(data['children'])} posts from '{self.subreddit}' have been scraped")
            return data['after'], len(data['children'])
        
        else:
            print(f'Error {response.status_code}')
            return None
        
    
    def scrape(self, sort:str='hot'):

        subreddit = self.subreddit
    
        __class__.__create_tables(self)
        all_scraped_posts = 0
        after = ""
        
        try:
            while True:

                after, len_data = __class__.__parse(self, subreddit, after, sort=sort)


                all_scraped_posts += len_data
                
                if not after:
                    break

        except KeyboardInterrupt:
            print('Exiting...')
        finally:
            self._connect.close()
            print(f"total posts have been scraped from '{self.subreddit}' => {all_scraped_posts} POSTS")
            print(f"-"*50)