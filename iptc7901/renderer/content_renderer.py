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
import textwrap
from typing import Callable

from iptc7901.Context import Context
from iptc7901.utils.WordUtils import TextHTML2Text


def render_article(
    context: Context,
    extract_dateline: Callable[[Context], str],
    extractors: list[Callable[[Context], str]],
) -> list[str]:
    """
    Renders the HTML content returned from ``extractors`` into a plain text with a line width of 69 characters. ``extract_dateline`` is the prefix for each extractor content.

    Note that no encoding fixes are performed.

    For example this HTML:

    .. code-block:: html

        <h2>Hauptthemen</h2>
           <p>+ Berlin: Sitzungen und Statements der Bundestagsfraktionen (gesonderter Eintrag)<br/>+ 1000 Potsdam: Pk des Moses Mendelssohn Zentrums für europäisch-jüdische Studien (MMZ) zu einer Bewertung der Ergebnisse der Landtagswahl (gesonderter Eintrag) <br/>+ Blick auf die konstituierende Sitzung des Thüringer Landtags am Donnerstag (gesonderter Eintrag)</p>
        <ul>
           <li>Einzelmeldungen</li>
           <li>Zusammenfassung, «Erste Schritte auf dem Weg zu «Brombeer»-Koalitionen» - 96 Zl.</li>
           <li>Grafik-Diagramm Nr. 107865, Querformat 90 x 70 mm, «Mögliche Koalitionen (weiter aktuell)»</li>
           <li>Video-Digital-Beitrag</li>
        </ul>

    will be transformed to:

    .. code-block:: text

        Hauptthemen
        + Berlin: Sitzungen und Statements der Bundestagsfraktionen
        (gesonderter Eintrag)
        + 1000 Potsdam: Pk des Moses Mendelssohn Zentrums für
        europäisch-jüdische Studien (MMZ) zu einer Bewertung der Ergebnisse
        der Landtagswahl (gesonderter Eintrag)
        + Blick auf die konstituierende Sitzung des Thüringer Landtags am
        Donnerstag (gesonderter Eintrag)

          * Einzelmeldungen
          * Zusammenfassung, «Erste Schritte auf dem Weg zu
        «Brombeer»-Koalitionen» - 96 Zl.
          * Grafik-Diagramm Nr. 107865, Querformat 90 x 70 mm, «Mögliche
        Koalitionen (weiter aktuell)»
          * Video-Digital-Beitrag

    :param context: Context object of the digitalwire message.
    :param extract_dateline: An extractor function, which takes a context object and returns the dateline, which may look like this: "Berlin (dpa) - "
    :param extractors: A list of extractor functions, which takes a context object and returns the HTML content of the digitalwire message.
    :return: A list of strings for each extractor, where each has the prefix from `extract_dateline`.
    """
    prefix = '<section class="main"><p>'
    dateline = extract_dateline(context)
    if dateline:
        dateline = prefix + dateline
    else:
        prefix = ""  # In this case we do not need to strip anything
    return [
        TextHTML2Text().handle(f"{dateline} {extractor(context).removeprefix(prefix)}")
        for extractor in extractors
    ]


def render_date_time(
    context: Context, extractors: list[Callable[[Context], str]]
) -> list[str]:
    """
    Renders the given timestamp from ``extractors`` in the format ``DDHHmm MMM YY``.
    :param context: The context object of the digitalwire message.
    :param extractors: A list of extractor functions, which takes a context object and returns an ISO formatted timestamp as a string
    :return: A list of strings for each extractor.
    """
    return [
        arrow.get(extractor(context)).format("DDHHmm MMM YY", "de")
        for extractor in extractors
    ]


def render_closing_line(
    context: Context, extractors: list[Callable[[Context], str]]
) -> list[str]:
    """
    Just executes each extractor from ``extractors`` and returns the result as a string.
    :param context: The context object of the digitalwire message.
    :param extractors: A list of extractor functions, which takes a context object and returns the closing line as a string.
    :return: A list of strings for each extractor.
    """
    return [extractor(context) for extractor in extractors]


def render_teaser(
    context: Context, extractors: list[Callable[[Context], str]]
) -> list[str]:
    """
    Renders the teaser from each extractor and returns the result as a string. Each line will never exceed the line width of 69 characters.
    :param context: The context object of the digitalwire message.
    :param extractors: A list of extractor functions, which takes a context object and returns the teaser as a string.
    :return: A list of strings for each extractor, where the text wrapped to a line width of 69 characters.
    """
    return [
        (
            textwrap.fill(extractor(context), width=69)
            if extractor(context) is not None
            else ""
        )
        for extractor in extractors
    ]
