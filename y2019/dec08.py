#!/usr/bin/env python
# -*- coding: utf-8
import io

from colorama import init, Fore
from util import get_input_name


class Image(object):
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.layers = []
        layersize = x * y
        for layerdata in chunks(data, layersize):
            self.layers.append(Layer(x, y, layerdata))

    def render(self):
        rendered = Layer(self.x, self.y, "2"*self.x*self.y)
        for layer in self.layers:
            rendered.merge(layer)
        print(rendered)


class Layer(object):
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = list(data)

    def merge(self, other):
        for i, v in enumerate(self.data):
            if v == "2":
                self.data[i] = other.data[i]

    def __str__(self):
        out = io.StringIO()
        for line in chunks(self.data, self.x):
            for c in line:
                if c == "1":
                    out.write(Fore.WHITE + "#")
                elif c == "0":
                    out.write(Fore.BLACK + " ")
                else:
                    out.write(Fore.RED + "!")
            out.write("\n")
        return out.getvalue()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    with open(get_input_name("dec08")) as fobj:
        data = fobj.read().strip()
        image = Image(25, 6, data)
        best_count = len(data)
        best_layer = None
        for layer in image.layers:
            count = layer.data.count("0")
            if count < best_count:
                best_count = count
                best_layer = layer
        count1 = best_layer.data.count("1")
        count2 = best_layer.data.count("2")
        print("Best layer has {} 1 digits, and {} 2 digits, yielding a result of {}".format(count1, count2, count1*count2))
        image.render()


if __name__ == "__main__":
    init()
    main()
