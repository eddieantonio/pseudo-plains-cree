#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from hypothesis import given
from hypothesis.strategies import builds

from generate import generate

VOWELS = 'aioâîôê'


@given(builds(generate))
def test_basic_usage(utterance):
    """
    A produced utterance has at least one vowel in it.
    """
    assert any(v in utterance for v in VOWELS)
