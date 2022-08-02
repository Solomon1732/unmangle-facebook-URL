#!/usr/bin/env python3

import argparse
import sys

import exceptions
import program_modes
import url_utils


def main_loop(prog_mode: program_modes.ProgramMode) -> None:
    """Main loop of the program."""

    prompt, print_msg = prog_mode.value

    while True:
        try:
            raw_url: str = input(prompt)
        except EOFError:
            break

        try:
            processed_url: str = url_utils.decrypt_url(raw_url=raw_url)
        except exceptions.QueryStringParsingError as exc:
            print_msg(
                f"ERROR: Failed to parse URL '{exc.url}'",
                f"ERROR: Extracted query '{exc.url_query}'",
                file=sys.stderr,
                sep="\n",
            )
        else:
            print_msg(processed_url)


def main() -> None:
    """Main function of the module."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=program_modes.ProgramMode.QUIET,
        default=program_modes.ProgramMode.INTERACTIVE,
        help="Suppress input prompt message.",
    )
    args = parser.parse_args()
    main_loop(prog_mode=args.quiet)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Keyboard interrupt. Exiting...")
