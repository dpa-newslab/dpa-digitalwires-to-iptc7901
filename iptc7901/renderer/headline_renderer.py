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

import arrow

from typing import Callable

from iptc7901.digitalwires_model import DigitalwiresModel
from iptc7901.utils import BELL, signal_map, prio_map


def render_title(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the title from the extractors by joining them with a ``\\n``.

    If the headline ends with a ``=``, it will be removed since it is the headline
    delimiter, which will be added by the builder.
    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions to build the title.
    :return: A string, where all extractor results are joined by ``\n``
    """
    title = "\n".join([extractor(dw_model).strip() for extractor in extractors])
    return [title.removesuffix("=").strip()]


def render_correction(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the correction note for the headline.

    If there is a correction the german version looks like this: .. code-block:: text

    (Berichtigung: In einer früheren Version dieses Textes hieß es, Vergewaltigung in
    der Ehe sei bis 1992 nicht strafbar gewesen. Richtig ist aber das Jahr 1997.)

    The international version is whithout the note.

    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions to build the correction note.
    :return: A string, where all extractor results are joined by ``\\n``
    """
    result = ""
    correction_note = "\n".join(
        [extractor(dw_model).strip() for extractor in extractors]
    )

    def build_line(kind, note, lang):
        if lang == "de":
            return "(" + kind + (": " + note if len(note) > 0 else "") + ")"
        else:
            return kind

    if dw_model.canceled() and dw_model.lang() == "de":
        result += "(Achtung) " + correction_note
    else:
        signal = dw_model.get("signal")
        if signal is not None:
            result += build_line(
                signal_map[signal][dw_model.lang()], correction_note, dw_model.lang()
            )
    return [result] if result else []


def render_ednote_de(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the picture ednote. Since there can only be one only the first extractor
    function is used.

    The result may look like this:

    .. code-block:: text

    (Foto Produktion)

    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions, where only the first one is used.
    :return: A string which look like as shown above.
    """
    ednote = next(
        iter(
            remove_empty_items(
                [extractor(dw_model).strip() for extractor in extractors]
            )
        ),
        "",
    )
    return ["(" + ednote + ")"] if len(ednote) > 0 else []


def render_genre(
    dw_model: DigitalwiresModel,
    extract_qcode: Callable[[DigitalwiresModel], str],
    extract_name: Callable[[DigitalwiresModel], str],
    extract_note: Callable[[DigitalwiresModel], str],
) -> list[str]:
    """Renders the genre part of the headline including the name and genre note.

    :param dw_model: A model of the digitalwires message.
    :param extract_qcode: Function to retrieve the genre qcode
    :param extract_name: Function to retrieve the display name of the genre
    :param extract_note: Function to retrieve the genre note
    :return: Returns a list of one string with the following structure: "Überblick foo
        bar" or "Fragen &amp; Antworten - foo bar"
    """
    result = []
    qcode = extract_qcode(dw_model)
    name = extract_name(dw_model)
    note = extract_note(dw_model)

    dashless = [
        "dpatextgenre:1",
        "dpatextgenre:8",
        "dpatextgenre:21",
        "dpatextgenre:25",
        "dpatextgenre:26",
    ]
    blacklist = (
        ["dpatextgenre:1"]
        if dw_model.lang() == "de"
        else ["dpatextgenre:1", "dpatextgenre:30", "dpatextgenre:32"]
    )

    if qcode not in blacklist:
        result.append(name)
    if note is not None and note != "":
        result.append(note)
    delimiter = " " if qcode in dashless else " - "
    return [delimiter.join(result)]


def render_embargo(
    dw_model: DigitalwiresModel,
    extract_embargo: Callable[[DigitalwiresModel], str],
    extract_embargo_note: Callable[[DigitalwiresModel], str],
) -> list[str]:
    """Renders the embargo information given by ``extract_embargo`` and
    ``extract_embargo_note``.

    :param dw_model: A model of the digitalwires message.
    :param extract_embargo: An extractor function return the embargo date and time in
        ISO format.
    :param extract_embargo_note: An extractor function return the embargo note.
    :return: A string similar to `Sperrfrist 09. Oktober 14.20 Uhr - Some notes...`
    """
    result = []
    embargo = extract_embargo(dw_model)
    note = extract_embargo_note(dw_model)

    if embargo and len(embargo) > 0:
        date = (
            arrow.get(embargo).to("CET").format("d. MMMM HH.mm [Uhr]", locale="de_DE")
        )
        result.append("Sperrfrist " + date)
        if len(note) > 0:
            result.append(note)
        return [" - ".join(result)]
    return []


def render_byline(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], str]]
) -> list[str]:
    """Renders the byline.

    Since there is just one byline in a message only the first extractor function is
    used.
    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions to build the byline. Only the first
        result is used.
    :return: A list with one string containing the byline
    """
    return remove_empty_items(
        [extractor(dw_model).strip() for extractor in extractors][:1]
    )


def render_prio(
    dw_model: DigitalwiresModel, extractors: list[Callable[[DigitalwiresModel], int]]
) -> list[str]:
    """Renders the priority text for the headline including the BELL singals.

    In german it may look like this:

    .. code-block:: text

    (Eil \u0007\u0007\u0007\u0007\u0007)

    :param dw_model: A context object of the digitialwires message.
    :param extractors: A list of extractor functions to get the urgency. Only the first
        extractor is used.
    :return: A list with one string containing the prio headline if the urgency is `1`
        or `2`. Otherwise, the string is empty.
    """
    result = ""

    prio = extractors[0](dw_model)
    opening = "(" if dw_model.lang() == "de" else ""
    closing = ")" if dw_model.lang() == "de" else ""
    bell = ""
    if prio == 1:
        bell = BELL * 10
    elif prio == 2:
        bell = BELL * 5
    if prio < 3:
        result = (
            opening + prio_map.get(prio, {}).get(dw_model.lang(), "") + bell + closing
        )
    return [result]


def remove_empty_items(search_list):
    return list(filter(lambda s: len(s) > 0, search_list))
