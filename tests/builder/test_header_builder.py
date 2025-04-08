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

from iptc7901 import DigitalwiresModel
from iptc7901.builder import HeaderBuilder, SluglineBuilder

logger = logging.getLogger()


@pytest.fixture(scope="module")
def test_data_filenames():
    return ["dw-1.json", "eil.json", "lesestuecke.json", "nsb-n1.json", "tvo-pol.json"]


def test_header_builder(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        dw_model = DigitalwiresModel(dw)
        builder = HeaderBuilder(dw_model)
        result = builder.build_with(42, "bdt")

        logger.info(result)
        assert len(result) > 0
        assert result.startswith("bdt")
        assert result.endswith("0000")


def test_header_builder_with_sequence(test_data_json):
    for filename, file in test_data_json.items():
        from collections import defaultdict
        from itertools import count

        _sequences = defaultdict(count)

        def find_sequence(key):
            return _sequences[key]

        dw_model = DigitalwiresModel(file)
        builder = HeaderBuilder(dw_model, find_sequence)
        result = builder.build_with(42, "bdt")

        logger.info(result)
        assert len(result) > 0
        assert result.startswith("bdt0000")
        assert result.endswith("0000")

        builder = HeaderBuilder(dw_model, find_sequence)
        result = builder.build_with(42, "bdt")

        logger.info(result)
        assert len(result) > 0
        assert result.startswith("bdt0001")
        assert result.endswith("0001")


def test_slugline_builder(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        dw_model = DigitalwiresModel(dw)
        builder = SluglineBuilder(dw_model)
        result = builder.build()

        logger.info(result)
        assert len(result) > 0
        assert result.count("/") > 0
