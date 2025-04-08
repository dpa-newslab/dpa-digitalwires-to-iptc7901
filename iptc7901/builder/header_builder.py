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
from typing import Callable, Any

from iptc7901.builder import AbstractIptcBuilder
from iptc7901.digitalwires_model import DigitalwiresModel
from iptc7901.builder import TextBuilder
from iptc7901.extractor import (
    get_ressort,
    get_services,
    get_dpa_subjects,
    get_geo_subject,
    get_urgency,
    get_keywords,
)
from iptc7901.renderer import render_header, render_subject
from iptc7901.utils import extend_if_not_empty, service_to_iptc_agency_map


class HeaderBuilder(AbstractIptcBuilder):
    def __init__(
        self, dw_model: DigitalwiresModel, find_sequence: Callable[[str], Any] = None
    ):
        super().__init__(dw_model)
        self.find_sequence = find_sequence

    def build(self) -> str:
        return next(
            iter(
                [
                    self.build_with(
                        len(TextBuilder(dw_model=self.dw_model).build().split()),
                        service.qcode,
                    )
                    for service in get_services(self.dw_model)
                ]
            )
        )

    def build_with(self, word_count: int, service_qcode: str) -> str:
        result = []
        service = service_qcode.split(":")[-1]
        extend_if_not_empty(
            result,
            render_header(
                self.dw_model,
                word_count,
                lambda c: service,
                (
                    next(self.find_sequence(service_qcode))
                    if self.find_sequence is not None
                    else 0
                ),
                get_urgency,
                get_ressort,
                (
                    next(
                        self.find_sequence(
                            f"dpaagenturzeichen:{service_to_iptc_agency_map.get(service, 'dpa')}"
                        )
                    )
                    if self.find_sequence is not None
                    else 0
                ),
            ),
        )

        return "".join(result)


class SluglineBuilder(AbstractIptcBuilder):
    def __init__(self, dw_model: DigitalwiresModel):
        super().__init__(dw_model)

    def build(self) -> str:
        result = []
        if self.dw_model.lang() == "de":
            extend_if_not_empty(
                result,
                render_subject(self.dw_model, [get_dpa_subjects, get_geo_subject]),
            )
        else:
            extend_if_not_empty(
                result,
                render_subject(self.dw_model, [get_geo_subject, get_dpa_subjects]),
            )
        extend_if_not_empty(result, render_subject(self.dw_model, [get_keywords]))

        slugline = ""
        for line in result:
            if len(slugline) + len(line) < 69:
                slugline = slugline + ("/" if len(slugline) > 0 else "") + line
        return slugline + "/"
