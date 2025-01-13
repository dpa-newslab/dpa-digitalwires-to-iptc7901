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

from collections.abc import Generator

from .Context import Context
from .builder.content_builder import TeaserBuilder, TextBuilder, ClosingLineBuilder
from .builder.date_time_builder import DateTimeBuilder
from .builder.header_builder import HeaderBuilder, SluglineBuilder
from .builder.headline_builder import create_headline_builder
from .builder.notepad_builder import NotepadBuilder
from .extractor.category_extractor import get_services


def convert_to_iptc(
    digitalwires: dict,
    service_sequence_generator: Generator[int, str, None] = None,
    agency_sequence_generator: Generator[int, str, None] = None,
) -> dict[str, str]:
    """
    This function takes the string representation of a digitalwires message and creates an iptc message for each service.
    For more details on how an iptc message is structured, have a look here https://gitlab.com/dpa-gmbh/content-provisioning/high-level/mecom-belieferungen-high-level/-/wikis/IPTC_Format
    or here: http://www.iptc.org/std/IPTC7901/1.0/specification/7901V5.pdf
    :param digitalwires:
    :param service_sequence_generator: A generator, which return consecutive integers each time the function is called. If this parameter is None the service sequence number is always '0000'.
    :param agency_sequence_generator: A generator, which return consecutive integers each time the function is called. If this parameter is None the agency sequence number is always '0000'.
    :return: a list of iptc messages for each service
    """
    context = Context(digitalwires)
    if context.has_no_content:
        return {}

    iptc_dict = {}

    header_builder = HeaderBuilder(
        context, service_sequence_generator, agency_sequence_generator
    )
    slugline_builder = SluglineBuilder(context)
    headline_builder = create_headline_builder(context)
    teaser_builder = TeaserBuilder(context)
    text_builder = TextBuilder(context)
    notepad_builder = NotepadBuilder(context)
    closing_builder = ClosingLineBuilder(context)
    date_time_builder = DateTimeBuilder(context)

    for service in get_services(context):
        if service == "dnlsrv:sch3pb":
            continue  # keine Schalttafel-exporte
        text = text_builder.build()
        word_count = len([t for t in text.split() if t != "|"])  # ignore table frames

        iptc = ""
        iptc += f"""\x01{header_builder.build_with(word_count, service)}\n\n{slugline_builder.build()}
\x02{headline_builder.build()}\n"""

        teaser = teaser_builder.build()
        if teaser is not None and len(teaser.strip()) > 0:
            iptc += f"""\n{teaser_builder.build()}\n"""

        iptc += f"""\n{text_builder.build().strip()}\n\n"""

        notepad = notepad_builder.build()
        if notepad is not None and len(notepad.strip()) > 0:
            iptc += f"""{notepad_builder.build()}\n"""

        iptc += f"""{closing_builder.build()}\n\n\x03{date_time_builder.build()}\n\x7f\n\x7f\x04"""

        iptc_dict[service] = iptc
    return iptc_dict
