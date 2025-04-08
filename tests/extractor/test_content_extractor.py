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

import logging

from iptc7901 import DigitalwiresModel
from iptc7901.extractor import get_article, get_teaser, get_headline
from iptc7901.utils import article_html_to_text

logger = logging.getLogger()


def test_article_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_article(dw_model)

        logger.info(result)
        if result is not None:
            assert len(result) > 0
            assert result.startswith('<section class="main">')
            assert result.endswith("</section>")
            assert len(article_html_to_text(result)) > 0


def test_teaser_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_teaser(dw_model)

        logger.info(result)
        assert result == dw_model.get("teaser", "")


def test_headline_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_headline(dw_model)

        logger.info(result)
        assert len(result) > 0
