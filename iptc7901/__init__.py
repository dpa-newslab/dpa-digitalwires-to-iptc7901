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

from typing import Callable, Any

from iptc7901.digitalwires_model import DigitalwiresModel
from iptc7901.builder import (
    DateTimeBuilder,
    HeaderBuilder,
    SluglineBuilder,
    NotepadBuilder,
    TeaserBuilder,
    TextBuilder,
    ClosingLineBuilder,
    create_headline_builder,
)
from iptc7901.extractor import get_services


def convert_to_iptc(
    digitalwires: dict, find_sequence: Callable[[str], Any] = None
) -> dict[str, str]:
    """This function takes the dict representation of a digitalwires message and creates
    an iptc message for each service.

    For more details on how an iptc message is structured, have a look here
    https://gitlab.com/dpa-gmbh/content-provisioning/high-level/mecom-belieferungen-high-level/-/wikis/IPTC_Format
     or here: http://www.iptc.org/std/IPTC7901/1.0/specification/7901V5.pdf
    :param digitalwires: The parsed json representation of a digitalwires message.
    :param find_sequence: A function that takes the service qcode as a string and
        returns a generator, which return consecutive integers. If this parameter is
        None the service sequence number and the agency sequence number is always
        '0000'.
    :return: a list of iptc messages for each service
    """
    dw_model = DigitalwiresModel(digitalwires)
    if dw_model.has_no_content():
        return {}

    iptc_dict = {}

    header_builder = HeaderBuilder(dw_model, find_sequence)
    slugline_builder = SluglineBuilder(dw_model)
    headline_builder = create_headline_builder(dw_model)
    teaser_builder = TeaserBuilder(dw_model)
    text_builder = TextBuilder(dw_model)
    notepad_builder = NotepadBuilder(dw_model)
    closing_builder = ClosingLineBuilder(dw_model)
    date_time_builder = DateTimeBuilder(dw_model)

    for service in get_services(dw_model):
        text = text_builder.build()
        word_count = len([t for t in text.split() if t != "|"])  # ignore table frames

        iptc = ""
        iptc += f"""\x01{header_builder.build_with(word_count, service.qcode)}\n\n{slugline_builder.build()}
\x02{headline_builder.build()}\n"""

        teaser = teaser_builder.build()
        if teaser is not None and len(teaser.strip()) > 0:
            iptc += f"""\n{teaser_builder.build()}\n"""

        iptc += f"""\n{text_builder.build().strip()}\n\n"""

        notepad = notepad_builder.build()
        if notepad is not None and len(notepad.strip()) > 0:
            iptc += f"""{notepad_builder.build()}\n"""

        iptc += f"""{closing_builder.build()}\n\n\x03{date_time_builder.build()}\n\x7f\n\x7f\x04"""

        iptc_dict[service.qcode] = iptc
    return iptc_dict
