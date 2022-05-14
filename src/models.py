from typing import List
from abc import ABC, abstractmethod
from colorama import Fore, Style

"""
Models module, defines the central classes of the package.
"""


class Source(ABC):
    """
    Abstract source class, defines an interface for inheriting sources
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch(self):
        pass


class SourceManager:
    """
    SourceManger gets a list of sources.
    By calling this object, it will execute `fetch` on all sources it has,
    and print the results.
    """
    def __init__(self, sources: List[Source] = None) -> None:
        """
        Initialize sources
        """
        if not sources:
            self.sources = []
        else:
            self.sources = sources

    def __call__(self) -> None:
        """
        Iterate through the given sources and print their results.
        """
        for source in self.sources:
            source.fetch()
            print(source)

    def add(self, source: Source) -> None:
        """
        Add a single source to the sources list
        """
        self.sources.append(source)


class Result:
    """
    Unified class of results.
    """
    def __init__(self, title: str, url: str) -> None:
        """
        Save the title and url of a post
        """
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        """
        String representation of a Result
        """
        if not self.title or not self.url:
            return ""
        return f"* \t {Fore.CYAN}{self.title}{Style.RESET_ALL}:" \
               f" {Fore.MAGENTA}{self.url} {Style.RESET_ALL} \n"
