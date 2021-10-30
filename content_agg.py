from abc import ABC, abstractmethod
import praw
import os

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

    def connect(self):
        self.reddit_con = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     grant_type_access='client_credentials',
                     user_agent='script/1.0')
        return self.reddit_con

    def fetch(self):
        pass


class RedditHotProgramming(RedditSource):
    
    def __init__(self) -> None:
        self.reddit_con = super().connect()
        self.hot_submissions = []

    def fetch(self, limit: int):
        for submission in self.reddit_con.subreddit('programming').hot(limit=limit):
            self.hot_submissions.append(submission)

    def __repr__(self):
        urls = []
        for submission in self.hot_submissions:
            urls.append(vars(submission)['url'])
        return '\n'.join(urls)


if __name__ == '__main__':
    assert CLIENT_ID, CLIENT_SECRET
    reddit_top_programming = RedditHotProgramming()
    reddit_top_programming.fetch(limit=10)
    print(reddit_top_programming)