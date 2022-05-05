from abc import ABC, abstractmethod
from colorama import Fore, Style

class Source(ABC):
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch(self):
        pass


class Result:
    def __init__(self, title: str, url: str) -> None:
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        return f"* \t {Fore.CYAN}{self.title}{Style.RESET_ALL}: {Fore.MAGENTA}{self.url} {Style.RESET_ALL} \n"