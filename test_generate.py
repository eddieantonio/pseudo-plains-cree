#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from hypothesis import given  # type: ignore
from hypothesis.strategies import random_module, composite  # type: ignore

from generate import generate

VOWELS = 'aioâîôê'


@composite
def utterances(draw):
    random = draw(random_module())
    return generate()


@given(utterances())
def test_basic_usage(utterance):
    """
    A produced utterance has at least one vowel in it.
    """
    assert any(is_vowel(c) for c in utterance)


@given(utterances())
def test_vowels(utterance):
    assert not any(is_vowel(g1) and is_vowel(g2)
                   for g1, g2 in bigrams(utterance))


@given(utterances())
def test_doubled_grams(utterance):
    assert all(g1 != g2 for g1, g2 in bigrams(utterance))


def is_vowel(char: str) -> bool:
    if len(char) != 1:
        raise ValueError("expecting exactly one character; got " + repr(char))
    return char in VOWELS


def bigrams(text: str):
    return zip(text, text[1:])
