import pytest

from ibidem.advent_of_code.y2020.dec24 import part1, parse_line, Direction

INPUT = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
eeeeeeeeeeeeeeeeeee
"""


class TestDec24:
    @pytest.fixture
    def tile_flips(self):
        return list(parse_line(line.strip()) for line in INPUT.splitlines(keepends=False))

    def test_parse_line(self):
        directions = list(parse_line("ewnenwsesw"))
        assert len(directions) == 6
        assert directions[0] == Direction.EAST

    def test_part1(self, tile_flips):
        actual = part1(tile_flips)
        assert actual == 11
