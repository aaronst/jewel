"""
snippyt: Command-line tool for creating Python code snippets.
author: Aaron Stephens <aaronjst93@gmail.com>

Copyright 2022 Aaron Stephens

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from argparse import ArgumentParser, Namespace

from . import create_snippet


def main(args: Namespace) -> None:
    """Main function.

    Parameters
    ----------
    args : Namespace
        The parsed command-line arguments.
    """

    create_snippet(
        args.output,
        input_file=args.input,
        keep_docs=args.keep_docs,
        lines=args.lines,
        member=args.member,
        title=args.title,
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="Create Python code snippets.")
    parser.add_argument("-i", "--input", help="The Python file to use.")
    parser.add_argument(
        "-k", "--keep-docs", action="store_true", help="Keep member docstring."
    )
    parser.add_argument(
        "-l", "--lines", help="The line range to use.", nargs=2, type=int
    )
    parser.add_argument("-m", "--member", help="The module and member to use.", nargs=2)
    parser.add_argument(
        "-o", "--output", default="snippyt.svg", help="Where to save the SVG."
    )
    parser.add_argument("-t", "--title", help="A title for the snippet.")
    parser.add_argument("-w", "--width", help="The width of the snippet.", type=int)

    main(parser.parse_args())
