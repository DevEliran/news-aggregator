import argparse
import logging
from typing import List

from numpy import source
from models import  Source
from reddit_source import RedditSource
from medium_source import MediumSource
import sys


class SourceManager:
    def __init__(self, sources: List[Source] = None) -> None:
        if not sources:
            self.sources = []
        else:
            self.sources = sources

    def __call__(self) -> None:
        for source in self.sources:
            source.fetch()
            print(source)

    def add(self, source: Source) -> None:
        self.sources.append(source)


def normalize_args(args):
    print(args)
    if args["reddit"] and not args["sub"]:
        logging.error("detected --reddit flag without --sub flag")
        raise
    if args["medium"] and not args["tag"]:
        logging.error("detected --medium flag without --tag flag")
        raise
    if args["sub"] and not args["metric"]:
        logging.error("detected --sub flag without --metric flag")
        raise
    if args["metric"] and not args["sub"]:
        logging.error("detected --metric flag without --sub flag")
        raise
    if args["metric"] and args["sub"] and len(args["metric"]) != len(args["sub"]):
        logging.error("every subreddit should have a metric specified")
        raise
    
    return args

def create_sources_from_args(args) -> List[Source]:
    sources = []

    if args['reddit']:
        for subreddit, metric in zip(args['sub'], args['metric']):
            reddit_source = RedditSource(
                subreddit=subreddit,
                limit=args["limit"],
                metric=metric
            )
            sources.append(reddit_source)

    if args["medium"]:
        for tag in args['tag']:
            medium_source = MediumSource(
                tag=tag,
                limit=args['limit']
            )
            sources.append(medium_source)

    return sources



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reddit', action='store_true')
    parser.add_argument('--sub', action='append', type=str)
    parser.add_argument('--metric', action='append', type=str)

    parser.add_argument('--medium', action='store_true')
    parser.add_argument('--tag', action='append', type=str)

    parser.add_argument('--limit', action='store', type=int, default=10)

    try:
        args = normalize_args(vars(parser.parse_args()))
    except Exception as e:
        print(e)
        logging.info("Unable to parse settings, turn on LOG_LEVEL=ERROR for a detailed log")
        sys.exit(1)

    sources = create_sources_from_args(args)
    source_manager = SourceManager(sources)
    source_manager()


    # source_manager = SourceManager(
    #     [
    #         RedditSource(subreddit='programming', limit=10, metric='top'),
    #         RedditSource(subreddit='showerthoughts', limit=3, metric='hot'),
    #         MediumSource(tag='programming', limit=5)
    #     ]
    # )
    # source_manager()