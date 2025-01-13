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
import pytest

from iptc7901.Context import Context
from iptc7901.builder.content_builder import TextBuilder
from iptc7901.builder.header_builder import HeaderBuilder, SluglineBuilder

logger = logging.getLogger()


@pytest.fixture(scope="module")
def test_data_filenames():
    return ["dw-1.json", "eil.json", "lesestuecke.json", "nsb-n1.json", "tvo-pol.json"]


def test_header_builder(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        builder = HeaderBuilder(context)
        result = builder.build_with(42, "bdt")

        logger.info(result)
        assert len(result) > 0
        assert result.startswith("bdt")
        assert result.endswith("0000")


def test_slugline_builder(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        builder = SluglineBuilder(context)
        result = builder.build()

        logger.info(result)
        assert len(result) > 0
        assert result.count("/") > 0
