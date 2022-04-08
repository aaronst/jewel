"""
jewel: Rich Python code snippets.
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
from inspect import getmembers, getsource
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from rich.console import Console
from rich.syntax import Syntax, SyntaxTheme, DEFAULT_THEME
from rich.terminal_theme import TerminalTheme, DEFAULT_TERMINAL_THEME

from .formats import create_format


def remove_docstring(member: Any) -> str:
    """Remove a member's docstring.

    Parameters
    ----------
    member : Any
        The member to remove a docstring from.

    Returns
    -------
    str
        The code for the member with the docstring removed.
    """

    source = getsource(member)

    try:
        doc = f'"""{member.__doc__}"""\n'
    except AttributeError:
        return source

    try:
        location = source.index(doc)
    except ValueError:
        return source

    for i in range(location - 1, 1, -1):
        if source[i - 1] == "\n":
            start = i
            break

    return source.replace(source[start : location + len(doc)], "")


def get_member_source(member: str, docstring: bool = True) -> str:
    """Get the source code for a given module and member.

    Parameters
    ----------
    member : str
        The `module.member` to use.
    docstring : bool, optional
        Whether to include the docstring, by default True.

    Returns
    -------
    str
        The source code for the member.
    """

    match = None
    module, member = member.rsplit(".", maxsplit=1)

    for name, thing in getmembers(import_module(module)):
        if name == member:
            match = thing
            break

    if match is None:
        raise ValueError(f"Could not find member {member} in {module}.")

    if docstring:
        return getsource(match)

    return remove_docstring(match)


def create_snippet(
    output: Union[str, Path],
    after: bool = True,
    docstring: bool = True,
    guides: bool = False,
    input_file: Optional[Union[str, Path]] = None,
    lines: Optional[Union[List[int], Tuple[List, List]]] = None,
    member: Optional[str] = None,
    numbers: bool = False,
    theme: Union[str, SyntaxTheme] = DEFAULT_THEME,
    title: Optional[str] = None,
    traffic_lights: bool = True,
    width: Optional[int] = None,
) -> None:
    """Create a code snippet.

    Parameters
    ----------
    output : Union[str, Path]
        A path to save the SVG to.
    after : bool, optional
        Whether to include the terminal:after gradient, by default True.
    docstring : bool, optional
        Whether to include the member docstring, by default True.
    guides : bool, optional
        Whether to include indent guides, by default False.
    input_file : Optional[Union[str, Path]], optional
        A path to the Python file containing the code you want, by default None.
    lines : Optional[Union[List[int], Tuple[int, int]]], optional
        The range of lines for the snippet, by default None.
    member : Optional[str], optional
        The member for the snippet, by default None.
    numbers : bool, optional
        Whether to include line numbers, by default False.
    theme : Union[str, SyntaxTheme], optional
        The syntax theme to use, by default DEFAULT_THEME.
    title : Optional[str], optional
        A title for the snippet, by default None.
    traffic_lights : bool, optional
        Whether to include traffic lights, by default True.
    width : Optional[int], optional
        The width of the snippet, by default None.
    """

    if input_file is not None:
        syntax = Syntax.from_path(
            input_file,
            dedent=True,
            indent_guides=guides,
            line_numbers=numbers,
            line_range=lines,
            theme=theme,
            word_wrap=True,
        )

    elif member is not None:
        code = get_member_source(member, docstring=docstring)

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
