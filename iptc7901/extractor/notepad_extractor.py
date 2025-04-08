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

from iptc7901.digitalwires_model import DigitalwiresModel
from iptc7901.utils import get_none_safe, EdNote


def get_ednotes(dw_model: DigitalwiresModel) -> list[EdNote]:
    """Returns a list of editorial notes from the ednotes given by the role
    ``dpaednoterole:editorialnote``.

    :param dw_model: A model of the digitalwires message.
    :return: A list of editorial notes.
    """
    return dw_model.notepad_items(
        notepad_role="dpaednoterole:editorialnote", attrs=["ednote"]
    )


def get_public_notepad(dw_model: DigitalwiresModel) -> str:
    """Returns the public notepad.

    :param dw_model: A model of the digitalwires message.
    :return: The public notepad as string. This is ``None`` if and only if there is a
        public notepad entry having a null-value.
    """
    return get_none_safe(dw_model, "notepad", {}).get("public_html", "")


def get_non_public_notepad(dw_model: DigitalwiresModel) -> str:
    """Returns the non-public notepad.

    :param dw_model: A model of the digitalwires message.
    :return: The non-public notepad as string. This is ``None`` if and only if there is
        a non-public notepad entry having a null-value.
    """
    return get_none_safe(dw_model, "notepad", {}).get("nonpublic_html", "")


def get_notepad_header(dw_model: DigitalwiresModel) -> str:
    """Returns the notepad header.

    :param dw_model: A model of the digitalwires message.
    :return: The notepad header as a string. This is ``None`` if and only if there is a
        notepad header entry having null-value.
    """
    return get_none_safe(dw_model, "notepad", {}).get("header_html", "")


def get_closing_line(dw_model: DigitalwiresModel) -> str:
    """Returns the closing line from the ednotes.

    There should only be one closing line, but in case there are more, they are joined
    with an empty string.
    :param dw_model: A model of the digitalwires message.
    :return: The closing line as a string.
    """
    return "".join(
        note.ednote
        for note in dw_model.notepad_items(
            notepad_role="dpaednoterole:closingline", attrs=["ednote"]
        )
    )


def get_correction(dw_model: DigitalwiresModel) -> str:
    """Returns the correction notes from the ednotes given by the role
    ``dpaednoterole:correctionshort``

    :param dw_model: A model of the digitalwires message.
    :return: The correction notes as a string. If there are more than one, they are
        joined by a space.
    """
    return " ".join(
        note.ednote
        for note in dw_model.notepad_items(
            notepad_role="dpaednoterole:correctionshort", attrs=["ednote"]
        )
    )


def get_picture_ednote_de(dw_model: DigitalwiresModel) -> str:
    """Returns the picture note from the ednotes given by the role
    ``dpaednoterole:picture``

    :param dw_model: A model of the digitalwires message.
    :return: The picture note as a string. If there are more than one, only the first
        result is returned.
    """
    return next(
        iter(
            note.ednote
            for note in dw_model.notepad_items(
                notepad_role="dpaednoterole:picture", attrs=["ednote"]
            )
        ),
        "",
    )


def get_genre_note(dw_model: DigitalwiresModel) -> str:
    """Returns the genre note from the categories given by ``"role":
    "dpaednoterole:genre"``.

    :param dw_model: A model of the digitalwires message.
    :return: The genre note as a string. If there are more than one, only the first
        result is returned.
    """
    return next(
        iter(
            note.ednote
            for note in dw_model.notepad_items(
                notepad_role="dpaednoterole:genrenote", attrs=["ednote"]
            )
        ),
        "",
    )


def get_embargo_note(dw_model: DigitalwiresModel) -> str:
    """Returns the embargo note from the ednotes given by ``"role":
    "dpaednoterole:embargo"``

    :param dw_model: A model of the digitalwires message.
    :return: The embargo note as a string. If there are more than one, only the first
        result is returned.
    """
    return next(
        iter(
            note.ednote
            for note in dw_model.notepad_items(
                notepad_role="dpaednoterole:embargo", attrs=["ednote"]
            )
        ),
        "",
    )
