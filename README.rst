
Advent of Code
==============

These are my solutions for `Advent of Code`_.


CLI
---

This repo also contains a minimal cli to generate files for problems ready for implementing.
In order to work, it needs a proper session to start with.
To get a session this cli can work with, follow these steps:

1. Log in on `Advent of Code`_ in your browser
2. Use developer tools or similar to get session cookie
3. Add session cookie to httpie session::

    # http --session session https://adventofcode.com/ "Cookie: session=<session-id>"

4. Run ``aoc``

.. _Advent of Code: https://adventofcode.com
