"""
shine: Command-line tool for creating Python code snippets.
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
from io import StringIO
from inspect import getdoc, getmembers, getsourcelines
from pathlib import Path

from rich.console import Console, ConsoleOptions
from rich.measure import measure_renderables
from rich.syntax import Syntax, SyntaxTheme, DEFAULT_THEME
from rich.terminal_theme import TerminalTheme, DEFAULT_TERMINAL_THEME

from .formats import create_format


def remove_docstring(lines: list[str], docs: list[str]) -> str:
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

    return "".join(no_docs)


def get_member_source(module: str, member: str, docstring: bool = True) -> str:
    """Get the source code for a given module and member.

    Parameters
    ----------
    module : str
        The module to use.
    member : str
        The member within the module to use.
    docstring : bool, optional
        Whether to include the docstring, by default True.

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

    if docstring:
        return "".join(lines)

    docs = getdoc(match).splitlines(keepends=True)
    return remove_docstring(lines, docs)


def create_snippet(
    output: str | Path,
    after: bool = True,
    docstring: bool = True,
    guides: bool = False,
    input_file: str | Path | None = None,
    lines: list[int] | tuple[list, list] | None = None,
    member: list[str] | tuple[str, str] | None = None,
    numbers: bool = False,
    theme: str | SyntaxTheme = DEFAULT_THEME,
    title: str | None = None,
    traffic_lights: bool = True,
    width: int | None = None,
) -> None:
    """Create a code snippet.

    Parameters
    ----------
    output : str | Path
        A path to save the SVG to.
    after : bool, optional
        Whether to include the terminal:after gradient, by default True.
    docstring : bool, optional
        Whether to include the member docstring, by default True.
    guides : bool, optional
        Whether to include indent guides, by default False.
    input_file : str | Path | None, optional
        A path to the Python file containing the code you want, by default None.
    lines : list[int] | tuple[int, int] | None, optional
        The range of lines for the snippet, by default None.
    member : list[str] | tuple[str, str] | None
        The name of the module and member for the snippet, by default None.
    numbers : bool, optional
        Whether to include line numbers, by default False.
    theme : str | SyntaxTheme, optional
        The syntax theme to use, by default DEFAULT_THEME.
    title : str | None, optional
        A title for the snippet, by default None.
    traffic_lights : bool, optional
        Whether to include traffic lights, by default True.
    width : int | None, optional
        The width of the snippet, by default None.
    """

    if input_file is not None:
        syntax = Syntax.from_path(
            input_file,
            "python",
            dedent=True,
            indent_guides=guides,
            line_numbers=numbers,
            line_range=lines,
            theme=theme,
            word_wrap=True,
        )

    elif member is not None:
        code = get_member_source(*member, docstring=docstring)

        syntax = Syntax(
            code,
            "python",
            dedent=True,
            indent_guides=guides,
            line_numbers=numbers,
            theme=theme,
            word_wrap=True,
        )

    else:
        raise ValueError("Must provide an input file or module member.")

    if width is None:
        # set the width to fit the code
        width = (
            syntax._numbers_column_width
            + max(len(line) for line in syntax.code.splitlines())
            + (3 if numbers else 0)
        )

    console = Console(file=StringIO(), record=True, width=width)
    console.print(syntax)

    if title is None and not traffic_lights:
        code_format = create_format(after=after, header=False)
    else:
        code_format = create_format(
            after=after, title=title is not None, traffic_lights=traffic_lights
        )

    # this is only to get the console background the same as the code background
    terminal_theme = TerminalTheme(
        syntax._theme._background_style.bgcolor.triplet,
        (255, 255, 255),  # white
        DEFAULT_TERMINAL_THEME.ansi_colors._colors,
    )

    console.save_svg(output, code_format=code_format, theme=terminal_theme, title=title)
