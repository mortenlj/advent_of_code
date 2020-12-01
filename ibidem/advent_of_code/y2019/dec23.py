#!/usr/bin/env python
# -*- coding: utf-8

from queue import Empty, Queue
from threading import Thread, Lock

try:
    from .intcode import load_program, IntCode
except ModuleNotFoundError:
    from intcode import load_program, IntCode


IDLE_THRESHOLD = 10


class Nic(object):
    def __init__(self, id, inq, outq):
        self._id = id
        self._inq = inq
        self._outq = outq
        program = load_program("dec23")
        self._intcode = IntCode(program)
        self._thread = Thread(target=self._run, name="NIC-{}".format(id), daemon=True)
        self._outgoing_packet = []
        self._block = False
        self._idle_counter = 0

    def _input_init(self):
        self._input = self._input_packet
        return self._id

    def _input_packet(self):
        try:
            value = self._inq.get(self._block)
            self._block = False
            self._idle_counter = 0

            def packet(*args):
                self._input = self._input_packet
                return value[2]

            self._input = packet
            return value[1]
        except Empty:
            if self.idle:
                self._block = True
            self._idle_counter += 1
            return -1

    def _input(self):
        return self._input_init()

    def input(self):
        return self._input()

    def output(self, v):
        self._idle_counter = 0
        self._outgoing_packet.append(v)
        if len(self._outgoing_packet) == 3:
            self._outq.put(tuple(self._outgoing_packet))
            self._outgoing_packet = []

    def start(self):
        self._thread.start()

    def _run(self):
        self._intcode.execute(self.input, self.output)

    @property
    def idle(self):
        if self._idle_counter > IDLE_THRESHOLD:
            return True
        return False
    

class Nat(object):
    def __init__(self, inq, outq, idle_check):
        self._inq = inq
        self._outq = outq
        self._idle_check = idle_check
        self._thread = Thread(target=self._run, name="NAT", daemon=True)
        self.result = None
        self._last_packet = None
        self._last_y_sent = None

    def start(self):
        self._thread.start()

    def _run(self):
        while True:
            try:
                self._last_packet = self._inq.get_nowait()
                print("Last packet updated: {!r}".format(self._last_packet))
            except Empty:
                pass
            if self._idle_check() and self._last_packet:
                packet = (0, self._last_packet[1], self._last_packet[2])
                print("NAT is sending {}".format(packet))
                self._outq.put(packet)
                if self._last_y_sent == self._last_packet[2]:
                    self.result = self._last_y_sent
                    return
                self._last_y_sent = self._last_packet[2]


class Router(object):
    def __init__(self):
        self._outq = Queue()
        self._inq = {i: Queue() for i in range(50)}
        self._inq[255] = Queue()
        self._nics = [Nic(i, self._inq[i], self._outq) for i in range(50)]
        self._nat = Nat(self._inq[255], self._outq, self._idle_check)
        self._lock = Lock()

    def start(self):
        self._nat.start()
        for nic in self._nics:
            nic.start()
        while self._nat.result is None:
            packet = self._outq.get()
            with self._lock:
                dst = self._inq.get(packet[0])
                if dst is None:
                    print("Received invalid packet: {!r}".format(packet))
                    continue
                dst.put(packet)
        return self._nat.result

    def _idle_check(self):
        with self._lock:
            all_idle = all(nic.idle for nic in self._nics)
            if all_idle:
                print("All NICs are idle")
            return all_idle


def part2():
    router = Router()
    result = router.start()
    print("The first Y value delivered by the NAT to the computer at address 0 twice in a row: {}".format(result))


if __name__ == "__main__":
    part2()
