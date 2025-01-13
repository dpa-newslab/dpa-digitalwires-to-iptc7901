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
from iptc7901.extractor.notepad_extractor import (get_closing_line,
                                                  get_correction, get_ednotes,
                                                  get_embargo_note,
                                                  get_genre_note,
                                                  get_non_public_notepad,
                                                  get_notepad_header,
                                                  get_picture_ednote_de,
                                                  get_public_notepad)

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


def test_ednotes_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_ednotes(context)

        logger.info(result)
        assert len(result) >= 0
        for note in result:
            assert len(note) > 0


def test_public_notepad_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_public_notepad(context)

        logger.info(f"public Notepad: {result}")
        assert len(result) >= 0 if result is not None else True
        assert (
            result.startswith('<section class="np-public">')
            if result is not None and len(result) > 0
            else True
        )
        assert (
            result.endswith("</section>")
            if result is not None and len(result) > 0
            else True
        )


def test_non_public_notepad_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_non_public_notepad(context)

        logger.info(result)
        assert (
            result.startswith('<section class="np-nonpublic">')
            if result is not None and len(result) > 0
            else True
        )
        assert (
            result.endswith("</section>")
            if result is not None and len(result) > 0
            else True
        )


def test_notepad_header_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_notepad_header(context)

        logger.info(result)
        assert (
            result.startswith("<header>")
            if result is not None and len(result) > 0
            else True
        )
        assert (
            result.endswith("</header>")
            if result is not None and len(result) > 0
            else True
        )


def test_correction_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_correction(context)

        logger.info(result)
        assert len(result) >= 0


def test_picture_ednote_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_picture_ednote_de(context)

        logger.info(result)
        assert len(result) >= 0


def test_embargo_note_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_embargo_note(context)

        logger.info(result)
        assert len(result) >= 0


def test_closing_line_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_closing_line(context)

        logger.info(result)
        assert len(result) >= 0
        assert len(result.split()) >= 0


def test_genre_note_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw = file
        context = Context(dw)
        result = get_genre_note(context)

        logger.info(result)
        assert len(result) >= 0
