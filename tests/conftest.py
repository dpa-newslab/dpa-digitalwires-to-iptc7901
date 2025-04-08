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

import json
import os
import pytest


@pytest.fixture(scope="module")
def test_data_json(test_data_filenames):
    test_jsons = dict()
    for filename in test_data_filenames:
        file_path = os.path.join(os.path.dirname(__file__), "data/input", filename)
        with open(file_path) as f:
            test_jsons[filename] = json.load(f)
    return test_jsons


@pytest.fixture(scope="module")
def result_data_iptc(result_data_filenames):
    result_iptc = dict()
    for filename in result_data_filenames:
        file_path = os.path.join(os.path.dirname(__file__), "data/output", filename)
        with open(file_path) as f:
            result_iptc[filename] = f.read()
    return result_iptc


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
        "emptyParagraph.json",
    ]


@pytest.fixture(scope="module")
def result_data_filenames():
    return [
        "dw-1.iptc",
        "eil.iptc",
        "lesestuecke.iptc",
        "nsb-n1.iptc",
        "tvo-pol.iptc",
        "spe-tab.iptc",
    ]
