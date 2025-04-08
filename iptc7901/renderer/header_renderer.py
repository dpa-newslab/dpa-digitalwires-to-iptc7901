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
from iptc7901.utils import service_mnemonic_map, service_to_iptc_agency_map, Category


def render_header(
    dw_model: DigitalwiresModel,
    word_count: int,
    extract_service: Callable[[DigitalwiresModel], str],
    service_sequence_number: int,
    extract_urgency: Callable[[DigitalwiresModel], int],
    extract_ressort: Callable[[DigitalwiresModel], str],
    agency_sequence_number: int,
) -> str:
    """Render the IPTC header based on the extractor functions. The header looks like
    this: .. code-block:: text.

    <DNST><DLFD> <PRIO> <RESS> <WANZ>  <AGNT> <ALFD>  <BEZU>

    where ``DNST`` is the 3-character abbreviation of the service,

    ``DLFD`` is a 4-digit number, either ``'0000'`` or the number given by
    ``service_sequence_number``,

    ``PRIO`` is the urgency,

    ``RESS`` is the ressort, given by the categorie with ``type='dnltype:desk'``,

    ``WANZ`` is the word count, without headline and notepad,

    ``AGNT`` is the agency name, which is derived by the result from ``extract_service``
    and mapped by ``iptc_7901.utils.Mappings.service_to_iptc_agency_map``.

    ``ALFD`` is the agency squence number, either ``'0000'`` or the number given by
    ``agency_sequence_number``,

    ``BEZU`` is empty

    :param dw_model: A model of the digitalwires message.
    :param word_count: The number of words in the text, excluding the headline and
        notepad
    :param extract_service: A function return the service code, which is mapped to the
        3-character abbreviation by ``iptc_7901.utils.Mappings.service_mnemonic_map``.
    :param service_sequence_number: The service sequence number, which is set to 4
        digits with leading zeros.
    :param extract_urgency: A function returning the urgency.
    :param extract_ressort: A function returning the ressort.
    :param agency_sequence_number: The sequence number for the agency.
    :return: A string representation of the IPTC header.
    """
    service = extract_service(dw_model)
    return f"{service_mnemonic_map.get(service, service)}{service_sequence_number:04d} {str(extract_urgency(dw_model))} {extract_ressort(dw_model).split(':')[-1]} {word_count}  {service_to_iptc_agency_map.get(service, 'dpa')} {agency_sequence_number:04d}"


def render_subject(
    dw_model: DigitalwiresModel,
    extractors: list[Callable[[DigitalwiresModel], list[Category]]],
) -> list[str]:
    """Renders the keyword list for the IPTC header.

    :param dw_model: A model of the digitalwires message.
    :param extractors: A list of extractor functions used to extract a list of keywords.
    :return: A flattened list of keywords.
    """
    return [subj.name for extractor in extractors for subj in extractor(dw_model)]
