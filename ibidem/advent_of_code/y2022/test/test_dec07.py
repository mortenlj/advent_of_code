import io

import pytest

from ibidem.advent_of_code.y2022.dec07 import load, part1, part2

TEST_INPUT = io.StringIO("""\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""")

PART1_RESULT = 95437
PART2_RESULT = 24933642


class TestDec07():
    @pytest.fixture
    def input(self):
        TEST_INPUT.seek(0)
        return TEST_INPUT

    @pytest.fixture
    def loaded(self, input):
        return load(input)

    def test_load(self, loaded):
        assert loaded.cwd.name == "/"
        root = loaded.cwd
        loaded.cd("a").cd("e")
        e = loaded.cwd
        assert len(loaded.cwd.children) == 1
        assert loaded.cwd.children[0].name == "i"
        assert loaded.cwd.children[0].size == 584
        assert loaded.cwd.size == 584
        loaded.cd("..")
        a = loaded.cwd
        assert len(loaded.cwd.children) == 4
        assert loaded.cwd.name == "a"
        assert loaded.cwd.size == 94853
        assert root.size == 48381165
        assert len(root.children) == 4

        assert len(a.children) == 4
        assert len(e.children) == 1

    def test_part1(self, loaded):
        result = part1(loaded)
        assert result == PART1_RESULT

    def test_part2(self, loaded):
        result = part2(loaded)
        assert result == PART2_RESULT
