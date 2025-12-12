import io
import textwrap
from collections import namedtuple
from typing import Mapping, Sequence

import pytest

from ibidem.advent_of_code.y2024.dec24 import load, part1, part2

Case = namedtuple("Case", "part1 part2 input")

TEST_INPUTS = [
    Case(
        4,
        NotImplemented,
        io.StringIO(
            textwrap.dedent("""\
        x00: 1
        x01: 1
        x02: 1
        y00: 0
        y01: 1
        y02: 0
        
        x00 AND y00 -> z00
        x01 XOR y01 -> z01
        x02 OR y02 -> z02
    """)
        ),
    ),
    Case(
        2024,
        NotImplemented,
        io.StringIO(
            textwrap.dedent("""\
        x00: 1
        x01: 0
        x02: 1
        x03: 1
        x04: 0
        y00: 1
        y01: 1
        y02: 1
        y03: 1
        y04: 1
        
        ntg XOR fgs -> mjb
        y02 OR x01 -> tnw
        kwq OR kpj -> z05
        x00 OR x03 -> fst
        tgd XOR rvg -> z01
        vdt OR tnw -> bfw
        bfw AND frj -> z10
        ffh OR nrd -> bqk
        y00 AND y03 -> djm
        y03 OR y00 -> psh
        bqk OR frj -> z08
        tnw OR fst -> frj
        gnj AND tgd -> z11
        bfw XOR mjb -> z00
        x03 OR x00 -> vdt
        gnj AND wpb -> z02
        x04 AND y00 -> kjc
        djm OR pbm -> qhw
        nrd AND vdt -> hwm
        kjc AND fst -> rvg
        y04 OR y02 -> fgs
        y01 AND x02 -> pbm
        ntg OR kjc -> kwq
        psh XOR fgs -> tgd
        qhw XOR tgd -> z09
        pbm OR djm -> kpj
        x03 XOR y03 -> ffh
        x00 XOR y04 -> ntg
        bfw OR bqk -> z06
        nrd XOR fgs -> wpb
        frj XOR qhw -> z04
        bqk OR frj -> z07
        y03 OR x01 -> nrd
        hwm AND bqk -> z03
        tgd XOR rvg -> z12
        tnw OR pbm -> gnj
    """)
        ),
    ),
]


class TestDec24:
    @pytest.fixture(params=TEST_INPUTS)
    def case(self, request):
        request.param.input.seek(0)
        return request.param

    @pytest.fixture
    def loaded(self, case):
        return load(case.input)

    def test_load(self, loaded):
        initial, gates = loaded
        assert isinstance(initial, Mapping)
        assert isinstance(gates, Sequence)

    def test_part1(self, loaded, case):
        result = part1(loaded)
        assert result == case.part1

    @pytest.mark.skip("Not interested right now")
    def test_part2(self, loaded, case):
        result = part2(loaded)
        assert result == case.part2
