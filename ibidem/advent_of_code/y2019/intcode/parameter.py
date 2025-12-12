#!/usr/bin/env python
# -*- coding: utf-8


class Parameter(object):
    mode = None
    _parameters = None

    def __init__(self, value, machine):
        self._value = value
        self._memory = machine.memory

    def get(self):
        raise NotImplementedError("Must be implemented")

    def set(self, value):
        raise NotImplementedError("Must be implemented")

    def __repr__(self):
        return "{}(value={}, evaled={})".format(
            self.__class__.__name__, self._value, self.get()
        )

    @classmethod
    def from_mode(cls, mode):
        if cls._parameters is None:
            cls._parameters = {
                p.mode: p for p in cls.__subclasses__() if p.mode is not None
            }
        if mode not in cls._parameters:
            raise ValueError("Invalid mode {} for Parameter".format(mode))
        return cls._parameters[mode]


class Position(Parameter):
    mode = 0

    def __init__(self, value, machine):
        if value < 0:
            raise ValueError("Invalid position {} for Position parameter".format(value))
        super().__init__(value, machine)

    def get(self):
        return self._memory[self._value]

    def set(self, value):
        self._memory[self._value] = value


class Immediate(Parameter):
    mode = 1

    def get(self):
        return self._value

    def set(self, value):
        raise TypeError("Immediate parameter doesn't support set operation")


class Relative(Parameter):
    mode = 2

    def __init__(self, value, machine):
        super().__init__(value, machine)
        self._machine = machine

    def get(self):
        return self._memory[self._machine.rb + self._value]

    def set(self, value):
        self._memory[self._machine.rb + self._value] = value
