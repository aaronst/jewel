# shine 

[Rich](https://github.com/Textualize/rich) Python snippets. Let your code shine!

```
> shine -m rich.print

✨ Saved SVG to shine.svg!
```

![The source code for `rich.print`.](shine.svg)

## Usage

```
> shine -h

usage: shine [-h] (-i PATH | -m MEMBER) [-l START END] [-g] [-n] [-nd] [-th THEME] [-na] [-nt] [-o PATH] [-t TITLE] [-w WIDTH]

Rich Python snippets. Let your code shine!

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
