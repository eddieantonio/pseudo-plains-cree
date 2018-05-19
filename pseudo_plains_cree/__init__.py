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


"""
Generates pseudo-Plains Cree words, in Standard Roman Orthography (SRO).
"""

from pathlib import Path
from random import randint

from ._grammar import Parser


here = Path(__file__).parent
with open(here / 'phonotactics.txt') as grammar_file:
    grammar = Parser().parse_file(grammar_file)


def generate(min_syllables=2, max_syllables=8) -> str:
    """
    Generate a pseudo-Plains Cree word.
    """
    VOWELS = tuple('aioâîôê')

    needed = randint(min_syllables, max_syllables)
    # Generate AT LEAST one syllable.
    utterance = grammar.generate()

    generated = 1
    while generated < needed:
        syllable = grammar.generate()
        if utterance.endswith(VOWELS) and syllable.startswith(VOWELS):
            continue
        if syllable.startswith(utterance[-1]):
            continue
        utterance += syllable
        generated += 1

    return utterance


def lorem(min_words=40, max_words=400) -> str:
    """
    Generate ipsum text out of pseudo words.
    """
    needed = randint(min_words, max_words)
    sentence = ' '.join(generate() for _ in range(needed))
    return sentence.capitalize() + '.'
