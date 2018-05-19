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

import sys
from pseudo_plains_cree import grammar, lorem, generate


def main(_program_name: str, command: str='lorem', *_) -> None:
    if command == 'lorem':
        print(lorem())
    elif command == 'word':
        print(generate())
    elif command == 'regex':
        print(grammar.to_regex())
    else:
        print("Invalid subcommand", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main(*sys.argv)
