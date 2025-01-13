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

from iptc7901 import Context
from iptc7901.extractor.category_extractor import (
    get_dpa_subjects,
    get_geo_subject,
    get_genre_qcode,
    get_genre_name,
    get_ressort,
    get_services,
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


def test_dpa_subject_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_dpa_subjects(context)

        logger.info(result)
        assert len(result) >= 0
        for subject in result:
            assert len(subject) > 0


def test_geo_subject_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_geo_subject(context)

        logger.info(result)
        assert len(result) >= 0
        for subject in result:
            assert len(subject) > 0


def test_dpa_and_geo_subject_extractor_are_disjoint(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_geo_subject(context)

        logger.info(result)
        assert len(result) >= 0
        assert set(result).isdisjoint(get_dpa_subjects(context))


def test_genre_qcode_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_genre_qcode(context)

        logger.info(result)
        assert len(result) >= 0
        assert result.count(":") == 1


def test_genre_name_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_genre_name(context)

        logger.info(result)
        assert len(result) > 0


def test_ressort_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_ressort(context)

        logger.info(result)
        assert 0 < len(result.split(":")[-1]) <= 3


def test_service_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_services(context)

        logger.info(result)
        assert len(result) > 0
        for service in result:
            assert len(service.split(":")[-1]) == 3 or service.split(":")[-1] in [
                "sch3pb",
                "apwire",
            ]
