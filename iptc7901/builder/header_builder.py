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

from collections.abc import Generator

from iptc7901 import Context
from iptc7901.builder.AbstractIptcBuilder import AbstractIptcBuilder
from iptc7901.builder.content_builder import TextBuilder
from iptc7901.extractor.category_extractor import (
    get_ressort,
    get_services,
    get_dpa_subjects,
    get_geo_subject,
)
from iptc7901.extractor.meta_extractor import get_urgency, get_keywords
from iptc7901.renderer.header_renderer import render_header, render_subject
from iptc7901.utils.CollectionUtils import extend_if_not_empty
from iptc7901.utils.Mappings import service_to_iptc_agency_map


class HeaderBuilder(AbstractIptcBuilder):
    def __init__(
        self,
        context: Context,
        service_sequence_generator: Generator[int, str, None] = None,
        agency_sequence_generator: Generator[int, str, None] = None,
    ):
        super().__init__(context)
        self.service_sequence_generator = service_sequence_generator
        self.agency_sequence_generator = agency_sequence_generator
        if self.service_sequence_generator is not None:
            next(self.service_sequence_generator)
        if self.agency_sequence_generator is not None:
            next(self.agency_sequence_generator)

    def build(self) -> str:
        return next(
            iter(
                [
                    self.build_with(
                        len(TextBuilder(context=self.context).build().split()), service
                    )
                    for service in get_services(self.context)
                ]
            )
        )

    def build_with(self, word_count: int, service_qcode: str) -> str:
        result = []
        service = service_qcode.split(":")[-1]
        extend_if_not_empty(
            result,
            render_header(
                self.context,
                word_count,
                lambda c: service,
                (
                    self.service_sequence_generator.send(service)
                    if self.service_sequence_generator is not None
                    else 0
                ),
                get_urgency,
                get_ressort,
                (
                    self.agency_sequence_generator.send(
                        service_to_iptc_agency_map.get(service, "dpa")
                    )
                    if self.agency_sequence_generator is not None
                    else 0
                ),
            ),
        )

        return "".join(result)


class SluglineBuilder(AbstractIptcBuilder):
    def __init__(self, context: Context):
        super().__init__(context)

    def build(self) -> str:
        result = []
        if self.context.lang == "de":
            extend_if_not_empty(
                result,
                render_subject(self.context, [get_dpa_subjects, get_geo_subject]),
            )
        else:
            extend_if_not_empty(
                result,
                render_subject(self.context, [get_geo_subject, get_dpa_subjects]),
            )
        extend_if_not_empty(result, render_subject(self.context, [get_keywords]))

        slugline = ""
        for line in result:
            if len(slugline) + len(line) < 69:
                slugline = slugline + ("/" if len(slugline) > 0 else "") + line
        return slugline + "/"
