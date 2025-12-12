#!/usr/bin/env python
import collections
from datetime import datetime
from enum import Enum
from typing import Iterable

from ibidem.advent_of_code.util import get_input_name


class Pulse(Enum):
    HIGH = 1
    LOW = 0

    def __str__(self):
        return "-high->" if self == Pulse.HIGH else "-low->"


class Module:
    def __init__(self, name, outputs, output_deque: collections.deque):
        self.name = name
        self.outputs = outputs
        self.output_deque = output_deque

    def pulse(self, input_pulse: Pulse, sender):
        for output_name, output_pulse in self._process(input_pulse, sender):
            self.output_deque.append((output_name, output_pulse, self.name))

    def _process(self, input_pulse, sender) -> Iterable[tuple[str, Pulse]]:
        raise NotImplementedError("")


class Output(Module):
    def __init__(self, name):
        super().__init__(name, [], None)
        self.last_pulse = None

    def _process(self, input_pulse, sender) -> Iterable[tuple[str, Pulse]]:
        # print(f"{self.name} recieved {input_pulse!r} from {sender}")
        self.last_pulse = input_pulse
        return []


class Broadcaster(Module):
    def __init__(self, outputs, output_deque: collections.deque):
        super().__init__("broadcaster", outputs, output_deque)

    def _process(self, input_pulse, sender) -> Iterable[tuple[str, Pulse]]:
        return [(on, input_pulse) for on in self.outputs]


class FlipFlop(Module):
    class State(Enum):
        ON = True
        OFF = False

    def __init__(self, name, outputs, output_deque: collections.deque):
        super().__init__(name, outputs, output_deque)
        self._state = FlipFlop.State.OFF

    def _process(self, input_pulse, sender) -> Iterable[tuple[str, Pulse]]:
        if input_pulse == Pulse.HIGH:
            return []
        if self._state == FlipFlop.State.OFF:
            pulse = Pulse.HIGH
            self._state = FlipFlop.State.ON
        else:
            pulse = Pulse.LOW
            self._state = FlipFlop.State.OFF
        return [(on, pulse) for on in self.outputs]


class Conjunction(Module):
    def __init__(self, name, outputs, output_deque: collections.deque):
        super().__init__(name, outputs, output_deque)
        self._input_map = {}

    def set_inputs(self, inputs):
        self._input_map = {input_name: Pulse.LOW for input_name in inputs}

    def _process(self, input_pulse, sender) -> Iterable[tuple[str, Pulse]]:
        self._input_map[sender] = input_pulse
        pulse = (
            Pulse.LOW
            if all(v == Pulse.HIGH for v in self._input_map.values())
            else Pulse.HIGH
        )
        return [(on, pulse) for on in self.outputs]


def load(fobj):
    conjunctions = []
    deque = collections.deque()
    modules = {}
    for line in fobj:
        line = line.strip()
        module_name, outputstr = line.split("->")
        module_name = module_name.strip()
        outputs = [s.strip() for s in outputstr.split(",")]
        if module_name[0] == "%":
            module = FlipFlop(module_name[1:].strip(), outputs, deque)
        elif module_name[0] == "&":
            module = Conjunction(module_name[1:].strip(), outputs, deque)
            conjunctions.append(module)
        elif module_name == "broadcaster":
            module = Broadcaster(outputs, deque)
        else:
            raise ValueError(f"Incorrectly parsed module name: {module_name!r}")
        modules[module.name] = module
    for conjunction in conjunctions:
        inputs = []
        for module in modules.values():
            if conjunction.name in module.outputs:
                inputs.append(module.name)
        conjunction.set_inputs(inputs)
    outputs = []
    for module in modules.values():
        for output_name in module.outputs:
            if output_name not in modules:
                outputs.append(Output(output_name))
    for output in outputs:
        modules[output.name] = output
    return deque, modules


def part1(input):
    print("Starting part 1")
    deque, modules = input
    pulse_counter = collections.Counter()
    for i in range(1000):
        deque.append(("broadcaster", Pulse.LOW, "button"))
        while deque:
            target, pulse, source = deque.popleft()
            print(f"{source} {pulse} {target}")
            modules[target].pulse(pulse, source)
            pulse_counter[pulse] += 1
        print(f"Completed {i + 1} button presses")
    return pulse_counter[Pulse.LOW] * pulse_counter[Pulse.HIGH]


def part2(input):
    print("Starting part 2")
    deque, modules = input
    rx = modules["rx"]
    i = 0
    while rx.last_pulse != Pulse.LOW:
        deque.append(("broadcaster", Pulse.LOW, "button"))
        while deque:
            target, pulse, source = deque.popleft()
            # print(f"{source} {pulse} {target}")
            modules[target].pulse(pulse, source)
        if i % 1000000 == 0:
            now = datetime.now()
            print(f"[{now.isoformat()}] Completed {i + 1} button presses")
        i += 1
    return i


if __name__ == "__main__":
    with open(get_input_name(20, 2023)) as fobj:
        p1_result = part1(load(fobj))
        print(f"Part 1: {p1_result}")
    with open(get_input_name(20, 2023)) as fobj:
        p2_result = part2(load(fobj))
        print(f"Part 2: {p2_result}")
