from abc import ABC, abstractmethod
from typing import List
import praw
import os
import feedparser
from praw.reddit import Reddit
from models import Result

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

    def __init__(self, subreddit: str, limit: int = 10, metric: str = 'hot') -> None:
        self.results: List[Result] = []
        self.valid_metrics = ['hot', 'top']
        self.reddit_con = self.connect()
        self.subreddit = subreddit
        self.limit = limit
        self.metric = metric

    def connect(self) -> Reddit:
        self.reddit_con = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     grant_type_access='client_credentials',
                     user_agent='script/1.0')
        return self.reddit_con


    def fetch(self) -> List:
        """
        @param subreddit: Name of the subreddit to fetch from
        @param limit: Limit the amount of links to fetch (default: 10)
        @param metric: Fetch by a specific metric; valid values: 'hot' \ 'top' (default: 'hot')
        """
        
        if not self.subreddit or self.limit < 0 or self.metric.lower() not in self.valid_metrics:
            return
        
        if self.metric == 'hot':
            raw_results = self.reddit_con.subreddit(self.subreddit).hot(limit=self.limit)
        else:
            raw_results = self.reddit_con.subreddit(self.subreddit).top(limit=self.limit)

        self.results = self.reformat_results(raw_results)

        return self.results


    def reformat_results(self, raw_results) -> List[Result]:
        reformatted_results = []
        for result in raw_results:
            reformatted_results.append(
                Result(
                    title=vars(result)['title'],
                    url=vars(result)['url']
                )
            )
        return reformatted_results


    def __repr__(self) -> str:
        output = f"Reddit Source Results [Sub:{self.subreddit}, Metric: {self.metric}] \n"
        for result in self.results:
            output += str(result) + "\n"
        return output


class MediumSource(Source):
    
    def __init__(self, tag, limit=10) -> None:
        self.results: List[Result] = []
        self.tag = tag
        self.limit = limit

    def connect(self):
        pass

    def fetch(self):
        """
        @param subreddit: Name of the tag to fetch from
        @param limit: Limit the amount of links to fetch (default: 10)
        """
        if not self.tag or self.limit < 0:
            return

        raw_results = feedparser.parse(f"https://medium.com/feed/tag/{self.tag}").entries[:self.limit]

        self.results = self.reformat_results(raw_results)
        return self.results

    def reformat_results(self, raw_results) -> List[Result]:
        results = []
        for result in raw_results:
            results.append(
                Result(
                    title=result.title,
                    url=result.link
                )
            )

        return results

    def __repr__(self) -> str:
        output = f"Medium Source Results [Tag: {self.tag}] \n"
        for result in self.results:
            output += str(result) + "\n"
        return output


class SourceManager:
    def __init__(self, sources: List[Source]) -> None:
        self.sources = sources

    def __call__(self) -> None:
        for source in self.sources:
            source.fetch()
            print(source)


if __name__ == '__main__':
    assert CLIENT_ID, CLIENT_SECRET
    source_manager = SourceManager(
        [
            RedditSource(subreddit='programming', limit=10, metric='top'),
            MediumSource(tag='programming', limit=5)
        ]
    )
    source_manager()