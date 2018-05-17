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

here = Path(__file__).parent


class Production:
    def generate(self) -> str:
        raise NotImplementedError

    def to_regex(self) -> str:
        raise NotImplementedError


class ProductionReference(Production):
    def __init__(self, grammar: 'Grammar', ref: str) -> None:
        self.ref = ref
        self.grammar = grammar

    def dereference(self) -> Production:
        return self.grammar[self.ref]

    def generate(self) -> str:
        return self.dereference().generate()

    def to_regex(self) -> str:
        return self.dereference().to_regex()


class Terminal(Production):
    def __init__(self, literal: str) -> None:
        self.literal = literal

    def generate(self) -> str:
        return self.literal

    def to_regex(self) -> str:
        return re_uescape(self.literal)


class Maybe(Production):
    def __init__(self, rule: Production) -> None:
        self.rule = rule

    def generate(self) -> str:
        if choice((True, False)):
            return self.rule.generate()
        return ''

    def to_regex(self) -> str:
        inner_re = self.rule.to_regex()

        # Output a simpler form if we can.
        if is_single_char_terminal(self.rule) or wrapped_in_parens(inner_re):
            return inner_re + '?'

        return f"({inner_re})?"


class Concatenation(Production):
    def __init__(self, components):
        self.components = components

    def generate(self) -> str:
        return ''.join(c.generate() for c in self.components)

    def to_regex(self) -> str:
        return ''.join(c.to_regex() for c in self.components)


class Alternation(Production):
    def __init__(self, alternatives):
        self.alternatives = alternatives

    def generate(self) -> str:
        return choice(self.alternatives).generate()

    def to_regex(self) -> str:
        # Return a character alternation if we can.
        if all(is_single_char_terminal(a) for a in self.alternatives):
            return '[' + ''.join(a.to_regex() for a in self.alternatives) + ']'
        return '(' + '|'.join(a.to_regex() for a in self.alternatives) + ')'


class Grammar:
    start_name: str

    def __init__(self) -> None:
        self.productions: Dict[str, Production] = {}

    def __getitem__(self, name: str) -> Production:
        return self.productions[name]

    def __setitem__(self, name: str, definition: Production) -> None:
        self.productions[name] = definition
        if not hasattr(self, 'start_name'):
            self.start_name = name

    @property
    def start(self) -> Production:
        return self[self.start_name]

    def generate(self) -> str:
        return self.start.generate()

    def to_regex(self) -> str:
        return self.start.to_regex()


class Parser:
    def parse_file(self, grammar_file: TextIO) -> Grammar:
        self.grammar = Grammar()
        for line in grammar_file:
            self.parse_production(line)
        return self.grammar

    def parse_production(self, line: str) -> None:
        if line.strip() == '':
            return
        # It's a production rule.
        name, definition = line.split(':=')
        name = name.strip()
        self.grammar[name] = self.parse_definition(definition)

    def parse_definition(self, definition: str) -> Production:
        alternatives = [self.parse_alternative(d.strip())
                        for d in definition.split('|')]

        if len(alternatives) > 1:
            return Alternation(alternatives)
        else:
            return alternatives[0]

    def parse_alternative(self, alternative: str):
        concatenation = [a.strip() for a in alternative.split()]
        # Don't need to create a concatenation if there is only one option!
        if len(concatenation) == 1:
            return self.parse_optional(concatenation[0])
        return Concatenation([self.parse_optional(o)
                              for o in concatenation])

    def parse_value(self, text: str) -> Production:
        if first_char_uppercase(text):
            return ProductionReference(self.grammar, text)
        else:
            return Terminal(text)

    def parse_optional(self, text: str) -> Production:
        if text.endswith('?'):
            return Maybe(self.parse_value(text[:-1]))
        else:
            return self.parse_value(text)


def first_char_uppercase(text: str) -> bool:
    return text[:1].upper() == text[:1]


def is_single_char_terminal(p: Production) -> bool:
    return isinstance(p, Terminal) and len(p.literal) == 1


def wrapped_in_parens(s: str) -> bool:
    return re.match('^[(].+[)]$', s)


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
    print(lorem())
