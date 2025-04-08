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
from .content_renderer import (
    render_article,
    render_teaser,
    render_date_time,
    render_closing_line,
)
from .header_renderer import render_header, render_subject
from .headline_renderer import (
    render_genre,
    render_prio,
    render_title,
    render_correction,
    render_embargo,
    render_byline,
    render_ednote_de,
)
from .notepad_renderer import (
    render_notepad_header,
    render_public_notepad,
    render_nonpublic_notepad,
)
