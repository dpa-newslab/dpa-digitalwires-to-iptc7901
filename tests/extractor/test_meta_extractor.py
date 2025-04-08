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
import re

import arrow
from jinja2.nodes import Keyword

from iptc7901 import DigitalwiresModel
from iptc7901.extractor.meta_extractor import (
    get_dateline,
    get_version_created,
    get_urgency,
    get_keywords,
    get_embargo,
    get_byline,
)
from iptc7901.utils import Category

logger = logging.getLogger()


def test_dateline_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_dateline(dw_model)

        logger.info(result)
        assert (
            re.search(r".+\s\(.+\)\s+-\s*", result) is not None
            if len(result) > 0
            else True
        )


def test_version_created_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_version_created(dw_model)

        logger.info(result)
        assert len(result) > 0
        assert arrow.get(result) is not None


def test_urgency_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_urgency(dw_model)

        logger.info(result)
        assert result > 0


def test_keyword_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_keywords(dw_model)

        logger.info(result)
        assert len(result) >= 0
        for keyword in result:
            assert type(keyword) == Category
            assert len(keyword.name) > 0


def test_embargo_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_embargo(dw_model)

        logger.info(result)
        assert arrow.get(result) is not None if result is not None else True


def test_byline_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_byline(dw_model)

        logger.info(result)
        assert len(result) >= 0
