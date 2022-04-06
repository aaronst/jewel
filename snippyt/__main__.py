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

from . import create_snippyt


def main(args: Namespace) -> None:
    """Main function.

    Parameters
    ----------
    args : Namespace
        The parsed command-line arguments.
    """

    try:
        create_snippyt(
            args.output,
            after=args.no_after,
            docstring=args.no_docs,
            guides=args.guides,
            input_file=args.input,
            lines=args.lines,
            member=args.member,
            numbers=args.numbers,
            theme=args.theme,
            title=args.title,
            traffic_lights=args.no_traffic_lights,
            width=args.width,
        )
    except ValueError as err:
        print(err)
        return

    print(f"Saved SVG to {args.output}.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Create Python code snippets.")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i", "--input", help="The Python file to use.", metavar="PATH"
    )
    input_group.add_argument(
        "-m",
        "--member",
        help="The module and member to use.",
        metavar=("MODULE", "MEMBER"),
        nargs=2,
    )

    parser.add_argument(
        "-l",
        "--lines",
        help="The line range to use.",
        metavar=("START", "END"),
        nargs=2,
        type=int,
    )

    code_group = parser.add_argument_group(title="code options")
    code_group.add_argument(
        "-g", "--guides", action="store_true", help="Include indent guides."
    )
    code_group.add_argument(
        "-n", "--numbers", action="store_true", help="Include line numbers."
    )
    code_group.add_argument(
        "-nd", "--no-docs", action="store_false", help="Remove member docstring."
    )
    code_group.add_argument(
        "-th", "--theme", default="monokai", help="The syntax theme to use."
    )

    svg_group = parser.add_argument_group(title="svg options")
    svg_group.add_argument(
        "-na", "--no-after", action="store_false", help="No terminal:after gradient."
    )
    svg_group.add_argument(
        "-nt", "--no-traffic-lights", action="store_false", help="No traffic lights."
    )
    svg_group.add_argument(
        "-o",
        "--output",
        default="snippyt.svg",
        help="Where to save the SVG.",
        metavar="PATH",
    )
    svg_group.add_argument("-t", "--title", help="A title for the snippet.")
    svg_group.add_argument("-w", "--width", help="The width of the snippet.", type=int)

    main(parser.parse_args())
