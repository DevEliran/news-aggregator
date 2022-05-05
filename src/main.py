import argparse
import logging
from typing import List
from models import  Source
from reddit_source import RedditSource
from medium_source import MediumSource
import sys


class SourceManager:
    def __init__(self, sources: List[Source]) -> None:
        self.sources = sources

    def __call__(self) -> None:
        for source in self.sources:
            source.fetch()
            print(source)


def normalize_args(args):
    if args["--reddit"] and not args["--sub"]:
        logging.error("detected --reddit flag without --sub flag")
        raise
    if args["--medium"] and not args["--tag"]:
        logging.error("detected --medium flag without --tag flag")
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reddit', action='store_true', type=bool)
    parser.add_argument('--sub', action='store', type=str)
    parser.add_argument('--metric', action='store', type=str)

    parser.add_argument('--medium', action='store_true', type=bool)
    parser.add_argument('--tag', action='store', type=str)

    parser.add_argument('--limit', action='store', type=int)

    try:
        args = normalize_args(parser.parse_args())
    except Exception:
        logging.info("Unable to parse settings, turn on LOG_LEVEL=ERROR for a detailed log")
        sys.exit(1)




    source_manager = SourceManager(
        [
            RedditSource(subreddit='programming', limit=10, metric='top'),
            RedditSource(subreddit='showerthoughts', limit=3, metric='hot'),
            MediumSource(tag='programming', limit=5)
        ]
    )
    source_manager()