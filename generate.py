#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Generates pseudo-Plains Cree words, in Standard Roman Orthography (SRO)
"""

from pathlib import Path
from random import choice, randint
from typing import Dict, Sequence

here = Path(__file__).parent


class Production:
    def generate(self) -> str:
        ...


productions: Dict[str, Production] = {}


class ProductionReference(Production):
    def __init__(self, ref: str) -> None:
        self.ref = ref

    def generate(self) -> str:
        return productions[self.ref].generate()


class Terminal(Production):
    def __init__(self, alternatives):
        self.alternatives = list(alternatives)

    def generate(self) -> str:
        return choice(self.alternatives)


class Optional(Production):
    def __init__(self, rule: Production) -> None:
        self.rule = rule

    def generate(self) -> str:
        if choice((True, False)):
            return self.rule.generate()
        return ''


class Concatenation(Production):
    def __init__(self, components):
        self.components = components

    def generate(self) -> str:
        return ''.join(c.generate() for c in self.components)


class Alternation(Production):
    def __init__(self, alternatives):
        self.alternatives = alternatives

    def generate(self) -> str:
        return choice(self.alternatives).generate()


def parse_definition(definition: str) -> Production:
    alternatives = [parse_alternative(d.strip())
                    for d in definition.split('|')]

    if len(alternatives) > 1:
        return Alternation(alternatives)
    else:
        return alternatives[0]


def parse_alternative(alternative: str):
    concatenation = alternative.split()
    return Concatenation([parse_optional(o.strip()) for o in concatenation])


def parse_value(text: str) -> Production:
    if first_char_uppercase(text):
        return ProductionReference(text)
    else:
        return Terminal(text)


def parse_optional(text: str):
    if text.endswith('?'):
        return Optional(parse_value(text[:-1]))
    else:
        return parse_value(text)


def first_char_uppercase(text: str) -> bool:
    return text[:1].upper() == text[:1]


def generate(min_syllables=2, max_syllables=8) -> str:
    with open(here / 'phonotactics.txt') as grammar_file:
        for line in grammar_file:
            if line.strip() == '':
                continue
            # It's a production rule.
            name, definition = line.split(':=')
            name = name.strip()
            productions[name] = parse_definition(definition)

    start = productions['Syllable']
    return ''.join((start.generate() for _ in
                    range(randint(min_syllables, max_syllables))))


if __name__ == '__main__':
    print(generate())
