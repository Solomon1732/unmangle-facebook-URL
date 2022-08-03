#!/usr/bin/env python3
from typing import Final


class QueryStringParsingError(ValueError):
    """Exception class for an error during parsing a URL's string query."""

    def __init__(self, *args: object, url: str, url_query: str) -> None:
        super().__init__(*args)
        self._url: Final[str] = url
        self._url_query: Final[str] = url_query

    @property
    def url_query(self) -> str:
        return self._url_query

    @property
    def url(self) -> str:
        return self._url


if __name__ == "__main__":
    pass
