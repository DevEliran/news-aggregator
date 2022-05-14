import os
from typing import List
import praw
from praw.reddit import Reddit
from colorama import Fore, Style

from src.models import Source, Result

CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')

REDDIT_VALID_METRICS = ['hot', 'top']

"""
RedditSource module, responsible for querying Reddit's API.
"""


def reformat_results(raw_results) -> List[Result]:
    """
    Transforming Reddit's API raw results into the Result class
    """
    reformatted_results = []
    for result in raw_results:
        reformatted_results.append(
            Result(
                title=vars(result)['title'],
                url=vars(result)['url']
            )
        )
    return reformatted_results


class RedditSource(Source):
    """
    RedditSource class accepts a subreddit, metric, limit and credentials
    for API access.
    Queries Reddit's API based on the subreddit and metric specified.
    """
    def __init__(self, subreddit: str, limit: int = 10, metric: str = 'hot',
                 reddit_id: str = None, reddit_secret: str = None) -> None:
        """
        Initializes the empty results list, connection to the API and given
        attributes.
        """
        self.results: List[Result] = []
        self.subreddit = subreddit
        self.limit = limit
        self.metric = metric
        self.reddit_id = reddit_id
        self.reddit_secret = reddit_secret
        self.reddit_con = self.connect()

    def connect(self) -> Reddit:
        """
        Connects to Reddit's API with the credentials given.
        """
        reddit_id = self.reddit_id if self.reddit_id else CLIENT_ID
        reddit_secret = self.reddit_secret if \
            self.reddit_secret else CLIENT_SECRET

        self.reddit_con = praw.Reddit(client_id=reddit_id,
                                      client_secret=reddit_secret,
                                      grant_type_access='client_credentials',
                                      user_agent='script/1.0')
        return self.reddit_con

    def fetch(self) -> List[Result]:
        """
        Retrieves posts from Reddit's API based on the subreddit and metric.
        """
        if not self.subreddit or self.limit < 0 or \
                self.metric.lower() not in REDDIT_VALID_METRICS:
            return []

        if self.metric == 'hot':
            raw_results = self.reddit_con.subreddit(self.subreddit).hot(
                limit=self.limit)
        else:
            raw_results = self.reddit_con.subreddit(self.subreddit).top(
                limit=self.limit)

        self.results = reformat_results(raw_results)

        return self.results

    def __repr__(self) -> str:
        """
        RedditSource string representation
        """
        output = f"{Fore.GREEN}Reddit Source Results [Sub: {self.subreddit}," \
                 f" Metric: {self.metric}]{Style.RESET_ALL} \n"
        for result in self.results:
            output += f"{result} \n"
        return output
