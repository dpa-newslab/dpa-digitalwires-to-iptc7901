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
from iptc7901.utils.CollectionUtils import find_first_in, get_none_safe


def get_ressort(context: Context) -> str:
    """
    Returns the ressort from the categories. There should only be one categorie with ``"type": "dnltype:desk"``.
    :param context: A context object of the digitalwires message.
    :return: The ressort as a string.
    """
    return "".join(
        [
            cat.get("qcode", "")
            for cat in sorted(
                get_none_safe(context.digitalwire, "categories", []),
                key=lambda cat: _get_rank(cat),
            )
            if cat.get("type", "") == "dnltype:desk"
        ]
    )


def get_services(context: Context) -> list[str]:
    """
    Returns all services from the categories given by ``"type": "dnltype:wire"``.
    :param context: A context object of the digitalwires message.
    :return: A list of service qcodes from the categories.
    """
    return [
        cat.get("qcode", "")
        for cat in sorted(
            get_none_safe(context.digitalwire, "categories", []),
            key=lambda cat: _get_rank(cat),
        )
        if cat.get("type", "") == "dnltype:wire"
    ]


def get_dpa_subjects(context: Context) -> list[str]:
    """
    Returns all dpa_subjects from the categories given by ``"type": "dnltype:dpasubject"``.
    :param context: A context object of the digitalwires message.
    :return: A list of subject names from the categories.
    """
    return [
        categorie.get("name", "")
        for categorie in sorted(
            get_none_safe(context.digitalwire, "categories", []),
            key=lambda cat: _get_rank(cat),
        )
        if categorie.get("type", "") == "dnltype:dpasubject"
    ]


def get_geo_subject(context: Context) -> list[str]:
    """
    Returns all geo subjects from the categories given by ``"type": "dnltype:geosubject"``.
    :param context: A context object of the digitalwires message.
    :return: A list of geo subject names from the categories.
    """
    return [
        categorie.get("name", "")
        for categorie in sorted(
            get_none_safe(context.digitalwire, "categories", []),
            key=lambda cat: _get_rank(cat),
        )
        if categorie.get("type", "") == "dnltype:geosubject"
    ]


def get_genre_qcode(context: Context) -> str:
    """
    Returns the genre qcode from the categories given by ``"type": "dnltype:genre"``.
    :param context: A context object of the digitalwires message.
    :return: The genre qcode as a string. If there are more than one, only the first result is returned.
    """
    return find_first_in(
        get_none_safe(context.digitalwire, "categories", []),
        "qcode",
        lambda cat: cat.get("type", "") == "dnltype:genre",
    )


def get_genre_name(context: Context) -> str:
    """
    Returns the genre name from the categories given by ``"type": "dnltype:genre"``.
    :param context: A context object of the digitalwires message.
    :return: The genre name as a string. If there are more than one, only the first result is returned.
    """
    return find_first_in(
        get_none_safe(context.digitalwire, "categories", []),
        "name",
        lambda cat: cat.get("type", "") == "dnltype:genre",
    )


def _get_rank(cat):
    rank = cat.get("rank", 999)
    return rank if rank is not None else 999
