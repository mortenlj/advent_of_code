#!/usr/bin/env python
from collections import namedtuple, defaultdict

from ibidem.advent_of_code.util import get_input_name

Recipie = namedtuple("Recipie", ["ingredients", "allergens"])


def load():
    with open(get_input_name(21, 2020)) as fobj:
        lines = fobj.readlines()
        all2ing, counts, ing2all, recipies = load_lines(lines)
    return all2ing, counts, ing2all, recipies


def load_lines(lines):
    recipies = []
    counts = defaultdict(int)
    ing2all = defaultdict(set)
    all2ing = defaultdict(set)
    for line in lines:
        ingredients, rest = line.strip().split("(")
        allergens = rest[len("contains"):-1]
        recipie = Recipie(set(ingredients.split()), set(allergens.replace(",", "").split()))
        for ing in recipie.ingredients:
            counts[ing] += 1
            ing2all[ing].update(recipie.allergens)
        for all in recipie.allergens:
            all2ing[all].update(recipie.ingredients)
        recipies.append(recipie)
    return all2ing, counts, ing2all, recipies


def part1(all2ing, counts, ing2all, recipies):
    mapping = {}
    while len(mapping) < len(all2ing):
        for allergen, candidates in all2ing.items():
            for recipie in recipies:
                if allergen in recipie.allergens:
                    candidates.intersection_update(recipie.ingredients)
            if len(candidates) == 1:
                ingredient = candidates.pop()
                mapping[allergen] = ingredient
                for a in ing2all[ingredient]:
                    if ingredient in all2ing[a]:
                        all2ing[a].remove(ingredient)
    ingredients = set(ing2all.keys())
    for ing in mapping.values():
        ingredients.remove(ing)
    result = sum(counts[i] for i in ingredients)
    print(f"The sum of ingredient counts is {result}")
    return result, mapping


def format_cdi(mapping):
    allergens = sorted(mapping.keys())
    ingredients = (mapping[a] for a in allergens)
    return ",".join(ingredients)


def part2(mapping):
    cdi = format_cdi(mapping)
    print(f"The canonical dangerous ingredient list is '{cdi}'")


if __name__ == "__main__":
    ret = load()
    _, mapping = part1(*ret)
    part2(mapping)
