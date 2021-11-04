from abc import ABC, abstractmethod
from typing import List
import praw
import os
import feedparser
from praw.reddit import Reddit

CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')


class Source(ABC):
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch(self):
        pass


class RedditSource(Source):

    def __init__(self) -> None:
        self.results = []
        self.valid_metrics = ['hot', 'top']
        self.reddit_con = self.connect()


    def connect(self) -> Reddit:
        self.reddit_con = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     grant_type_access='client_credentials',
                     user_agent='script/1.0')
        return self.reddit_con


    def fetch(self, subreddit: str, limit: int = 10, metric: str = 'hot') -> List:
        """
        @param subreddit: Name of the subreddit to fetch from
        @param limit: Limit the amount of links to fetch (default: 10)
        @param metric: Fetch by a specific metric; valid values: 'hot' \ 'top' (default: 'hot')
        """
        
        if not subreddit:
            return
        if limit < 0:
            return
        if metric not in self.valid_metrics:
            return
        
        if metric == 'hot':
            self.results = self.reddit_con.subreddit(subreddit).hot(limit=limit)
        else:
            self.results = self.reddit_con.subreddit(subreddit).top(limit=limit)

        return self.results


    def __repr__(self) -> str:
        output = ""
        for submission in self.results:
            output += str(vars(submission)['title']) + " : " + str(vars(submission)['url']) + "\n"
        return output


class MediumSource(Source):
    
    def __init__(self) -> None:
        self.results = []

    def connect(self):
        pass

    def fetch(self, tag: str, limit: int = 10):
        """
        @param subreddit: Name of the tag to fetch from
        @param limit: Limit the amount of links to fetch (default: 10)
        """
        if not tag:
            return
        if limit < 0:
            return

        self.results = feedparser.parse(f"https://medium.com/feed/tag/{tag}").entries[:limit]

    def __repr__(self) -> str:
        output = ""
        for submission in self.results:
            output += str(submission.title) + " : " + str(submission.link) + "\n"
        return output


if __name__ == '__main__':
    assert CLIENT_ID, CLIENT_SECRET
    reddit_top_programming = RedditSource()
    reddit_top_programming.fetch(subreddit='programming', limit=10, metric='top')
    print(reddit_top_programming)

    medium_programming = MediumSource()
    medium_programming.fetch(tag='programming', limit=10)
    print(medium_programming)