from redditScraper import ScrapeSubReddits

# Specify the subreddit and database name
subreddit_name = "programming"
database_name = "programming_posts.db"

# Create an instance of the ScrapeSubReddits class
scraper = ScrapeSubReddits(subreddit_name, database_name)

# Scrape posts from the "hot" section of the subreddit
scraper.scrape(sort="hot")