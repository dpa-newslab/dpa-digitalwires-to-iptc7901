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
from iptc7901.utils import Category


def get_ressort(dw_model: DigitalwiresModel) -> str:
    """Returns the ressort from the categories.

    There should only be one categorie with ``"type": "dnltype:desk"``.
    :param dw_model: A model of the digitalwires message.
    :return: The ressort as a string.
    """
    return "".join(
        cat.qcode
        for cat in dw_model.category_items(cat_type="dnltype:desk", attrs=["qcode"])
    )


def get_services(dw_model: DigitalwiresModel) -> list[Category]:
    """Returns all services from the categories where type is ``dnltype:wire``.

    :param dw_model: A model of the digitalwires message.
    :return: A list of service qcodes from the categories.
    """
    return dw_model.category_items(cat_type="dnltype:wire", attrs=["qcode"])


def get_dpa_subjects(dw_model: DigitalwiresModel) -> list[Category]:
    """Returns all dpa_subjects from the categories where type is
    ``"dnltype:dpasubject"``.

    :param dw_model: A model of the digitalwires message.
    :return: A list of subject names from the categories.
    """
    return dw_model.category_items(cat_type="dnltype:dpasubject", attrs=["name"])


def get_geo_subject(dw_model: DigitalwiresModel) -> list[Category]:
    """Returns all geo subjects from the categories given by ``"type":
    "dnltype:geosubject"``.

    :param dw_model: A model of the digitalwires message.
    :return: A list of geo subject names from the categories.
    """
    return dw_model.category_items(cat_type="dnltype:geosubject", attrs=["name"])


def get_genre_qcode(dw_model: DigitalwiresModel) -> str:
    """Returns the genre qcode from the categories given by ``"type": "dnltype:genre"``.

    :param dw_model: A model of the digitalwires message.
    :return: The genre qcode as a string. If there are more than one, only the first
        result is returned.
    """
    return next(
        iter(
            cat.qcode
            for cat in dw_model.category_items(
                cat_type="dnltype:genre", attrs=["qcode"]
            )
        ),
        "",
    )


def get_genre_name(dw_model: DigitalwiresModel) -> str:
    """Returns the genre name from the categories given by ``"type": "dnltype:genre"``.

    :param dw_model: A model of the digitalwires message.
    :return: The genre name as a string. If there are more than one, only the first
        result is returned.
    """
    return next(
        iter(
            cat.name
            for cat in dw_model.category_items(cat_type="dnltype:genre", attrs=["name"])
        ),
        "",
    )
