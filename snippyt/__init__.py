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


from importlib import import_module
from inspect import getdoc, getmembers, getsourcelines
from pathlib import Path

from rich.console import Console
from rich.terminal_theme import MONOKAI


def remove_docstring(lines: list[str], docs: list[str]) -> list[str]:
    """Remove the docstring from the lines of code.

    Parameters
    ----------
    lines : list[str]
        The lines of code.
    docs : list[str]
        The docstring to remove.

    Returns
    -------
    list[str]
        The lines of code with the docstring removed.
    """

    no_docs = lines

    for i, line in enumerate(lines):
        if line.endswith(docs[0]):
            end = i + len(docs)

            if lines[end].endswith('"""\n'):
                del no_docs[i : end + 1]
            else:
                del no_docs[i:end]

            break

    return no_docs


def get_member_source(module: str, member: str, keep_docs: bool = False) -> list[str]:
    """Get the source code for a given module and member.

    Parameters
    ----------
    module : str
        The module to use.
    member : str
        The member within the module to use.
    keep_docs : bool, optional
        Whether to keep the docstring, by default False.

    Returns
    -------
    list[str]
        The lines of source code for the member.
    """

    match = None

    for name, thing in getmembers(import_module(module)):
        if name == member:
            match = thing
            break

    if match is None:
        raise ValueError(f"Could not find member {member} in {module}.")

    lines = getsourcelines(match)[0]

    if keep_docs:
        return lines

    docs = getdoc(match).splitlines(keepends=True)
    return remove_docstring(lines, docs)


def create_snippet(
    output: str | Path,
    border: bool = False,
    input_file: str | Path | None = None,
    keep_docs: bool = False,
    lines: list[int, int] | tuple[list, list] | None = None,
    member: list[str, str] | tuple[str, str] | None = None,
    numbers: bool = False,
    title: str | None = None,
    width: int | None = None,
) -> None:
    """Create a code snippet.

    Parameters
    ----------
    output : str | Path
        A path to save the SVG to.
    border : bool, optional
        Whether to include a border, by default False.
    input_file : str | Path | None, optional
        A path to the Python file containing the code you want, by default None.
    keep_docs : bool, optional
        Whether to keep member docstrings, by default False.
    lines : list[int, int] | tuple[int, int] | None, optional
        The range of lines for the snippet, by default None.
    member : str | None
        The name of the member for the snippet, by default None.
    numbers : bool, optional
        Whether to include line numbers, by default False.
    title : str | None, optional
        A title for the snippet, by default None.
    width : int | None, optional
        The width of the snippet, by default None.
    """

    if lines is not None:
        if input_file is None:
            raise ValueError("input_file must be specified with lines")

        start = lines[0] - 1
        end = lines[1]

        with open(input_file) as source:
            code = source.readlines()[start:end]

    elif member is not None:
        code = get_member_source(*member, keep_docs=keep_docs)

        if title is None:
            title = member[1]

    else:
        if input_file is None:
            raise ValueError("no input_file was given")

        with open(input_file) as source:
            code = source.readlines()

    if width is None:
        width = max(len(line) for line in code)

    console = Console(record=True, width=width)

    console.print("".join(code))
    console.save_svg(output, title=title, theme=MONOKAI)
