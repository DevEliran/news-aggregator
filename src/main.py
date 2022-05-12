import argparse
import logging
from typing import List

from src.hn_source import HackerNewsSource
from src.models import Source, SourceManager
from src.reddit_source import RedditSource
from src.medium_source import MediumSource
import sys
import os

from util.banner import banner as fuse_banner


def run(banner: str = fuse_banner, argv: List[str] = sys.argv[1:]):
    config = create_config(argv)

    try:
        normalize_config(config)
    except ValueError:
        logging.info("Unable to parse arguments, set LOG_LEVEL=ERROR for a "
                     "detailed error log")
        sys.exit(1)

    print(banner)
    parsed_sources = create_sources_from_args(config)
    source_manager = SourceManager(parsed_sources)
    source_manager()


def create_config(argv):
    parser = argparse.ArgumentParser(description="Content aggregation CLI")
    add_parser_args(parser)
    config = parser.parse_args(argv)

    return config


def normalize_config(config):
    if config.reddit and not config.sub:
        logging.error("detected --reddit flag without --sub flag")
        raise ValueError("bad config")

    if config.reddit and not config.reddit_id or \
            config.reddit and not config.reddit_secret:
        if not os.environ.get('REDDIT_CLIENT_ID') or not \
                os.environ.get('REDDIT_CLIENT_SECRET'):
            logging.error("Unable to initiate reddit source - no credentials "
                          "passed, see --reddit-id and --reddit-secret "
                          "arguments")
            raise ValueError("bad config")

    if config.medium and not config.tag:
        logging.error("detected --medium flag without --tag flag")
        raise ValueError("bad config")

    if config.sub and not config.metric:
        logging.error("detected --sub flag without --metric flag")
        raise ValueError("bad config")

    if config.metric and not config.sub:
        logging.error("detected --metric flag without --sub flag")
        raise ValueError("bad config")

    if config.metric and config.sub and len(config.metric) != len(
            config.sub):
        logging.error("every subreddit should have a metric specified")
        raise ValueError("bad config")

    return config


def create_sources_from_args(config) -> List[Source]:
    sources = []

    if config.reddit:
        for subreddit, metric in zip(config.sub, config.metric):
            reddit_source = RedditSource(
                subreddit=subreddit,
                limit=config.limit,
                metric=metric,
                reddit_id=config.reddit_id,
                reddit_secret=config.reddit_secret
            )
            sources.append(reddit_source)

    if config.medium:
        for tag in config.tag:
            medium_source = MediumSource(
                tag=tag,
                limit=config.limit
            )
            sources.append(medium_source)

    if config.hn:
        for metric in config.hn_metric:
            hn_source = HackerNewsSource(
                metric=metric,
                limit=config.limit
            )
            sources.append(hn_source)

    return sources


def add_parser_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--reddit', action='store_true')
    parser.add_argument('--sub', action='append', type=str)
    parser.add_argument('--metric', action='append', type=str)
    parser.add_argument('--reddit_id', action='store', type=str)
    parser.add_argument('--reddit_secret', action='store', type=str)

    parser.add_argument('--medium', action='store_true')
    parser.add_argument('--tag', action='append', type=str)

    parser.add_argument('--hn', action='store_true')
    parser.add_argument('--hn_metric', action='append', default=['top'])

    parser.add_argument('--limit', action='store', type=int, default=10)


if __name__ == '__main__':
    sys.exit(run())
