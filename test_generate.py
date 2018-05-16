#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from generate import generate

VOWELS = 'aioâîôê'


def test_basic_usage():
    """
    A produced utterance has at least one vowel in it.
    """
    utterance = generate()
    assert any(v in utterance for v in VOWELS)
