import itertools

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
                yield ''

class MultArgument(Argument):
    def __init__(self, name, atype, values, no_name=False):
        super().__init__(name, atype)
        self.values = values
        self.no_name = no_name

    def __iter__(self):
        for i in self.values:
            if self.no_name:
                yield str(i)
            else:
                yield self.atype + self.name + " " + str(i) + " "


def get_int_argument(d):
    pass





