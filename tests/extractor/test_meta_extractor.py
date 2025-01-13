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

import arrow
import logging
import pytest
import re

from iptc7901 import Context
from iptc7901.extractor.meta_extractor import (
    get_dateline,
    get_version_created,
    get_urgency,
    get_keywords,
    get_embargo,
    get_byline,
)

logger = logging.getLogger()


@pytest.fixture(scope="module")
def test_data_filenames():
    return [
        "dw-1.json",
        "eil.json",
        "lesestuecke.json",
        "nsb-n1.json",
        "tvo-pol.json",
        "spe-tab.json",
        "rubix-multimedia-real.json",
        "rubix-multimedia-testartikel.json",
        "hoerfunk.json",
        "spe2.json",
        "noNotepad.json",
    ]


def test_dateline_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_dateline(context)

        logger.info(result)
        assert (
            re.search(r".+\s\(.+\)\s+-\s*", result) is not None
            if len(result) > 0
            else True
        )


def test_version_created_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_version_created(context)

        logger.info(result)
        assert len(result) > 0
        assert arrow.get(result) is not None


def test_urgency_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_urgency(context)

        logger.info(result)
        assert result > 0


def test_keyword_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_keywords(context)

        logger.info(result)
        assert len(result) >= 0
        for keyword in result:
            assert len(keyword) > 0


def test_embargo_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_embargo(context)

        logger.info(result)
        assert arrow.get(result) is not None if result is not None else True


def test_byline_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_byline(context)

        logger.info(result)
        assert len(result) >= 0
