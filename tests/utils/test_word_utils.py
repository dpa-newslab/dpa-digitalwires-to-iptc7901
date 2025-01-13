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
from iptc7901.utils.WordUtils import article_html_to_text, TextHTML2Text

logger = logging.getLogger()


def test_article_html_to_text():
    html = '<section class="main"><p>Lorem<br/><br/>Ipsum</p></section>'
    result = TextHTML2Text().handle(html)

    logger.info(result)
    assert result is not None
    assert result == "Lorem\n\nIpsum\n"


def test_article_html_to_text_li():
    html = '<section class="main"><ul><li>Einzelmeldungen</li><li>Zusammenfassung, «Erste Schritte auf dem Weg zu «Brombeer»-Koalitionen» - 96 Zl.</li><li>Grafik-Diagramm Nr. 107865, Querformat 90 x 70 mm, «Mögliche Koalitionen (weiter aktuell)»</li><li>Video-Digital-Beitrag</li></ul><p>+++ Deutschland;Brandenburg;Wahlen;Landtag; +++</p><p></p><p>Berlin<br/></section>'
    result = article_html_to_text(html)

    logger.info(result)
    assert result is not None
    assert (
        result
        == """  * Einzelmeldungen
  * Zusammenfassung, «Erste Schritte auf dem Weg zu
«Brombeer»-Koalitionen» - 96 Zl.
  * Grafik-Diagramm Nr. 107865, Querformat 90 x 70 mm, «Mögliche
Koalitionen (weiter aktuell)»
  * Video-Digital-Beitrag

+++ Deutschland;Brandenburg;Wahlen;Landtag; +++



Berlin
"""
    )
