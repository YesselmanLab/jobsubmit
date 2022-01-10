from jobsubmit import arguments, settings
from itertools import product
import yaml


def test_bool():
    arg = arguments.BoolArgument("arg1", "-")
    assert list(arg) == ["-arg1 ", ""]
    arg = arguments.BoolArgument("arg1", "--")
    assert list(arg) == ["--arg1 ", ""]


def test_mult():
    arg = arguments.MultArgument("arg1", "-", [0, 1])
    assert list(arg) == ["-arg1 0 ", "-arg1 1 "]


def test_mult_2():
    arg = arguments.MultArgument("arg1", "--", ["test_1", "test_2"], no_name=True)
    print(list(arg))


def test_combo():
    arg1 = arguments.BoolArgument("local", "--")
    arg2 = arguments.BoolArgument("no-unal", "--")
    combo = arguments.ComboArgument("bt2_alignment_args", "--", ";", [arg1, arg2])
    val = next(combo.__iter__())
    print(val)


def test_iter_tools_1():
    arg1 = arguments.BoolArgument("bool", "--")
    arg2 = arguments.MultArgument("int", "-", [0, 1])
    combos = product(arg1, arg2)
    arg_strs = ["--bool -int 0 ", "--bool -int 1 ", "-int 0 ", "-int 1 "]
    for i, c in enumerate(combos):
        args = "".join(c)
        assert args == arg_strs[i]


def test_int_parse():
    path = settings.get_py_path() + "/resources/testing/int_1.yml"
    params = yaml.load(open(path), Loader=yaml.FullLoader)
    arg = arguments.get_numerical_argument("arg1", params["arg1"])
    assert list(arg) == ["-arg1 0 ", "-arg1 2 "]

    path = settings.get_py_path() + "/resources/testing/int_2.yml"
    params = yaml.load(open(path), Loader=yaml.FullLoader)
    arg = arguments.get_numerical_argument("arg1", params["arg1"])
    assert list(arg) == ["-arg1 100 ", "-arg1 0 "]


def test_arg_set():
    arg_set = arguments.ArgumentSet()
    arg = arguments.MultArgument("int", "-", [0, 1])
    arg_set.add_argument(arg)
    arg_set.setup()
    args = list(iter(arg_set))[0]
    assert args["int"] == "-int 0 "


def test_arg_set_2():
    pass
