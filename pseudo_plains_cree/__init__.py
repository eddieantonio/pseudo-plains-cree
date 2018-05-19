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

import re
from pathlib import Path
from random import choice, randint
from typing import Dict, Sequence, TextIO, Optional



def first_char_uppercase(text: str) -> bool:
    return text[:1].upper() == text[:1]


def is_single_char_terminal(p: Production) -> bool:
    return isinstance(p, Terminal) and len(p.literal) == 1


def wrapped_in_parens(s: str) -> bool:
    return bool(re.match('^[(].+[)]$', s))


def re_uescape(text: str) -> str:
    """
    Like re.escape, except maintains non-ASCII characters.
    """
    return ''.join(
        re.escape(c) if c < '\u0080' else c
        for c in text
    )


VOWELS = tuple('aioâîôê')

with open(here / 'phonotactics.txt') as grammar_file:
    grammar = Parser().parse_file(grammar_file)


def generate(min_syllables=2, max_syllables=8) -> str:
    """
    Generate a pseudo-Plains Cree word.
    """
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
    needed = randint(min_words, max_words)
    sentence = ' '.join(generate() for _ in range(needed))
    return sentence.capitalize() + '.'


if __name__ == '__main__':
    import sys
    command = sys.argv[1] if len(sys.argv) > 1 else 'lorem'
    if command == 'lorem':
        print(lorem())
    elif command == 'word':
        print(generate())
    elif command == 'regex':
        print(grammar.to_regex())
    else:
        print("Invalid subcommand", file=sys.stderr)
        sys.exit(1)
