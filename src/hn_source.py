import asyncio
import logging
import os
from typing import List
import requests
from colorama import Fore, Style

from src.models import Source, Result


"""
HackerNews module, responsible for querying hackernews API.
"""


class HackerNewsSource(Source):
    """
    HackerNewsSource class accepts a metric from self.valid_metrics and a limit.
    Queries the HackerNews API with regarding to the specified metric and limit.
    """

    def __init__(self, metric: str = 'top', limit: int = 10):
        """
        Initiate valid metrics, base URL for API and an empty results list.
        """
        self.metric = metric
        self.limit = limit
        self.valid_metrics = ['top', 'best', 'new']
        self.base_url = 'https://hacker-news.firebaseio.com/v0'
        self.results: List[Result] = []

    def connect(self):
        """
        HackerNews API doesn't require an API key, hence there's no need to
        implement `connect`
        """
        pass

    def fetch(self) -> None:
        """
        Asynchronous Wrapper for the actual fetch mechanism `do_fetch`.
        """
        results = asyncio.run(self.do_fetch())
        self.results = results

    async def do_fetch(self) -> List[Result]:
        """
        Retrieves the stories ids based on a metric and then fetches each story
        details by the id
        """
        if self.limit < 0 or self.metric.lower() not in self.valid_metrics:
            return []

        request_url = f"{self.base_url}/{self.metric}stories.json"

        response = requests.get(request_url)
        response.raise_for_status()

        stories_ids = response.content[:self.limit]

        if os.getenv("PYCHARM_HOSTED") == "1":
            # PYCHARM_HOSTED env variable equals 1 when running via Pycharm.
            # it avoids us from crashing, which happens when using
            # multiprocessing via Pycharm's debug-mode
            results = []
            for story_id in stories_ids:
                results.append(await self.fetch_story_by_id(story_id))
        else:
            results = await asyncio.gather(*[self.fetch_story_by_id(i)
                                             for i in stories_ids])
        return results

    async def fetch_story_by_id(self, story_id: str) -> Result:
        """
        Fetching a single story details by the story_id
        """
        request_url = f"{self.base_url}/item/{story_id}.json"

        response = requests.get(request_url)
        if not response.ok:
            logging.info("failed to retrieve %".format(story_id))
            return Result(
                title="",
                url=""
            )

        response_json = response.json()

        return Result(
            title=response_json.get("title"),
            url=response_json.get("url")
        )

    def __repr__(self) -> str:
        """
        HackerNewsSource string representation
        """
        output = f"{Fore.GREEN}HackerNews Source Results " \
                 f"[Metric: {self.metric}]{Style.RESET_ALL} \n"
        for result in self.results:
            output += f"{result} \n"
        return output
