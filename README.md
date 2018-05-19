Pseudo Plains Cree
==================

Generates fake words using the orthographic rules of Plains Cree
(Nêhiyawêwin), written in Standard Roman Orthography (SRO).

The purpose is to generate data for testing tools that work with Plains
Cree orthography, or to create [Lorem ipsum][Lorem] text.

[Lorem]: https://en.wikipedia.org/wiki/Lorem_ipsum

Usage
-----

From the command line:

Generate a word:

```
$ python3 -m pseudo_plains_cree word
```

Generate a paragraph:

```
$ python3 -m pseudo_plains_cree lorem
```

Print the regular expression used to generate a syllable:

```
$ python3 -m pseudo_plains_cree regex
```


License
-------

Copyright © 2018 Eddie Antonio Santos. Licensed under the terms of the
GNU General Public License, version 3. See `License` for details.
