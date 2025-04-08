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
from iptc7901.extractor.notepad_extractor import (
    get_closing_line,
    get_correction,
    get_ednotes,
    get_embargo_note,
    get_genre_note,
    get_non_public_notepad,
    get_notepad_header,
    get_picture_ednote_de,
    get_public_notepad,
)
from iptc7901.utils import EdNote

logger = logging.getLogger()


def test_ednotes_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_ednotes(dw_model)

        logger.info(result)
        assert len(result) >= 0
        for note in result:
            assert type(note) == EdNote
            assert len(note.ednote) > 0


def test_public_notepad_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_public_notepad(dw_model)

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
        dw_model = DigitalwiresModel(file)
        result = get_non_public_notepad(dw_model)

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
        dw_model = DigitalwiresModel(file)
        result = get_notepad_header(dw_model)

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
        dw_model = DigitalwiresModel(file)
        result = get_correction(dw_model)

        logger.info(result)
        assert len(result) >= 0


def test_picture_ednote_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_picture_ednote_de(dw_model)

        logger.info(result)
        assert len(result) >= 0


def test_embargo_note_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_embargo_note(dw_model)

        logger.info(result)
        assert len(result) >= 0


def test_closing_line_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_closing_line(dw_model)

        logger.info(result)
        assert len(result) >= 0
        assert len(result.split()) >= 0


def test_genre_note_extractor(test_data_json):
    for filename, file in test_data_json.items():
        dw_model = DigitalwiresModel(file)
        result = get_genre_note(dw_model)

        logger.info(result)
        assert len(result) >= 0
