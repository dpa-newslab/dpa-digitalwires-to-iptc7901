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

class Context:
    def __init__(self, digitalwire):
        self.digitalwire = digitalwire
        self.has_no_content = digitalwire.get("article_html", None) is None
        self.lang = digitalwire.get("language")
        self.canceled = digitalwire.get("pubstatus", "") == "canceled"
        self.ns = {
            "xmlns": "http://iptc.org/std/nar/2006-10-01/",
            "xml": "http://www.w3.org/XML/1998/namespace",
        }
