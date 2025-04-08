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

from typing import Callable

from iptc7901.digitalwires_model import DigitalwiresModel
from iptc7901.utils import extend_if_not_empty, notepad_md


def render_public_notepad(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the public notepad information by converting it into markdown-like plain
    text.

    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions returning the public notepad.
    :return: A list of markdown-like plain text of the public notepad.
    """
    return [notepad_md(extractor(dw_model)) for extractor in extractors]


def render_nonpublic_notepad(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the non-public notepad information by converting it into markdown-like
    plain text. The fist element is always `* * * *` if there are non-public notes.

    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions returning the non-public notepad.
    :return: A list of strings containing the markdown-like plain text of the non-public
        notepad. If there are any, the first element is `* * * *`, otherwise, the list
        is empty. Never ``None``.
    """
    result = ["* * * *"]
    extend_if_not_empty(
        result, [notepad_md(extractor(dw_model)) for extractor in extractors]
    )
    return result if len(result) > 1 else []


def render_notepad_header(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the notepad header by converting it into markdown-like plain text.

    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions returning the public notepad.
    :return: A list of markdown-like plain text of the public notepad.
    """
    return [notepad_md(extractor(dw_model)) for extractor in extractors]
