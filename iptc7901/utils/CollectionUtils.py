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

from typing import Iterable, Callable


def extend_if_not_empty(list_to_add, add_list):
    if add_list and len(add_list) > 0:
        for element in add_list:
            if element and len(element) > 0:
                list_to_add.append(element)


def get_none_safe(col, field, default):
    result = col.get(field, default)
    return result if result is not None else default


def find_first_in(
    parent: Iterable[dict],
    extract_tag: str,
    condition: Callable[[dict[str, str]], bool],
) -> str:
    """
    Returns the value of the first element in a collection given by ``extract_tag``.
    :param parent: A list of dictionaries to extract from.
    :param extract_tag: The key for the dictionary to extract from.
    :param condition: The condition to filter the list ``parent``.
    :return: The first element of the filtered list ``parent``.
    """
    return next(
        iter(
            [
                categorie.get(extract_tag, "")
                for categorie in parent
                if condition(categorie)
            ]
        ),
        "",
    )
