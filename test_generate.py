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
    assert any(is_vowel(c) for c in utterance)


@given(builds(generate))
def test_vowels(utterance):
    assert not any(is_vowel(g1) and is_vowel(g2)
                   for g1, g2 in bigrams(utterance))


def is_vowel(char: str) -> bool:
    if len(char) != 1:
        raise ValueError("expecting exactly one character; got " + repr(char))
    return char in VOWELS


def bigrams(text: str):
    return zip(text, text[1:])
