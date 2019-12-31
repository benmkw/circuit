class wire:
    def __init__(self):
        self.signal = None
        self.actions = []

    def set_signal(self, value):
        if self.signal != value:
            self.signal = value
            for action in self.actions:
                action()

    def get_signal(self):
        return self.signal

    def add_action(self, action):
        self.actions.append(action)


def or_gate(a1, a2, output):
    def or_fn():
        new_val = a1.get_signal() or a2.get_signal()
        output.set_signal(new_val)

    a1.add_action(or_fn)
    a2.add_action(or_fn)


def and_gate(a1, a2, output):
    def and_fn():
        new_val = a1.get_signal() and a2.get_signal()
        output.set_signal(new_val)

    a1.add_action(and_fn)
    a2.add_action(and_fn)


def inverter(input, output):
    def invert_input():
        new_val = not input.get_signal()
        output.set_signal(new_val)

    input.add_action(invert_input)


def probe(wire, name):
    def probe_fn():
        print("probe name:", name)
        print("new value: ", wire.get_signal())
        print()
    wire.add_action(probe_fn)


def half_adder(a, b, s, c):
    d = wire()
    e = wire()
    or_gate(a, b, d)
    and_gate(a, b, c)
    inverter(c, e)
    and_gate(d, e, s)


def full_adder(a, b, c_in, sum_, c_out):
    s = wire()
    c1 = wire()
    c2 = wire()
    half_adder(b, c_in, s, c1)
    half_adder(a, s, sum_, c2)
    or_gate(c1, c2, c_out)


a = wire()
b = wire()
c_in = wire()
sum_ = wire()
c_out = wire()

probe(a, "a")
probe(b, "b")
probe(c_in, "c_in")
probe(sum_, "sum_")
probe(c_out, "c_out")

my_half_adder = full_adder(a, b, c_in, sum_, c_out)

a.set_signal(True)
b.set_signal(False)
c_in.set_signal(True)
