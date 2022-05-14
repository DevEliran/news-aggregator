from typing import List
import feedparser
from colorama import Fore, Style
from src.models import Source, Result


"""
MediumSource module, responsible for querying Medium feed based on tags.
"""


def reformat_results(raw_results) -> List[Result]:
    """
    Transforming feedparser raw results into the Result class
    """
    results = []
    for result in raw_results:
        results.append(
            Result(
                title=result.title,
                url=result.link
            )
        )

    return results


class MediumSource(Source):
    """
    MediumSource class accepts a tag and a limit.
    Parsing Medium's feed based on the tag and limit specified.
    """
    
    def __init__(self, tag, limit=10) -> None:
        """
        Initiate empty results list
        """
        self.results: List[Result] = []
        self.tag = tag
        self.limit = limit

    def connect(self):
        """
        Medium doesn't require an API key, hence there's no need to
        implement `connect`
        """
        pass

    def fetch(self) -> List[Result]:
        """
        Retrieves posts from Medium feed based on the tag specified.
        """
        if not self.tag or self.limit < 0:
            return []

        raw_results = feedparser.parse(f"https://medium.com/feed/tag/"
                                       f"{self.tag}").entries[:self.limit]

        self.results = reformat_results(raw_results)
        return self.results

    def __repr__(self) -> str:
        """
        MediumSource string representation
        """
        output = f"{Fore.GREEN}Medium Source Results" \
                 f" [Tag: {self.tag}]{Style.RESET_ALL} \n"
        for result in self.results:
            output += f"{result} \n"
        return output
