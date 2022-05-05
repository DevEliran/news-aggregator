from models import Source, Result
from typing import List
import praw
from praw.reddit import Reddit
import os
from colorama import Fore, Style

CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')

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
        output = f"{Fore.GREEN}Reddit Source Results [Sub:{self.subreddit}, Metric: {self.metric}]{Style.RESET_ALL} \n"
        for result in self.results:
            output += f"{result} \n"
        return output