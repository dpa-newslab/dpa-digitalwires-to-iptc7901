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
from iptc7901.extractor import (
    get_notepad_header,
    get_public_notepad,
    get_non_public_notepad,
)
from iptc7901.renderer import (
    render_notepad_header,
    render_public_notepad,
    render_nonpublic_notepad,
)
from iptc7901.utils import extend_if_not_empty


class NotepadBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        extend_if_not_empty(
            result, render_notepad_header(self.dw_model, [get_notepad_header])
        )
        extend_if_not_empty(
            result, render_public_notepad(self.dw_model, [get_public_notepad])
        )
        extend_if_not_empty(
            result, render_nonpublic_notepad(self.dw_model, [get_non_public_notepad])
        )

        return "\n".join(result)
