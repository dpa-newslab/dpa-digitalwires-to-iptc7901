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
from iptc7901.renderer.header_renderer import render_header, render_subject

logger = logging.getLogger()


def test_header_renderer():
    result = render_header(
        None, 42, lambda c: "bdt", 21, lambda c: 3, lambda c: "vm", 23
    )

    logger.info(result)
    assert len(result) > 0
    assert result == "bdt0021 3 vm 42  dpa 0023"


def test_subject_renderer():
    result = render_subject(
        None, [lambda c: ["Foo", "bar", "baz"], lambda c: ["Lorem", "ipsum"]]
    )

    logger.info(result)
    assert len(result) == 5
    assert result[0] == "Foo"
    assert result[1] == "bar"
    assert result[2] == "baz"
    assert result[3] == "Lorem"
    assert result[4] == "ipsum"
