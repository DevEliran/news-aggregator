from typing import List
from models import  Source
from reddit_source import RedditSource
from medium_source import MediumSource


class SourceManager:
    def __init__(self, sources: List[Source]) -> None:
        self.sources = sources

    def __call__(self) -> None:
        for source in self.sources:
            source.fetch()
            print(source)


if __name__ == '__main__':
    source_manager = SourceManager(
        [
            RedditSource(subreddit='programming', limit=10, metric='top'),
            RedditSource(subreddit='showerthoughts', limit=3, metric='hot'),
            MediumSource(tag='programming', limit=5)
        ]
    )
    source_manager()