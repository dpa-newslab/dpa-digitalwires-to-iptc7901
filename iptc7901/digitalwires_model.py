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
from dataclasses import dataclass
from operator import itemgetter
from typing import Any

from iptc7901.utils import get_none_safe, get_rank, Category, EdNote


@dataclass
class DigitalwiresModel(object):
    """A data model for representing and accessing digitalwire dictionaries.

    This class provides a convenient interface for working with digitalwire data,
    offering easier access to collections such as editorial notes (ednotes) and
    categories. It also implements safeguards against KeyErrors for missing dictionary
    keys.

    The class uses a custom sorting mechanism based on a 'rank' attribute and provides
    flexibility in selecting specific attributes from the items. It also implements
    safeguards against None values in the underlying data structure.
    """

    digitalwire: dict[str, Any]

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=None):
        return self.digitalwire.get(key, default)

    def __missing__(self, key):
        return None

    def category_items(self, cat_type=None, attrs: list[str] = None) -> list[Category]:
        type_filter = {"key": "type", "value": cat_type} if cat_type else None
        return [
            Category(**dict(zip(Category.map_dw_key(attrs), cat)))
            for cat in self.get_sorted_list(attrs, "categories", type_filter)
        ]

    def notepad_items(self, notepad_role=None, attrs: list[str] = None) -> list[EdNote]:
        role_filter = {"key": "role", "value": notepad_role} if notepad_role else None
        return [
            EdNote(**dict(zip(attrs, ednote)))
            for ednote in self.get_sorted_list(attrs, "ednotes", role_filter)
        ]

    def get_sorted_list(self, attrs, col_field, filter_options):
        if attrs is None:
            attrs = ["type", "name", "qcode", "rank"]
        return [
            (
                itemgetter(*attrs)(KeySafeDict(categorie))
                if len(attrs) > 1
                else [itemgetter(*attrs)(KeySafeDict(categorie))]
            )
            for categorie in sorted(
                get_none_safe(self, col_field, []),
                key=lambda cat: get_rank(cat),
            )
            if not filter_options
            or categorie.get(filter_options["key"], "") == filter_options["value"]
        ]

    def _count_associations(self) -> int:
        return len(self.get("associations", []))

    def has_no_content(self) -> bool:
        return self["article_html"] is None

    def get_item_class(self):
        if not self.has_no_content():
            return "ninat:text"
        elif self._count_associations() == 1:
            assoc = self.get("associations", [])[0]
            if "image" == assoc.get("type"):
                return f"ninat:picture"
            else:
                return f"ninat:{assoc.get('type')}"
        else:
            return "ninat:text"

    def is_text_message(self) -> bool:
        return self.get_item_class() == "ninat:text"

    def lang(self):
        return self.get("language", "de")

    def canceled(self):
        return self.get("pubstatus", "") == "canceled"


class KeySafeDict(dict):
    def __missing__(self, key):
        return None
