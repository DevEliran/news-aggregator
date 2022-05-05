from dataclasses import dataclass

class Result:
    def __init__(self, title: str, url: str) -> None:
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        return f"{self.title}: \n {self.url}"