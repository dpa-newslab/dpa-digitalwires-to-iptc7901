#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (c) 2025  dpa-IT Services GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Category:
    category_type: str = None
    role: str = None
    name: str = None
    qcode: str = None
    rank: int = None

    @staticmethod
    def map_dw_key(dw_key: str | list[str]) -> str | list[str]:
        def replace_key(key: str) -> str:
            if key == "type":
                return "category_type"
            else:
                return key

        if type(dw_key) is not list:
            dw_key = [dw_key]
        dw_key = [replace_key(to_replace) for to_replace in dw_key]
        return dw_key


@dataclass(eq=True, frozen=True)
class EdNote:
    role: str = None
    ednote: str = None
    is_publishable: bool = None
