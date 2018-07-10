import os
import sys
import unittest

class TestAsyncApply(unittest.TestCase):

    def test_single_apply(self):

        r = async.apply(single_return_func, [10])
        self.assertEqual(r, 10)

        r = async.apply(double_return_func, [10, 20])
        self.assertEqual(r, (10, 20))

        r = async.apply(kwarg_return_func, kwargs={'a':10, 'b':20})
        self.assertEqual(r, (10, 20))

        r = async.apply(arg_kwarg_return_func, [1, 2], {'a':10, 'b':20})
        self.assertEqual(r, (1, 2, 10, 20))

    def test_import_apply(self):
        r = async.apply(sqrt_func, [10], modules=['math as m'])
        self.assertEqual(round(r, 2), 3.16)

    def test_runtime_globals_appl(self):
        r = async.apply(return_obj_func, [ReturnObject(1)], runtime_globals=[ReturnObject])
        self.assertEqual(r.value, 5)
        self.assertEqual(str(type(r)), str(type(ReturnObject(0))))

def single_return_func(x):
    return x

def double_return_func(x, y):
    return x, y

def kwarg_return_func(a=1, b=2):
    return a, b

def arg_kwarg_return_func(x, y, a=1, b=2):
    return x, y, a, b

def sqrt_func(x):
    return m.sqrt(x)

def return_obj_func(obj):
    return ReturnObject(5)

class ReturnObject(object):
    def __init__(self, value):
        self.value = value


if __name__ == '__main__':

    package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(package_path)
    import async

    unittest.main()
