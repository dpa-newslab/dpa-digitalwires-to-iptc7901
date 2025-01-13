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

import textwrap

from abc import ABC, abstractmethod
from iptc7901.Context import Context


class AbstractIptcBuilder(ABC):

    def __init__(self, context: Context, line_length: int = 69):
        self.line_length = line_length
        self.context = context

    @abstractmethod
    def build(self) -> str:
        pass

    def wrap_line(self, paragraphs: list[str], double_newline: bool = False) -> str:
        """
        Wrap every line of every paragraph/table row/list item to self.line_length chars.
        :param self:
        :param paragraphs: a list of paragraphs that will be wrapped.
        :param double_newline: flag if each item in `paragraphs` should be double-wrapped. This is used in body content
        :return: a string of wrapped paragraphs.
        """
        wrapped_lines_by_part = [
            [textwrap.fill(line, width=self.line_length) for line in part.splitlines()]
            for part in paragraphs
        ]
        # Recombine paragraph/table row/list item's lines
        wrapped_parts = ["\n".join(part_lines) for part_lines in wrapped_lines_by_part]
        # Get plaintext by combining all parts
        delimiter = "\n\n" if double_newline else "\n"
        plaintext = (
            str(delimiter.join(wrapped_parts).strip())
            if type(wrapped_parts) != str
            else wrapped_parts
        )
        return plaintext
