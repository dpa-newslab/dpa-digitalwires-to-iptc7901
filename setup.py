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

from setuptools import setup, find_packages

setup(
    name="digitalwirestoiptc7901",
    version="0.1",
    description='A Python library that transforms dpa-digitalwires to IPTC7901.',
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    install_requires=[
        "arrow==1.3.0",
        "html2text==2024.2.26",
        "markdownify==0.13.1",
        "six~=1.16.0",
        "beautifulsoup4~=4.12.3"
    ],
    author="Christoffer Kassens",
    author_email="kassens.christoffer@dpa.com",
    python_requires=">=3.12",
)
