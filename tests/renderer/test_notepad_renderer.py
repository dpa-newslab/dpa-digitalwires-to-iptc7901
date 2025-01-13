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
from iptc7901.renderer.notepad_renderer import (
    render_public_notepad,
    render_nonpublic_notepad,
)

logger = logging.getLogger()


def test_public_notepad_renderer():
    result = render_public_notepad(None, [lambda c: "Foo bar", lambda c: "Lorem Ipsum"])

    logger.info(result)
    assert len(result) == 2
    assert result[0] == "Foo bar"
    assert result[1] == "Lorem Ipsum"


def test_nonpublic_notepad_renderer():
    result = render_nonpublic_notepad(
        None, [lambda c: "Foo bar", lambda c: "Lorem Ipsum"]
    )

    logger.info(result)
    assert len(result) == 3
    assert result[0] == "* * * *"
    assert result[1] == "Foo bar"
    assert result[2] == "Lorem Ipsum"


def test_notepad_header_renderer():
    result = render_public_notepad(None, [lambda c: "Foo bar", lambda c: "Lorem Ipsum"])

    logger.info(result)
    assert len(result) == 2
    assert result[0] == "Foo bar"
    assert result[1] == "Lorem Ipsum"
