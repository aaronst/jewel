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


CONSOLE_SVG_FORMAT = """\
<svg width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}"
     xmlns="http://www.w3.org/2000/svg">
    <style>
        @font-face {{
            font-family: "Fira Code";
            src: local("FiraCode-Regular"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
            font-style: normal;
            font-weight: 400;
        }}
        @font-face {{
            font-family: "Fira Code";
            src: local("FiraCode-Bold"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                 url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
            font-style: bold;
            font-weight: 700;
        }}
        span {{
            display: inline-block;
            white-space: pre;
            vertical-align: top;
            font-size: {font_size}px;
            font-family:'Fira Code','Cascadia Code',Monaco,Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace;
        }}
        a {{
            text-decoration: none;
            color: inherit;
        }}
        .blink {{
           animation: blinker 1s infinite;
        }}
        @keyframes blinker {{
            from {{ opacity: 1.0; }}
            50% {{ opacity: 0.3; }}
            to {{ opacity: 1.0; }}
        }}
        #wrapper {{
            padding: {margin}px;
            padding-top: 100px;
        }}
        #terminal {{
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: {theme_background_color};
            border-radius: 14px;
            outline: 1px solid #484848;
        }}[terminal_after]
        #terminal-header {{
            position: relative;
            width: 100%;
            min-height: 64px;
            background-color: #2e2e2e;
            margin-bottom: 12px;
            font-weight: bold;
            border-radius: 14px 14px 0 0;
            color: {theme_foreground_color};
            font-size: 18px;
            box-shadow: inset 0px -1px 0px 0px #4e4e4e,
                        inset 0px -4px 8px 0px #1a1a1a;
        }}
        #terminal-title-tab {{
            display: inline-block;
            margin-top: 14px;
            margin-left: 124px;
            font-family: sans-serif;
            padding: 14px 28px;
            border-radius: 6px 6px 0 0;
            background-color: {theme_background_color};
            box-shadow: inset 0px 1px 0px 0px #4e4e4e,
                        0px -4px 4px 0px #1e1e1e,
                        inset 1px 0px 0px 0px #4e4e4e,
                        inset -1px 0px 0px 0px #4e4e4e;
        }}
        #terminal-traffic-lights {{
            position: absolute;
            top: 24px;
            left: 20px;
        }}
        #terminal-body {{
            line-height: {line_height}px;
            padding: 14px;[body_margin_top]
        }}
        {stylesheet}
    </style>
    <foreignObject x="0" y="0" width="100%" height="100%">
        <body xmlns="http://www.w3.org/1999/xhtml">
            <div id="wrapper">
                <div id="terminal">[terminal_header]
                    <div id='terminal-body'>
                        {code}
                    </div>
                </div>
            </div>
        </body>
    </foreignObject>
</svg>
"""

BODY_MARGIN_TOP = """
            margin-top: {line_height}px;
"""

TERMINAL_AFTER = """
        #terminal:after {{
            position: absolute;
            width: 100%;
            height: 100%;
            content: '';
            border-radius: 14px;
            background: rgb(71,77,102);
            background: linear-gradient(90deg, #804D69 0%, #4E4B89 100%);
            transform: rotate(-4.5deg);
            z-index: -1;
        }}
"""

TERMINAL_HEADER = """
                    <div id='terminal-header'>[traffic_lights][title]
                    </div>
"""

TRAFFIC_LIGHTS = """
                        <svg id="terminal-traffic-lights" width="90" height="21" viewBox="0 0 90 21" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="14" cy="8" r="8" fill="#ff6159"/>
                            <circle cx="38" cy="8" r="8" fill="#ffbd2e"/>
                            <circle cx="62" cy="8" r="8" fill="#28c941"/>
                        </svg>
"""

TITLE = """
                        <div id="terminal-title-tab">{title}</div>
"""


def create_format(
    after: bool = True,
    header: bool = True,
    title: bool = True,
    traffic_lights: bool = True,
) -> str:
    """Create an SVG format string based on desired features.

    Parameters
    ----------
    after : bool, optional
        Whether to include the terminal:after gradient, by default True.
    header : bool, optional
        Whether to include the header, by default True.
    title : bool, optional
        Whether to include the title tab, by default True.
    traffic_lights : bool, optional
        Whether to include the traffic lights, by default True.

    Returns
    -------
    str
        An SVG format string.
    """

    code_format = CONSOLE_SVG_FORMAT
    code_format = code_format.replace(
        "[terminal_after]", TERMINAL_AFTER if after else ""
    )

    if header:
        code_format = code_format.replace("[body_margin_top]", "")

        terminal_header = TERMINAL_HEADER
        terminal_header = terminal_header.replace("[title]", TITLE if title else "")
        terminal_header = terminal_header.replace(
            "[traffic_lights]", TRAFFIC_LIGHTS if traffic_lights else ""
        )

        code_format = code_format.replace("[terminal_header]", terminal_header)
    else:
        code_format = code_format.replace("[body_margin_top]", BODY_MARGIN_TOP)
        code_format = code_format.replace("[terminal_header]", "")

    return code_format
