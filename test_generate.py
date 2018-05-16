#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (C) 2018  Eddie Antonio Santos <easantos@ualberta.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
