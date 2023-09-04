# reddit_scraper
# Reddit Subreddit Scraper

## Getting Started
This Python script is designed to scrape posts from a Reddit subreddit and save them to a SQLite database. It allows you to collect data such as post ID, title, score, author, date, and associated URL.


### Prerequisites

Before using this script, you need to have Python installed on your system. You also need to install the required packages by running:


### Usage

1. Clone this repository to your local machine
2. Navigate to the project directory:
3. Run the script, specifying the subreddit name and the name of the SQLite database where you want to save the scraped data:


### Database

The script creates an SQLite database with a table named "posts" to store the scraped data. The table schema is as follows:

- `id` (TEXT): The post's unique ID.
- `title` (TEXT): The title of the post.
- `score` (INTEGER): The post's score.
- `author` (TEXT): The post's author.
- `date` (REAL): The date the post was created (UTC timestamp).
- `associatedUrl` (TEXT): The URL associated with the post.


## Author

- [SeasonedCode](https://github.com/yourusername)
