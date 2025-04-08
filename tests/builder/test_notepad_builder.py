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
from iptc7901.builder import NotepadBuilder

logger = logging.getLogger()


@pytest.fixture(scope="module")
def test_data_filenames():
    return ["dw-1.json", "eil.json", "lesestuecke.json", "nsb-n1.json", "tvo-pol.json"]


def test_notepad_builder(test_data_json):
    dw = test_data_json["dw-1.json"]
    dw_model = DigitalwiresModel(dw)
    builder = NotepadBuilder(dw_model)
    result = builder.build()

    logger.info(result)
    assert len(result) > 0
    assert len(result) == 2330
    assert len(result.split("\n")) == 61
    assert result.startswith("# Notizblock")
