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


def get_article(dw_model: DigitalwiresModel) -> str:
    """Returns the article.

    :param dw_model: A model of the digitalwires message.
    :return: The article as a string in HTML.
    """
    return dw_model["article_html"]


def get_teaser(dw_model: DigitalwiresModel) -> str:
    """Returns the teaser.

    :param dw_model: A model of the digitalwires message.
    :return: The teaser as a string.
    """
    return dw_model["teaser"]


def get_headline(dw_model: DigitalwiresModel) -> str:
    """Returns the headline.

    :param dw_model: A model of the digitalwires message.
    :return: The headline as a string.
    """
    return dw_model["headline"]
