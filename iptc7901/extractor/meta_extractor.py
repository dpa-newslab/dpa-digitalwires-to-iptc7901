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


def get_version_created(context: Context) -> str:
    """
    Returns the version created.
    :param context: A context object of the digitalwires message.
    :return: The version created as a string.
    """
    return context.digitalwire.get("version_created", "")


def get_dateline(context: Context) -> str:
    """
    Returns the dateline.
    :param context: A context object of the digitalwires message.
    :return: The dateline as a string.
    """
    dateline = context.digitalwire.get("dateline", "")
    return dateline if dateline else ""


def get_urgency(context: Context) -> int:
    """
    Returns the urgency if there is one, otherwise ``3``.
    :param context: A context object of the digitalwires message.
    :return: The urgency as an Integer, ``3`` if there is no urgency.
    """
    return context.digitalwire.get("urgency", 3)


def get_keywords(context: Context) -> list[str]:
    """
    Returns all keyword names.
    :param context: A context object of the digitalwires message.
    :return: A list of keyword names.
    """
    return context.digitalwire.get("keyword_names", [])


def get_embargo(context: Context) -> str:
    """
    Returns the embargo date.
    :param context: A context object of the digitalwires message.
    :return: The embargo date as a string.
    """
    return context.digitalwire.get("embargoed", "")


def get_byline(context: Context) -> str:
    """
    Returns the byline.
    :param context: A context object of the digitalwires message.
    :return: The byline as a string. Never ``None``.
    """
    byline = context.digitalwire.get("byline", "")
    return byline if byline else ""
