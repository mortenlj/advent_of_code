from ibidem.advent_of_code.y2020.dec08 import *

TEST_PROGRAM = [
    "nop +0",
    "acc +1",
    "jmp +4",
    "acc +3",
    "jmp -3",
    "acc -99",
    "acc +1",
    "jmp -4",
    "acc +6",
]


class TestDec08():
    def test_load_program(self):
        handheld = Handheld(["acc +5", "nop +0", "jmp -1"])
        assert handheld.program == [Instruction("acc", 5), Instruction("nop", 0), Instruction("jmp", -1)]

    def test_execute(self):
        handheld = Handheld(TEST_PROGRAM)
        handheld.execute()
        assert handheld.ip == 1
        assert handheld.acc == 5
