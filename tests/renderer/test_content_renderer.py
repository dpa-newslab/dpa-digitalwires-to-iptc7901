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

from iptc7901.renderer import (
    render_article,
    render_date_time,
    render_closing_line,
    render_teaser,
)

logger = logging.getLogger()


def test_article_renderer_single_extractor():
    result = render_article(
        None,
        lambda c: "Start Prefix - ",
        [lambda c: '<section class="main"><p>Lorem Ipsum</p></section>'],
    )

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "Start Prefix - Lorem Ipsum\n"


def test_article_renderer_multiple_extractor():
    result = render_article(
        None,
        lambda c: "Start Prefix - ",
        [
            lambda c: '<section class="main"><p>Lorem Ipsum</p></section>',
            lambda c: '<section class="main"><p>Foo bar</p></section>',
        ],
    )

    logger.info(result)
    assert len(result) == 2
    assert result[0] == "Start Prefix - Lorem Ipsum\n"
    assert result[1] == "Start Prefix - Foo bar\n"


def test_article_renderer_empty_paragraph():
    result = render_article(
        None,
        lambda c: "Start Prefix - ",
        [
            lambda c: '<section class="main"><p></p><p>Lorem Ipsum</p></section>',
            lambda c: '<section class="main"><p>Foo bar</p></section>',
        ],
    )

    logger.info(result)
    assert len(result) == 2
    assert result[0] == "Start Prefix -\n\nLorem Ipsum\n"
    assert result[1] == "Start Prefix - Foo bar\n"


def test_date_time_renderer():
    result = render_date_time(
        None,
        [lambda c: "2024-09-25T10:37:24+02:00", lambda c: "2024-10-25T10:37:24+02:00"],
    )

    logger.info(result)
    assert len(result) == 2
    assert result[0] == "251037 Sep 24"
    assert result[1] == "251037 Okt 24"


def test_closing_line_renderer():
    result = render_closing_line(None, [lambda c: "Lorem Ipsum", lambda c: "Foo bar"])

    logger.info(result)
    assert len(result) == 2
    assert result[0] == "Lorem Ipsum"
    assert result[1] == "Foo bar"


def test_teaser_renderer():
    result = render_teaser(
        None,
        [
            lambda c: "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
            lambda c: "Foo bar",
        ],
    )

    logger.info(result)
    assert len(result) == 2
    assert len(result[0].split("\n")) == 9
    for line in result[0].split("\n"):
        assert len(line) <= 69
    assert len(result[1].split("\n")) == 1
    for line in result[1].split("\n"):
        assert len(line) <= 69


def test_teaser_renderer_with_empty():
    result = render_teaser(None, [lambda c: ""])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == ""
