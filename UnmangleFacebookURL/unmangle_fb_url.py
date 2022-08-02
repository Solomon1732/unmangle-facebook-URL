#!/usr/bin/env python3

import argparse
import sys
import urllib.parse

from typing import Dict, Final, List
from urllib.parse import SplitResult


class QueryStringParsingError(ValueError):
    """Exception class for an error during parsing a URL's string query."""

    def __init__(self, *args: object, url: SplitResult, url_query: str) -> None:
        super().__init__(*args)
        self._url = url
        self._url_query = url_query

    @property
    def url_query(self) -> str:
        return self._url_query

    @property
    def url(self) -> SplitResult:
        return self._url


_URL_QUERY_PARAM: Final[str] = "u"
_FACEBOOK_TRACKER_PARAM: Final[str] = "fbclid"


def parse_query(url: SplitResult) -> Dict[str, str]:
    """Extract the query parameter from a URL."""

    url_query: str = url.query

    try:
        return urllib.parse.parse_qs(qs=url_query, strict_parsing=True)
    except ValueError as exc:
        raise QueryStringParsingError(
            f"Error parsing query: '{url_query}'",
            url=urllib.parse.urlunsplit(url),
            url_query=url_query,
        ) from exc


def extract_url(raw_url: str) -> str:
    """Extract the URL from an encrypted URL.

    The returned URL includes Facebook's query trackers.
    """

    url: SplitResult = urllib.parse.urlsplit(raw_url)
    url_query: Dict[str, str] = parse_query(url=url)
    query_param_list: List[str] = url_query[_URL_QUERY_PARAM]

    return query_param_list[0]


def clean_url(dirty_url: str) -> str:
    """Clean URL from Facebook URL parameter."""

    url_tuple: SplitResult = urllib.parse.urlsplit(dirty_url)
    url_query: Dict[str, str] = parse_query(url=url_tuple)
    url_query.pop(_FACEBOOK_TRACKER_PARAM, None)
    new_encoded_query: Dict[str, str] = urllib.parse.urlencode(query=url_query)
    new_url: SplitResult = url_tuple._replace(query=new_encoded_query)

    return urllib.parse.urlunsplit(new_url)


def decrypt_url(raw_url: str) -> str:
    """Decrypt URL shared on Facebook."""

    dirty_url: str = extract_url(raw_url=raw_url)

    return clean_url(dirty_url=dirty_url)


def print_func(is_quiet: bool = False):
    """Returns a print function.

    The returned function's behavior differs between quiet mode and interactive mode.
    In quite mode it prints the message as-is. In interactive mode it print a blank
    line before and after the message.
    """

    def quiet_print(*args, **kwargs) -> None:
        print(*args, **kwargs)

    def interactive_print(*args, **kwargs) -> None:
        print(file=kwargs.get("file", sys.stdout))
        print(*args, **kwargs)
        print(file=kwargs.get("file", sys.stdout))

    return quiet_print if is_quiet else interactive_print


def main_loop(is_quiet: bool) -> None:
    """Main loop of the program."""

    prompt: str = "" if is_quiet else "Enter link: "
    print_msg = print_func(is_quiet=is_quiet)

    while True:
        try:
            raw_url: str = input(prompt)
        except EOFError:
            break

        try:
            processed_url: str = decrypt_url(raw_url=raw_url)
        except QueryStringParsingError as exc:
            print_msg(
                f"ERROR: Failed to parse URL '{exc.url}'",
                f"ERROR: Extracted query '{exc.url_query}'",
                file=sys.stderr,
                sep="\n",
            )
        else:
            print_msg(processed_url)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress input prompt message.",
    )
    args = parser.parse_args()
    main_loop(is_quiet=args.quiet)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Keyboard interrupt. Exiting...")
