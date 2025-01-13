#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 dpa-IT Services GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import html2text
import re
import textwrap

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


def article_html_to_text(html, line_width=69, prefix=None):
    if html is None:
        return ""
    soup = BeautifulSoup(html, "html.parser")

    def gen_lines():
        s = soup.find("section")  # assumes toplevel section
        for br in s.find_all("br"):
            br.replace_with("\n")
        for li in s.find_all("li"):
            li.string = f"  * {li.string}\n"
        for i, tag in enumerate(s.find_all(recursive=False)):
            para = tag.get_text(separator="")
            if prefix is not None and i == 0:
                para = prefix + para
            for l in para.rstrip("\n").split("\n"):
                if l == "":
                    yield l
                for line in textwrap.wrap(l, width=line_width, break_on_hyphens=False):
                    yield line
            yield ""  # newline after each paragraph/heading

    return "\n".join(gen_lines())


class NotepadMarkdownConverter(MarkdownConverter):
    def convert_hn(self, n, el, text, convert_as_inline):
        return super().convert_hn(n, el, text, convert_as_inline)[
            2:-1
        ]  # Remove two '#' at beginning and one '\n' at the end

    def convert_li(self, el, text, convert_as_inline):
        text = super().convert_li(el, text, convert_as_inline)
        lines = []
        if self.options["wrap"]:
            depth = 0
            while el:
                if el.name == "ul":
                    depth += 1
                el = el.parent
            for t in text.strip().split("\n"):
                t = textwrap.fill(
                    t,
                    width=self.options["wrap_width"],
                    break_long_words=True,
                    break_on_hyphens=False,
                    initial_indent="  " * (depth - 1),
                    subsequent_indent="  " * depth,
                )
                lines.append(t)
        return "%s\n" % "\n".join(lines)


def notepad_md(html) -> str:
    if html is None:
        return ""
    return NotepadMarkdownConverter(
        escape_misc=False,
        escape_asterisks=False,
        escape_underscores=False,
        bullets="-",
        wrap=True,
        wrap_width=69,
    ).convert(html)


class TextHTML2Text(html2text.HTML2Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ## config
        self.ignore_links = True
        self.ignore_images = True
        self.ignore_emphasis = True
        self.protect_links = False
        self.pad_tables = True
        self.wrap_list_items = True
        self.wrap_tables = False
        self.ul_item_mark = "*"
        self.body_width = 69
        self.single_line_break = True
        html2text.config.RE_MD_PLUS_MATCHER = re.compile(
            r"(a)(b)^",
            flags=re.MULTILINE | re.VERBOSE,
        )  # matches nothing
        html2text.config.RE_UNORDERED_LIST_MATCHER = re.compile(r"(a)(b)^")
        html2text.config.RE_ORDERED_LIST_MATCHER = re.compile(r"(a)(b)^")
        html2text.config.RE_MD_DOT_MATCHER = re.compile(
            r"(a)(b)^",
            flags=re.MULTILINE | re.VERBOSE,
        )
        html2text.config.RE_MD_DASH_MATCHER = re.compile(
            r"(a)(b)^",
            flags=re.MULTILINE | re.VERBOSE,
        )
        html2text.config.RE_MD_DOT_MATCHER = re.compile(
            r"(a)(b)^",
            flags=re.MULTILINE | re.VERBOSE,
        )
        html2text.config.RE_MD_PLUS_MATCHER = re.compile(
            r"(a)(b)^",
            flags=re.MULTILINE | re.VERBOSE,
        )
        html2text.config.RE_SLASH_CHARS = r"(a)(b)^"
        html2text.config.RE_TABLE = re.compile(r"\| ")

        # internal state
        self.row_is_header = False

    def handle_tag(self, tag, attrs, start):
        # Hier kannst du die benutzerdefinierte Formatierung für bestimmte Tags handhaben
        if tag == "h4":
            self.o("\n") if start else self.o("\n")
        elif tag == "h3":
            self.o("\n") if start else self.o("\n")
        elif tag == "h2":
            self.o("\n") if start else self.o("\n")
        elif tag == "h1":
            self.o("\n") if start else self.o("\n")
        elif (
            tag == "br" and start and not self.split_next_td
        ):  # no line breaks in tables
            self.o("\n")
        elif tag == "br" and not start and self.split_next_td:
            self.o(" ")
        elif tag == "br":
            pass
        elif tag == "p":
            if not self.split_next_td:  # no line breaks in tables
                self.o("\n")
            elif not start:
                self.o(" ")
        elif tag == "div":
            self.o("")
        elif tag in ["ul", "ol"] and not start:
            self.o("")
            self.list.pop()
            self.lastWasList = True
        elif tag in ["table", "tr", "td", "th"]:
            self.handle_table(tag, attrs, start)
        else:
            super().handle_tag(tag, attrs, start)

    def handle_table(self, tag, attrs, start):
        if self.ignore_tables:
            if tag == "tr":
                if start:
                    pass
                else:
                    self.soft_br()
            else:
                pass

        elif self.bypass_tables:
            if start:
                self.soft_br()
            if tag in ["td", "th"]:
                if start:
                    self.o("<{}>\n\n".format(tag))
                else:
                    self.o("\n</{}>".format(tag))
            else:
                if start:
                    self.o("<{}>".format(tag))
                else:
                    self.o("</{}>".format(tag))

        else:
            if tag == "table":
                if start:
                    self.table_start = True
                    self.row_is_header = False
                    self.o("\n")
                    if self.pad_tables:
                        self.o("<" + html2text.config.TABLE_MARKER_FOR_PAD + ">")
                        self.o("  \n")
                else:
                    if self.pad_tables:
                        # add break in case the table is empty or its 1 row table
                        self.soft_br()
                        self.o("</" + html2text.config.TABLE_MARKER_FOR_PAD + ">")
                        self.o("  \n")
            if tag in ["td", "th"] and start:
                if self.split_next_td:
                    self.o("| ")
                self.split_next_td = True
            if tag == "th" and start:
                self.row_is_header = True

            if tag == "tr" and start:
                self.td_count = 0
            if tag == "tr" and not start:
                self.split_next_td = False
                self.soft_br()
            if tag == "tr" and not start and self.table_start and self.row_is_header:
                # Underline table header
                self.o("|".join(["---"] * self.td_count))
                self.soft_br()
                self.table_start = False
                self.row_is_header = False
            if tag in ["td", "th"] and start:
                self.td_count += int(attrs["colspan"]) if "colspan" in attrs else 1

    def optwrap(self, text: str) -> str:
        """
        Wrap all paragraphs in the provided text.

        :type text: str

        :rtype: str
        """
        if not self.body_width:
            return text

        result = ""
        newlines = 0
        # I cannot think of a better solution for now.
        # To avoid the non-wrap behaviour for entire paras
        # because of the presence of a link in it
        if not self.wrap_links:
            self.inline_links = False
        for para in text.strip().split("\n"):
            if len(para) > 0:
                if not html2text.skipwrap(
                    para, self.wrap_links, self.wrap_list_items, self.wrap_tables
                ):
                    indent = ""
                    if para.startswith("  " + self.ul_item_mark):
                        # list item continuation: add a double indent to the
                        # new lines
                        indent = "    "
                    elif para.startswith("> "):
                        # blockquote continuation: add the greater than symbol
                        # to the new lines
                        indent = "> "
                    wrapped = textwrap.wrap(
                        para,
                        width=self.body_width,
                        break_long_words=True,
                        break_on_hyphens=False,
                        subsequent_indent=indent,
                    )
                    result += "\n".join(wrapped)
                    if para.endswith("  "):
                        result += "  \n"
                        newlines = 1
                    elif indent:
                        result += "\n"
                        newlines = 1
                    else:
                        result += "\n"
                        newlines = 1
                else:
                    # Warning for the tempted!!!
                    # Be aware that obvious replacement of this with
                    # line.isspace()
                    # DOES NOT work! Explanations are welcome.
                    if not html2text.config.RE_SPACE.match(para):
                        result += para + "\n"
                        newlines = 1
            else:
                # if newlines < 2:
                result += "\n"
                newlines += 1
        return result
