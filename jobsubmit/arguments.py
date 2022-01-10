import itertools
import numpy as np


class Argument(object):
    def __init__(self, name, atype):
        self.name = name
        self.atype = atype

    def __iter__(self):
        pass


class BoolArgument(Argument):
    def __init__(self, name, atype):
        super().__init__(name, atype)

    def __iter__(self):
        for val in [True, False]:
            if val:
                yield self.atype + self.name + " "
            else:
                yield ""


class MultArgument(Argument):
    def __init__(self, name, atype, values, no_name=False):
        super().__init__(name, atype)
        self.values = values
        self.no_name = no_name

    def __iter__(self):
        for i in self.values:
            if self.no_name:
                yield self.atype + str(i)
            else:
                yield self.atype + self.name + " " + str(i) + " "


class ComboArgument(Argument):
    def __init__(self, name, atype, delim, sub_args):
        super().__init__(name, atype)
        self.delim: str = delim
        self.sub_args = sub_args
        self.combos = itertools.product(*self.sub_args)

    def __iter__(self):
        for c in self.combos:
            vals = []
            for arg_val in c:
                if len(arg_val) > 2:
                    vals.append(arg_val[:-1])
            yield self.atype + self.name + ' "' + self.delim.join(vals) + '" '


def get_numerical_argument(name, d):
    if "values" in d and "range" in d:
        raise ValueError("cannot have both values and range for int/float")
    if "range" in d:
        r = d["range"]
        values = np.arange(*r)
    else:
        values = d["values"]
    no_name = False
    if "no_name" in d:
        no_name = True
    return MultArgument(name, d["atype"], values, no_name)


def get_combo_argument(name, d):
    pass


class ArgumentSet(object):
    def __init__(self):
        self.names = []
        self.args = []
        self.combos = []

    @classmethod
    def from_yaml(cls, yaml_d):
        pass

    def add_argument(self, arg: Argument):
        self.names.append(arg.name)
        self.args.append(arg)

    def setup(self):
        self.combos = itertools.product(*self.args)

    def __iter__(self):
        for c in self.combos:
            yield dict(zip(self.names, c))
