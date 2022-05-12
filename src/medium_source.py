from typing import List
from models import Source, Result
import feedparser
from colorama import Fore, Style


class MediumSource(Source):
    
    def __init__(self, tag, limit=10) -> None:
        self.results: List[Result] = []
        self.tag = tag
        self.limit = limit

    def connect(self):
        pass

    def fetch(self) -> List[Result]:
        if not self.tag or self.limit < 0:
            return []

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
        output = f"{Fore.GREEN}Medium Source Results" \
                 f" [Tag: {self.tag}]{Style.RESET_ALL} \n"
        for result in self.results:
            output += f"{result} \n"
        return output