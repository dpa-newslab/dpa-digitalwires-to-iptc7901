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
    get_correction,
    get_picture_ednote_de,
    get_genre_note,
    get_embargo_note,
    get_genre_qcode,
    get_genre_name,
    get_headline,
    get_urgency,
    get_embargo,
    get_byline,
)
from iptc7901.renderer import (
    render_prio,
    render_correction,
    render_genre,
    render_embargo,
    render_title,
    render_byline,
    render_ednote_de,
)
from iptc7901.utils import extend_if_not_empty


def create_headline_builder(dw_model: DigitalwiresModel) -> AbstractIptcBuilder:
    if dw_model.lang() == "de":
        return HeadlineDeBuilder(dw_model)
    elif dw_model.lang() == "es":
        return HeadlineEsBuilder(dw_model)
    else:
        return HeadlineInternationalBuilder(dw_model)


class HeadlineDeBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        extend_if_not_empty(result, render_prio(self.dw_model, [get_urgency]))
        extend_if_not_empty(result, render_correction(self.dw_model, [get_correction]))

        genre = next(
            iter(
                render_genre(
                    self.dw_model, get_genre_qcode, get_genre_name, get_genre_note
                )
            ),
            "",
        )
        embargo = next(
            iter(render_embargo(self.dw_model, get_embargo, get_embargo_note)), ""
        )
        genre_embargo = " ".join([genre, embargo]).strip()
        if genre_embargo != "":
            result.append("(" + genre_embargo + ")")

        extend_if_not_empty(result, render_title(self.dw_model, [get_headline]))
        extend_if_not_empty(result, render_byline(self.dw_model, [get_byline]))
        extend_if_not_empty(
            result, render_ednote_de(self.dw_model, [get_picture_ednote_de])
        )
        result[-1] = result[-1] + " ="
        return self.wrap_line(result)


class HeadlineInternationalBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)
        self.cancel_note = {
            "en": "KILL KILL KILL",
            "fr": "KILL KILL KILL",
            "pl": "KILL KILL KILL",
            "ru": "АННУЛИРОВАНИЕ",
            "ar": "حظر حظر حظر",
        }

    def build(self) -> str:
        result = []
        if self.dw_model.canceled():
            result.append(self.cancel_note[self.dw_model.lang()])
        else:
            result.extend(render_correction(self.dw_model, [get_correction]))
            result.extend(
                render_genre(
                    self.dw_model, get_genre_qcode, get_genre_name, get_genre_note
                )
            )
            prio_title = (
                next(iter(render_prio(self.dw_model, [get_urgency])))
                + " "
                + next(iter(render_title(self.dw_model, [get_headline])))
            )
            result.append(prio_title.strip())
            result.extend(render_byline(self.dw_model, [get_byline]))
        result[-1] = result[-1] + " ="
        return self.wrap_line(result)


class HeadlineEsBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        if self.dw_model.canceled():
            result.append("*** ELIMINAR - ELIMINAR ***")
            result.append("ATENCION REDACCIONES")
        else:
            result.extend(render_correction(self.dw_model, [get_correction]))
            result.extend(
                render_genre(
                    self.dw_model, get_genre_qcode, get_genre_name, get_genre_note
                )
            )
            prio_title = (
                next(iter(render_prio(self.dw_model, [get_urgency])))
                + " "
                + next(iter(render_title(self.dw_model, [get_headline])))
            )
            result.append(prio_title.strip())
            result.extend(render_byline(self.dw_model, [get_byline]))
        result[-1] = result[-1] + " ="
        return self.wrap_line(result)
