#!/bin/usr/env python3

import urllib.parse
from typing import Dict, Final, List
from urllib.parse import SplitResult

import exceptions

_URL_QUERY_PARAM: Final[str] = "u"
_FACEBOOK_TRACKER_PARAM: Final[str] = "fbclid"


def parse_query(url: SplitResult) -> Dict[str, str]:
    """Extract the query parameter from a URL."""

    url_query: str = url.query

    try:
        return urllib.parse.parse_qs(qs=url_query, strict_parsing=True)
    except ValueError as exc:
        raise exceptions.QueryStringParsingError(
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
