from typing import List

import feedparser
from colorama import Fore, Style
from src.models import Result


class AwsBlogSource:

    def __init__(self, category: str, limit: int = 10):
        self.category = category
        self.limit = limit
        self.base_url = "https://aws.amazon.com/blogs"
        self.results: List[Result] = []

    def connect(self):
        pass

    def fetch(self):
        feed_url = f"{self.base_url}/{self.category}/feed"

        raw_results = feedparser.parse(feed_url).entries[:self.limit]

        results = []
        for result in raw_results:
            results.append(
                Result(
                    title=result.get("title"),
                    url=result.get('links')[0].get('href')
                )
            )

        self.results = results

    def __repr__(self) -> str:
        """
        AwsBlogSource string representation
        """
        output = f"{Fore.GREEN}AWS Blog Source Results " \
                 f"[Category: {self.category}]{Style.RESET_ALL} \n"
        for result in self.results:
            output += f"{result} \n"
        return output
