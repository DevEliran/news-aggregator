from fastapi import FastAPI

from src.aws_blog_source import AwsBlogSource
from src.hn_source import HackerNewsSource
from src.medium_source import MediumSource
from src.reddit_source import RedditSource

app = FastAPI()


def get_results_dict(source):
    return {
        'posts': {
            result.title: result.url for result in source.results
        }
    }


@app.get('/')
def root():
    return {}


@app.get('/reddit/{subreddit}/{metric}')
def get_reddit_posts(subreddit: str, metric: str, limit: int = 10):
    reddit = RedditSource(
        subreddit=subreddit,
        metric=metric,
        limit=limit
    )
    reddit.fetch()

    return get_results_dict(reddit)


@app.get('/medium/{tag}')
def get_medium_posts(tag: str, limit: int = 10):
    medium = MediumSource(
        tag=tag,
        limit=limit
    )
    medium.fetch()

    return get_results_dict(medium)


@app.get('/hackernews/{metric}')
def get_hackernews_posts(metric: str, limit: int = 10):
    hackernews = HackerNewsSource(
        metric=metric,
        limit=limit
    )
    hackernews.fetch()

    return get_results_dict(hackernews)


@app.get('/aws/{category}')
def get_aws_posts(category: str, limit: int = 10):
    aws = AwsBlogSource(
        category=category,
        limit=limit
    )
    aws.fetch()

    return get_results_dict(aws)
