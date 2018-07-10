import os
import sys
import unittest

class TestAsyncMap(unittest.TestCase):

    def test_single_arg_funcs(self):
        """ test if we can pass single arguments of differnt types """

        single_int_arg = [1]
        r = async.map(simple_return_func, single_int_arg, chunk_size=1, modules=['time as t'])
        self.assertEqual(single_int_arg, r)

        single_int_arg = [1, 2, 3, 4, 5]
        r = async.map(simple_return_func, single_int_arg, chunk_size=1, modules=['time as t'])
        self.assertEqual(single_int_arg, r)

        single_str_arg = ['a', 'b', 'c', 'd']
        r = async.map(simple_return_func, single_str_arg, chunk_size=1, modules=['time as t'])
        self.assertEqual(single_str_arg, r)

        single_list_arg = [[[1, 2]], [[3, 4]]]
        r = async.map(simple_return_func, single_list_arg, chunk_size=1, modules=['time as t'])
        self.assertEqual([[1, 2], [3, 4]], r)

    def test_double_arg_func(self):
        """ test if we can pass multiple arguments """

        double_arg = [[1,2], [3,4], [5,6]]
        r = async.map(double_arg_func, double_arg, callback=on_exit, chunk_size=1, modules=['time as t', 'os', 'numpy'])

    def test_custom_return_obj_arg_func(self):
        """ test if we can pass a custer iterable object and return another
        custom object """

        obj = CustomIter(10)
        r = async.map(simple_return_func, obj, modules=['time as t'], runtime_globals=[ReturnObject])
        ref = ReturnObject(3)
        # for some reason isinstance evaluate to false - don't ask
        # maybe because double import / messing with sys.path?
        [self.assertTrue(str(type(obj)), str(type(ReturnObject))) for obj in r]
        self.assertEqual(len(r), 10)


class CustomIter(object):
    def __init__(self, maximum=10):
        self.maximum = maximum

    def __iter__(self):
        t.sleep(0.01)
        for i in range(self.maximum):
            yield ReturnObject(i)

class ReturnObject(object):
    def __init__(self, value):
        self.value = value

def simple_return_func(x):
    return x

def double_arg_func(x, y):
    t.sleep(1)
    return x * y

def single_list_arg_func(l=[]):
    t.sleep(1)
    return l

def double_list_arg_func(l1=[], l2=[]):
    t.sleep(1)
    return l1, l2

def on_exit(result):
    print 'DONE', result



#  single_arg = [1, 2, 3, 4, 5]
#  r = async.map(single_arg_func, single_arg, callback=on_exit, chunk_size=1, modules=['time as t', 'os', 'numpy'])
#
#  import numpy
#  single_np_arg = numpy.array([1, 2, 3, 4, 5])
#  r = async.map(single_arg_func, single_np_arg, callback=on_exit, chunk_size=1, modules=['time as t', 'os', 'numpy'])
#
#
#  single_list_arg = [[[1,2,3,4]],[[5,6,7,8]]]
#  r = async.map(single_list_arg_func, single_list_arg, callback=on_exit, chunk_size=1, modules=['time as t', 'os', 'numpy'])
#
#  double_list_arg =[[[1,2],[2,3]],[[4,5],[6,7]]]
#  r = async.map(double_list_arg_func, double_list_arg, callback=on_exit, chunk_size=1, modules=['time as t', 'os', 'numpy'])
#
#  reload(async)
#  r = async.apply(single_arg_func, [10], callback=on_exit, modules=['time as t'])


if __name__ == '__main__':

    package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(package_path)
    import async

    unittest.main()
