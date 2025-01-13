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

from iptc7901 import Context
from iptc7901.Context import Context
from iptc7901.utils.CollectionUtils import find_first_in, get_none_safe


def get_ednotes(context: Context) -> list[str]:
    """
    Returns a list of editorial notes from the ednotes given by ``"role": "dpaednoterole:editorialnote"``.
    :param context: A context object of the digitalwires message.
    :return: A list of editorial notes.
    """
    return [
        ednote.get("ednote", "")
        for ednote in get_none_safe(context.digitalwire, "ednotes", [])
        if ednote.get("role", "") == "dpaednoterole:editorialnote"
    ]


def get_public_notepad(context: Context) -> str:
    """
    Returns the public notepad.
    :param context: A context object of the digitalwires message.
    :return: The public notepad as string. This is ``None`` if and only if there is a public notepad entry having a null-value.
    """
    return get_none_safe(context.digitalwire, "notepad", {}).get("public_html", "")


def get_non_public_notepad(context: Context) -> str:
    """
    Returns the non-public notepad.
    :param context: A context object of the digitalwires message.
    :return: The non-public notepad as string. This is ``None`` if and only if there is a non-public notepad entry having a null-value.
    """
    return get_none_safe(context.digitalwire, "notepad", {}).get("nonpublic_html", "")


def get_notepad_header(context: Context) -> str:
    """
    Returns the notepad header.
    :param context: A context object of the digitalwires message.
    :return: The notepad header as a string. This is ``None`` if and only if there is a notepad header entry having null-value.
    """
    return get_none_safe(context.digitalwire, "notepad", {}).get("header_html", "")


def get_closing_line(context: Context) -> str:
    """
    Returns the closing line from the ednotes. There should only be one closing line, but in case there are more, they are joined with an empty string.
    :param context: A context object of the digitalwires message.
    :return: The closing line as a string.
    """
    return "".join(
        [
            ednote.get("ednote", "")
            for ednote in get_none_safe(context.digitalwire, "ednotes", [])
            if ednote.get("role", "") == "dpaednoterole:closingline"
        ]
    )


def get_correction(context: Context) -> str:
    """
    Returns the correction notes from the ednotes given by ``"role": "dpaednoterole:correctionshort"``
    :param context: A context object of the digitalwires message.
    :return: The correction notes as a string. If there are more than one, they are joined by a space.
    """
    return " ".join(
        [
            ednote.get("ednote", "")
            for ednote in get_none_safe(context.digitalwire, "ednotes", [])
            if ednote.get("role", "") == "dpaednoterole:correctionshort"
        ]
    )


def get_picture_ednote_de(context: Context) -> str:
    """
    Returns the picture note from the ednotes given by ``"role": "dpaednoterole:picture"``
    :param context: A context object of the digitalwires message.
    :return: The picture note as a string. If there are more than one, only the first result is returned.
    """
    return next(
        iter(
            [
                ednote.get("ednote", "")
                for ednote in get_none_safe(context.digitalwire, "ednotes", [])
                if ednote.get("role", "") == "dpaednoterole:picture"
            ]
        ),
        "",
    )


def get_genre_note(context: Context) -> str:
    """
    Returns the genre note from the categories given by ``"role": "dpaednoterole:genre"``.
    :param context: A context object of the digitalwires message.
    :return: The genre note as a string. If there are more than one, only the first result is returned.
    """
    return find_first_in(
        get_none_safe(context.digitalwire, "ednotes", []),
        "ednote",
        lambda cat: cat.get("role", "") == "dpaednoterole:genrenote",
    )


def get_embargo_note(context: Context) -> str:
    """
    Returns the embargo note from the ednotes given by ``"role": "dpaednoterole:embargo"``
    :param context: A context object of the digitalwires message.
    :return: The embargo note as a string. If there are more than one, only the first result is returned.
    """
    return find_first_in(
        get_none_safe(context.digitalwire, "ednotes", []),
        "ednote",
        lambda cat: cat.get("role", "") == "dpaednoterole:embargo",
    )
