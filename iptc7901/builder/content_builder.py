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

from iptc7901.builder import AbstractIptcBuilder
from iptc7901.digitalwires_model import DigitalwiresModel
from iptc7901.extractor import get_article, get_teaser, get_closing_line, get_dateline
from iptc7901.renderer import (
    render_article,
    render_teaser,
    render_closing_line,
)
from iptc7901.utils.collection_utils import extend_if_not_empty


class TextBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        extend_if_not_empty(
            result, render_article(self.dw_model, get_dateline, [get_article])
        )

        return "".join(result)


class TeaserBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        extend_if_not_empty(result, render_teaser(self.dw_model, [get_teaser]))
        return "".join(result)


class ClosingLineBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        extend_if_not_empty(
            result, render_closing_line(self.dw_model, [get_closing_line])
        )

        return "".join(result)
