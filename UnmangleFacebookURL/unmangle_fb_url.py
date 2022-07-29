#!/usr/bin/env python3

import sys
import urllib.parse
from typing import Dict, Final, List, NamedTuple


class QueryStringParsingError(ValueError):
    """Exception class for an error during parsing a URL's string query."""

    def __init__(self, *args: object, url: NamedTuple, url_query: str) -> None:
        super().__init__(*args)
        self._url = url
        self._url_query = url_query

    @property
    def url_query(self) -> str:
        return self._url_query

    @property
    def url(self) -> NamedTuple:
        return self._url


_URL_QUERY_PARAM: Final[str] = "u"
_FACEBOOK_TRACKER_PARAM: Final[str] = "fbclid"


def parse_query(url_tuple: NamedTuple) -> Dict[str, str]:
    """Extract the query parameter from a URL."""
    url_query: str = url_tuple.query

    try:
        return urllib.parse.parse_qs(qs=url_query, strict_parsing=True)
    except ValueError as exc:
        raise QueryStringParsingError(
            f"Error parsing query: '{url_query}'", url=url_tuple, url_query=url_query
        ) from exc


def extract_url(raw_url: str) -> str:
    """Extract the URL from an encrypted URL. Return a URL with Facebook parameter trackers."""
    url_tuple: NamedTuple = urllib.parse.urlsplit(raw_url)
    url_query: Dict[str, str] = parse_query(url_tuple=url_tuple)
    query_param_list: List[str] = url_query[_URL_QUERY_PARAM]

    return query_param_list[0]


def clean_url(dirty_url: str) -> str:
    """Clean URL from Facebook URL parameter."""
    url_tuple: NamedTuple = urllib.parse.urlsplit(dirty_url)
    url_query: Dict[str, str] = parse_query(url_tuple=url_tuple)

    url_query.pop(_FACEBOOK_TRACKER_PARAM, None)
    new_encoded_query: Dict[str, str] = urllib.parse.urlencode(query=url_query)
    new_url = url_tuple._replace(query=new_encoded_query)

    return urllib.parse.urlunsplit(new_url)


def decrypt_url(raw_url: str) -> str:
    """Decrypt URL shared on Facebook."""
    dirty_url: str = extract_url(raw_url=raw_url)

    return clean_url(dirty_url=dirty_url)


def main() -> None:
    while True:
        try:
            raw_url: str = input("Enter outgoing link: ")
        except EOFError:
            return

        try:
            processed_url: str = decrypt_url(raw_url=raw_url)
        except QueryStringParsingError as exc:
            print(f"Error parsing URL: '{exc.url}'", file=sys.stderr)
            print(f"Malformed query: '{exc.url_query}'", file=sys.stderr)
        else:
            print("\n")
            print(processed_url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Keyboard interrupt. Exiting...")
