# jewel

[Rich](https://github.com/Textualize/rich) Python code snippets.

```
pip install jewel
```

## Examples

### Module & Member Input

```
> jewel -m rich.print -th dracula

💎 Saved SVG to jewel.svg!
```

![The source code for `rich.print`.](jewel.svg)

### File & Line Number Input

```
> jewel -i jewel/__main__.py -l 81 101 -o file_input.svg

💎 Saved SVG to file_input.svg!
```

![Source code from `jewel/__main__.py`.](file_input.svg)

## Usage

```
> jewel -h

usage: jewel [-h] (-i PATH | -m MEMBER) [-l START END] [-g] [-n] [-nd] [-th THEME] [-na] [-nt] [-o PATH] [-t TITLE] [-w WIDTH]

Rich Python code snippets.

options:
  -h, --help            show this help message and exit
  -i PATH, --input PATH
                        The Python file to use.
  -m MEMBER, --member MEMBER
                        The member to use.
  -l START END, --lines START END
                        The line range to use.

code options:
  -g, --guides          Include indent guides.
  -n, --numbers         Include line numbers.
  -nd, --no-docs        Remove member docstring.
  -th THEME, --theme THEME
                        The syntax theme to use.

svg options:
  -na, --no-after       No terminal:after gradient.
  -nt, --no-traffic-lights
                        No traffic lights.
  -o PATH, --output PATH
                        Where to save the SVG.
  -t TITLE, --title TITLE
                        A title for the snippet.
  -w WIDTH, --width WIDTH
                        The width of the snippet.
```
