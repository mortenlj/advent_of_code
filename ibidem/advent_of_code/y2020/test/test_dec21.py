from ibidem.advent_of_code.y2020.dec21 import load_lines, part1, format_cdi

RECIPIES = [
    "mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
    "trh fvjkl sbzzf mxmxvkd (contains dairy)",
    "sqjhc fvjkl (contains soy)",
    "sqjhc mxmxvkd sbzzf (contains fish)",
]

RESULT_MAPPING = {
    "dairy": "mxmxvkd",
    "fish": "sqjhc",
    "soy": "fvjkl",
}


class TestDec21:
    def test_load_lines(self):
        all2ing, counts, ing2all, recipies = load_lines(RECIPIES)
        assert len(all2ing) == 3
        assert len(counts) == 7
        assert len(ing2all) == 7
        assert len(recipies) == 4

    def test_part1(self):
        ret = load_lines(RECIPIES)
        result, mapping = part1(*ret)
        assert result == 5
        assert mapping == RESULT_MAPPING

    def test_format_cdi(self):
        actual = format_cdi(RESULT_MAPPING)
        assert actual == "mxmxvkd,sqjhc,fvjkl"
