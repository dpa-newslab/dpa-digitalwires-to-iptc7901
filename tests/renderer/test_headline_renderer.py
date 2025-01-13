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

from iptc7901 import Context
from iptc7901.renderer.headline_renderer import (
    render_title,
    render_correction,
    render_ednote_de,
    render_genre,
    render_byline,
    render_prio,
)
from iptc7901.utils import Symbols

logger = logging.getLogger()


def test_title_renderer():
    result = render_title(None, [lambda c: "Foo bar="])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "Foo bar"


def test_title_renderer_multiple_extractor():
    result = render_title(None, [lambda c: "Lorem Ipsum", lambda c: 'Foo "bar"='])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == 'Lorem Ipsum\nFoo "bar"'


def test_correction_renderer_de():
    dw = {
        "signal": "sig:update",
        "language": "de",
        "article_html": '<section class="main"></section>',
    }
    context = Context(dw)
    result = render_correction(context, [lambda c: "Foo bar"])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "(Aktualisierung: Foo bar)"


def test_correction_renderer_de_cancled():
    dw = {
        "signal": "sig:update",
        "language": "de",
        "pubstatus": "canceled",
        "article_html": '<section class="main"></section>',
    }
    context = Context(dw)
    result = render_correction(context, [lambda c: "Foo bar"])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "(Achtung) Foo bar"


def test_correction_renderer_en():
    dw = {
        "signal": "sig:update",
        "language": "en",
        "article_html": '<section class="main"></section>'
    }
    context = Context(dw)
    result = render_correction(context, [lambda c: "Foo bar"])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "Update"


def test_ednote_de_renderer():
    result = render_ednote_de(None, [lambda c: "Foo bar", lambda c: "removed"])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "(Foo bar)"


def test_genre_renderer():
    dw = {"language": "de", "article_html": '<section class="main"></section>'}
    context = Context(dw)
    result = render_genre(
        context,
        lambda c: "dpatextgenre:9",
        lambda c: "Gesamtzusammenfassung",
        lambda c: "Foo",
    )

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "Gesamtzusammenfassung - Foo"


def test_genre_renderer_dashless():
    dw = {"language": "de", "article_html": '<section class="main"></section>'}
    context = Context(dw)
    result = render_genre(
        context,
        lambda c: "dpatextgenre:8",
        lambda c: "Feiertagszusammenfassung",
        lambda c: "Foo",
    )

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "Feiertagszusammenfassung Foo"


def test_byline_renderer():
    result = render_byline(None, [lambda c: "Foo Bar", lambda c: "ignored"])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "Foo Bar"


def test_prio_renderer_prio1():
    dw = {"language": "de", "article_html": '<section class="main"></section>'}
    context = Context(dw)
    result = render_prio(context, [lambda c: 1, lambda c: 99])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "(Blitz " + Symbols.BELL * 10 + ")"


def test_prio_renderer_prio2():
    dw = {"language": "de", "article_html": '<section class="main"></section>'}
    context = Context(dw)
    result = render_prio(context, [lambda c: 2, lambda c: 99])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == "(Eil " + Symbols.BELL * 5 + ")"


def test_prio_renderer_prio3():
    dw = {"language": "de", "article_html": '<section class="main"></section>'}
    context = Context(dw)
    result = render_prio(context, [lambda c: 3, lambda c: 99])

    logger.info(result)
    assert len(result) == 1
    assert result[0] == ""
