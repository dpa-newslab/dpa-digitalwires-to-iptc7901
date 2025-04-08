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
from .collection_utils import (
    get_none_safe,
    extend_if_not_empty,
    get_rank,
    find_first_in,
)
from .word_utils import article_html_to_text, notepad_md, TextHTML2Text
from .mappings import (
    prio_map,
    signal_map,
    service_mnemonic_map,
    service_to_iptc_agency_map,
    link_label,
    note_label,
    embargo_label,
)
from .symbols import BELL
from .objects import EdNote, Category
