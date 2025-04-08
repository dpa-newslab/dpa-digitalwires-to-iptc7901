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

from iptc7901 import convert_to_iptc

logger = logging.getLogger()


def test_single_text_converter(test_data_json, result_data_iptc):
    filename = "dw-1.json"
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
        logger.info(results[filename])


def test_with_sequence(test_data_json):
    from collections import defaultdict
    from itertools import count

    _sequences = defaultdict(count)

    def find_sequence(key):
        return _sequences[key]

    old_sequence_values = {}
    for filename, dw in test_data_json.items():
        results = convert_to_iptc(dw, find_sequence)

        logger.info(f"Testing {filename}:")
        logger.info(results)
        for iptc in results.values():
            assert len(iptc) > 0
            assert iptc.startswith("\x01")
            sequence_regex = r"([a-zA-Z]{3,}) ?(\d{4})"
            sequence_numbers = re.findall(sequence_regex, iptc.split("\n")[0])
            assert len(sequence_numbers) == 2
            logging.info(sequence_numbers)
            assert int(sequence_numbers[0][1]) >= 0
            assert int(sequence_numbers[1][1]) >= 0
            if sequence_numbers[0][0] in old_sequence_values:
                assert old_sequence_values[sequence_numbers[0][0]] + 1 == int(
                    sequence_numbers[0][1]
                )
            if sequence_numbers[1][0] in old_sequence_values:
                assert old_sequence_values[sequence_numbers[1][0]] + 1 == int(
                    sequence_numbers[1][1]
                )
            old_sequence_values[sequence_numbers[0][0]] = int(sequence_numbers[0][1])
            old_sequence_values[sequence_numbers[1][0]] = int(sequence_numbers[1][1])
            assert iptc.endswith("\x7f\n\x7f\x04")
