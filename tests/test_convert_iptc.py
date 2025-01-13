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

from collections.abc import Generator
from iptc7901 import convert_to_iptc

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
        "noContent.json",
        "emptyParagraph.json"
    ]


@pytest.fixture(scope="module")
def result_data_filenames():
    return [
        "dw-1.iptc",
        "eil.iptc",
        "lesestuecke.iptc",
        "nsb-n1.iptc",
        "tvo-pol.iptc",
        "spe-tab.iptc"
    ]


def test_single_text_converter(test_data_json, result_data_iptc):
    filename = "emptyParagraph.json"
    results = convert_to_iptc(test_data_json[filename])

    for service, result in results.items():
        logger.info(result)
        assert len(result) > 0
        assert result.startswith("\x01")
        assert result.endswith("\x7f\n\x7f\x04")
    compares = [
        iptc == result_data_iptc[filename.replace(".json", ".iptc")].strip()
        for iptc in results.values()
        if filename.replace(".json", ".iptc") in result_data_iptc
    ]
    assert any(compares) if len(compares) > 0 else True


def test_text_builder(test_data_json, result_data_iptc):
    def gen() -> Generator[int, str, None]:
        sequence_name = yield 1
        dpa_sequence = 21
        other_sequence = 23
        while True:
            if sequence_name == "dpa":
                yield dpa_sequence
                dpa_sequence += 1
            else:
                yield other_sequence
                other_sequence += 1

    results = {filename: convert_to_iptc(dw) for filename, dw in test_data_json.items()}

    logger.info(results)
    assert len(results) > 0
    for filename, result in results.items():
        logger.info(f"Testing {filename}:")
        for iptc in result.values():
            assert len(iptc) > 0
            assert iptc.startswith("\x01")
            assert iptc.endswith("\x7f\n\x7f\x04")
        compares = [
            iptc == result_data_iptc[filename.replace(".json", ".iptc")].strip()
            for iptc in result.values()
            if filename.replace(".json", ".iptc") in result_data_iptc
        ]
        assert any(compares) if len(compares) > 0 else True
        if filename.replace(".json", ".iptc") not in result_data_iptc:
            logger.info(results[filename])
