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
from iptc7901.extractor import (
    get_dpa_subjects,
    get_geo_subject,
    get_genre_qcode,
    get_genre_name,
    get_ressort,
    get_services,
)
from iptc7901.utils import Category

logger = logging.getLogger()


def test_dpa_subject_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_dpa_subjects(dw_model)

        logger.info(result)
        assert len(result) >= 0
        for subject in result:
            assert type(subject) == Category
            assert len(subject.name) > 0


def test_geo_subject_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_geo_subject(dw_model)

        logger.info(result)
        assert len(result) >= 0
        for subject in result:
            assert type(subject) == Category
            assert len(subject.name) > 0


def test_dpa_and_geo_subject_extractor_are_disjoint(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_geo_subject(dw_model)

        logger.info(result)
        assert len(result) >= 0
        assert set(result).isdisjoint(get_dpa_subjects(dw_model))


def test_genre_qcode_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_genre_qcode(dw_model)

        logger.info(result)
        assert len(result) >= 0
        assert result.count(":") == 1 if len(result) >= 1 else True


def test_genre_name_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_genre_name(dw_model)

        logger.info(result)
        assert result is not None


def test_ressort_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_ressort(dw_model)

        logger.info(result)
        assert 0 < len(result.split(":")[-1]) <= 3


def test_service_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_services(dw_model)

        logger.info(result)
        assert len(result) > 0
        for service in result:
            assert type(service) == Category
            assert len(service.qcode.split(":")) == 2
