# connector gets a value by a constraint or by the user
# -> connector awakens all its constraints except the one that woke it

# each awakened constraint tries to complete, check if all needed values are given


class connector:
    def __init__(self):
        self.value = None
        self.informant = None
        self.constraints = []

    def has_value(self):
        return self.value is not None

    def get_value(self):
        return self.value

    def set_value(self, new_value, setter):
        if not self.has_value():
            self.value = new_value
            self.informant = setter
            for constraint in self.constraints:
                if constraint == setter:
                    continue
                else:
                    constraint.process_new_value()
        elif not self.value == new_value:
            print("Contradiction", self.value, new_value)
        else:
            print("ignored", self.value, new_value)

    def forget_value(self, retractor):
        if self.informant == retractor:
            self.informant = None
            self.value = None
            for constraint in self.constraints:
                if constraint == retractor:
                    continue
                else:
                    constraint.process_forget_value()

    def connect(self, new_constraint):
        if new_constraint not in self.constraints:
            self.constraints.append(new_constraint)

        if self.has_value():
            new_constraint.process_new_value()


class probe:
    def __init__(self, name, connector):
        self.name = name
        self.connector = connector

        connector.connect(self)

    def print_probe(self, value):
        print(self.name, value)

    def process_new_value(self):
        self.print_probe(self.connector.get_value())

    def process_forget_value(self):
        self.print_probe("?")


class adder:
    def __init__(self, a1, a2, sum_):
        self.a1 = a1
        self.a2 = a2
        self.sum_ = sum_

        a1.connect(self)
        a2.connect(self)
        sum_.connect(self)

    def process_new_value(self):
        if self.a1.has_value() and self.a2.has_value():
            self.sum_.set_value(self.a1.get_value() +
                                self.a2.get_value(), self)
        elif self.a1.has_value() and self.sum_.has_value():
            self.a2.set_value(self.sum_.get_value() -
                              self.a1.get_value(), self)
        elif self.a2.has_value() and self.sum_.has_value():
            self.a1.set_value(self.sum_.get_value() -
                              self.a2.get_value(), self)

    def process_forget_value(self):
        self.a1.forget_value(self)
        self.a2.forget_value(self)
        self.sum_.forget_value(self)

        self.process_new_value()


class multiplier:
    def __init__(self, a1, a2, product):
        self.a1 = a1
        self.a2 = a2
        self.product = product

        a1.connect(self)
        a2.connect(self)
        product.connect(self)

    def process_new_value(self):
        if self.a1.get_value() is 0 or self.a2.get_value() is 0:
            self.product.set_value(0, self)
        elif self.a1.has_value() and self.a2.has_value():
            self.product.set_value(
                self.a1.get_value() * self.a2.get_value(), self)
        elif self.a1.has_value() and self.product.has_value():
            self.a2.set_value(self.product.get_value() /
                              self.a1.get_value(), self)
        elif self.a2.has_value() and self.product.has_value():
            self.a1.set_value(self.product.get_value() /
                              self.a2.get_value(), self)

    def process_forget_value(self):
        self.a1.forget_value(self)
        self.a2.forget_value(self)
        self.product.forget_value(self)

        self.process_new_value()


class constant:
    def __init__(self, val, variable):
        self.val = val
        self.variable = variable

        variable.connect(self)
        self.variable.set_value(self.val, self)

    def process_new_value(self):
        assert(False)
        # self.variable.set_value(self.val, self)

    def process_forget_value(self):
        assert(False)


def celsius_fahrenheit_converter(C, F):
    u = connector()
    v = connector()
    w = connector()
    x = connector()
    y = connector()

    multiplier(C, w, u)
    multiplier(v, x, u)
    adder(v, y, F)
    constant(9, w)
    constant(5, x)
    constant(32, y)


A = connector()
B = connector()
C = connector()
probe("a", A)
probe("b", B)
probe("c out", C)
adder(A, B, C)
A.set_value(3, "user")
B.set_value(5, "user")
print("\n"*4)
B.set_value(30, "user")
print("\n"*4)
B.forget_value("user")
B.set_value(100, "user")

print("\n"*10)
# Fahrenheit converter

# Celsius <-> Fahrenheit conversion
C = connector()
F = connector()

cf_conv = celsius_fahrenheit_converter(C, F)
probe("Celsius Temp", C)
probe("Fahrenheit Temp", F)

print("done probes")

C.set_value(25, "User")
print("DONE !!!! 0", '\n'*5)

F.set_value(212, "User")
print("DONE !!!! 1", '\n'*5)

C.forget_value("User")

F.set_value(212, "User")
print("DONE !!!! 2")
