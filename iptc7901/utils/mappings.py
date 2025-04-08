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

signal_map = {
    "sig:correction": {
        "de": "Berichtigung",
        "ru": "коррекция",
        "pl": "Korekta",
        "fr": "Correction",
        "en": "Correction",
        "es": "VERSIÓN CORREGIDA",
        "ar": "تصحيح",
    },
    "sig:repeat": {
        "de": "Wiederholung",
        "ru": "повтор",
        "pl": "Powtarzanie",
        "fr": "Remettre",
        "en": "Refile",
        "es": "RPT RPT",
        "ar": "إعادة",
    },
    "sig:update": {
        "de": "Aktualisierung",
        "ru": "Обновить",
        "pl": "Aktualizacja",
        "fr": "Mettre à jour",
        "en": "Update",
        "es": "ACTUALIZACIÓN",
        "ar": "تحديث",
    },
}

prio_map = {
    1: {
        "de": "Blitz ",
        "es": "FLASH ",
        "en": "FLASH: ",
        "fr": "FLASH: ",
        "ru": "МОЛНИЯ: ",
        "pl": "FLASH: ",
        "ar": "عاجل جدا: ",
    },
    2: {
        "de": "Eil ",
        "es": "URGENTE ",
        "en": "URGENT: ",
        "fr": "D'URGENCE: ",
        "ru": "СРОЧНО: ",
        "pl": "PILNE: ",
        "ar": "عاجل: ",
    },
}

note_label = {
    "de": "Redaktionelle Hinweise",
    "es": "AVISO AL EDITOR",
    "ru": "Примечание для редакторов",
    "pl": "Uwaga dla redaktorów",
    "fr": "Publié",
    "en": "Note to editors",
    "ar": "تنويه للمحررين",
}

embargo_label = {
    "ru": "Эмбарго для публикации до",
    "pl": "EMBARGOED do publikacji do",
    "fr": "Être soumis(e) à un embargo pour publication jusqu'à",
    "en": "EMBARGOED for publication until",
    "ar": "حظر للنشر حتى",
}

link_label = {
    "ru": "Интернет-ссылки",
    "pl": "Łącza internetowe",
    "fr": "Liens internet",
    "de": "Internet",
    "en": "Internet links",
    "es": "INTERNET",
    "ar": "روابط إنترنت",
}

service_mnemonic_map = {
    "eca-3p": "ecp",
    "bobs": "obs",
    "bmag": "mag",
    "barch": "report",
    "bepai": "epa-i",
    "bdpai": "dpa-i",
    "blatam": "latam",
    "bweblines": "weblines",
    "anstueck": "n-stueck",
    "aoton": "o-ton",
    "ao-ton": "O-Ton",
    "aumfrage": "Umfrage",
    "atalk": "talk retired",
    "atalk_interview": "talk_interview",
    "ainterview": "Interview",
    "akorri-talk": "Korri-Talk",
    "abunt": "bunt",
    "anachrichten_lang": "nachrichten_lang",
    "anachrichten_kurz": "nachrichten_kurz",
    "akinder": "audiokinder",
    "aors": "ors",
    "audio": "dpaaudio",
    "awetter": "wetter",
    "awetter_regional": "wetter_regional",
    "awirtschaft": "Wirtschaft",
    "awirtschaft-bigfm": "Wirtschaft-BigFM",
    "awirtschaft-bawue": "Wirtschaft-BaWue",
    "aatmo": "Atmo",
    "aradio24": "radio24",
    "azaudiohub-oton": "zAudiohub-Oton",
    "azaudiohub-atmo": "zAudiohub-Atmo",
    "azaudiohub-interview": "zAudiohub-Interview",
    "azaudiohub-umfrage": "zAudiohub-Umfrage",
    "video": "dpavideo",
    "regiolinebayern": "bayern",
    "regiolinebwg": "badenwuerttemberg",
    "regiolinebrb": "berlinbrandenburg",
    "regiolinehsh": "hamburgschleswigholstein",
    "regiolinehes": "hessen",
    "regiolinembv": "mecklenburgvorpommern",
    "regiolinensb": "niedersachsen",
    "regiolinenwf": "nordrheinwestfalen",
    "regiolinerhs": "rheinlandpfalzsaarland",
    "regiolinesan": "sachsen",
    "regiolineaht": "sachsenanhalt",
    "regiolinethg": "thueringen",
    "wap-aht": "wap",
    "wap-san": "wap",
    "wap-rhs": "wap",
    "wap-hsh": "wap",
    "wap-nsb": "wap",
    "wap-hes": "wap",
    "wap-brb": "wap",
    "wap-mbv": "wap",
    "wap-thg": "wap",
    "wap-bwg": "wap",
    "wap-nwf": "wap",
    "wap-bay": "wap",
    "feat-en": "feature-en",
    "insight-eu": "ieu",
    "insight-eu-de": "ieu",
    "insight-eu-en": "ien",
    "dpa-news": "news",
    "dpa-agenda": "agenda",
    "dpa-feedback": "feedback",
    "text-arabisch-abi": "صاب",
    "text-arabisch-acc": "صيي",
    "text-arabisch-dara": "س",
    "text-arabisch-are": "صدط",
    "bfotografia": "fotografia",
    "photostream-es": "photostream-en",
    "europapres-tem": "europapress-tem",
    "dpa-espanol": "dpe",
    "graphics-ndk": "ndk",
    "graphics-dpa": "dpa",
    "graphics-glo": "glo",
    "graphics-glw": "glw",
    "graphics-stp": "stp",
    "graphics-biz": "biz",
    "graphics-krs": "krs",
    "graphics-dpa-e": "dpa-e",
    "graphics-bay": "bay",
    "graphics-bwg": "bwg",
    "graphics-hrs": "hrs",
    "graphics-nor": "nor",
    "graphics-nrw": "nrw",
    "graphics-tmn": "tmn",
    "graphics-geo": "geo",
    "graphics-ser": "ser",
    "graphics-sch": "sch",
    "erd-ch-photo": "photostream-de-erd-ch",
    "easynews-photo": "easynews",
    "ann-news": "ann",
}

service_to_iptc_agency_map = {
    "bdt": "dpa",
    "spe": "dpa-spe",
    "eca": "dpa",
    "eca-3p": "dpa-tns",
    "ldi": "dpa",
    "erd": "dpa-euro",
    "ndk": "dpa-knd",
    "bid": "dpa",
    "hfk": "dpa-kurz",
    "kom": "dpa",
    "mag": "azin",
    "tmn": "dpa-tmn",
    "biog": "dpa-biog",
    "mbv": "lmv",
    "bwg": "lsw",
    "hes": "lhe",
    "bay": "lby",
    "brb": "lbn",
    "nsb": "lni",
    "nwf": "lnw",
    "hsh": "lno",
    "rhs": "lrs",
    "san": "lsn",
    "aht": "lah",
    "thg": "lth",
    "wap-aht": "lah",
    "wap-san": "lsn",
    "wap-rhs": "lrs",
    "wap-hsh": "lno",
    "wap-nsb": "lni",
    "wap-hes": "lhe",
    "wap-brb": "lbn",
    "wap-mbv": "lmv",
    "wap-thg": "lth",
    "wap-bwg": "lsw",
    "wap-nwf": "lnw",
    "wap-bay": "lby",
    "edi": "dpa-euro-term",
    "edt": "dpa-euro-term",
    "apx": "ap",
    "insight-eu": "dpa",
    "insight-eu-de": "dpa",
    "insight-eu-en": "dpa",
    "dpa-feedback": "intern",
    "text-arabisch-abi": "dpa-text-arabisch-abi",
    "text-arabisch-acc": "dpa-text-arabisch-acc",
    "text-arabisch-dara": "dpa-text-arabisch-dara",
    "text-arabisch-are": "dpa-text-arabisch-are",
    "kon": "dpa",
    "ctn": "dpa",
    "dpa-espanol": "dpa",
    "ann-news": "ann",
}
