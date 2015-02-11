# -*- coding: utf-8 -*-
"""MSC104: Chatspeak.

---
layout:     post
error_code: MSC
source:     ???
source_url: ???
title:      textese
date:       2014-06-10 12:31:19
categories: writing
---

Chatspeak.

"""
from proselint.tools import blacklist, memoize


@memoize
def check(text):

    err = "MSC104"
    msg = u"'{}' is chatspeak. Write it out."

    words = [
        "2day",
        "4U",
        "AFAIK",
        "AFK",
        "AFK",
        "ASAP",
        "B4",
        "brb",
        "btw",
        "cya",
        "GR8",
        "lol",
        "LOL",
        "LUV",
        "OMG",
        "rofl",
        "roftl",
        "sum1",
        "SWAK",
        "THNX",
        "THX",
        "TTYL",
        "XOXO"
    ]

    return blacklist(text, words, err, msg)