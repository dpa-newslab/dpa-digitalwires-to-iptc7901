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


def get_version_created(dw_model: DigitalwiresModel) -> str:
    """Returns the version created.

    :param dw_model: A model of the digitalwires message.
    :return: The version created as a string.
    """
    return dw_model["version_created"]


def get_dateline(dw_model: DigitalwiresModel) -> str:
    """Returns the dateline.

    :param dw_model: A model of the digitalwires message.
    :return: The dateline as a string.
    """
    dateline = dw_model["dateline"]
    return dateline if dateline else ""


def get_urgency(dw_model: DigitalwiresModel) -> int:
    """Returns the urgency if there is one, otherwise ``3``.

    :param dw_model: A model of the digitalwires message.
    :return: The urgency as an Integer, ``3`` if there is no urgency.
    """
    return dw_model.get("urgency", 3)


def get_keywords(dw_model: DigitalwiresModel) -> list[Category]:
    """Returns all keyword names.

    :param dw_model: A model of the digitalwires message.
    :return: A list of keyword names.
    """
    return [Category(name=cat) for cat in dw_model.get("keyword_names", [])]


def get_embargo(dw_model: DigitalwiresModel) -> str:
    """Returns the embargo date.

    :param dw_model: A model of the digitalwires message.
    :return: The embargo date as a string.
    """
    return dw_model.get("embargoed", "")


def get_byline(dw_model: DigitalwiresModel) -> str:
    """Returns the byline.

    :param dw_model: A model of the digitalwires message.
    :return: The byline as a string. Never ``None``.
    """
    byline = dw_model["byline"]
    return byline if byline else ""
