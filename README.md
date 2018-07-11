# map
maya asynchronous processing

# Overview
**map** provides a convenient way to serialize python code and objects and send them to an
independent Python interpreter to achieve parallelism with python from within Maya.
In particular, **map** wrappes *multiprocessing.Pool().map* and *apply()* in the python
iterpreter to achieve concurrency.


# Dependencies
*dill* needs to be installed in order to run **map**.
```
pip install dill
```

## async.map()
```python
async.map(func, iterable, callback=None, chunk_size=1, callback=None, modules=None, runtime_globals=None)
```
parallel equivalent of python's builtin *map()*.

**chunk_size**<br/>
The chunk_size argument chops the iterable into a number of chunks which
are submitted to the process pool as separate tasks. The (approximate) size
of these chunks can be specified by setting chunksize to a positive integer.

**callback**<br/>
If a callback is given the subprocess is executed in a seperate thread to
keep Maya responsive. In this case the thread which runs the subprocess is
returned. Otherwise this functions waits for the result and returns it.

**modules**<br/>
Any module used in the function must be given in the modules argument.
The modules argument must be a list of module names.

**runtime_globals**<br/>
This argument takes any kind of object that is needed by the executed function.


## async.apply()
```python
async.apply(func, args=None, kwargs=None, callback=None, modules=None, runtime_globals=None)
```
parallel euqivalent of python's builtin *apply()*.


# Limitations
Since the subprocess runs in a separate interpreter there are a few limitations on what can be done
- Running Maya commands in the subprocess is not supported.
- Modules used in the function must be added as argument in order to be imported.
- Global variable that are needed for the function call must be passed to runtime_globals argument.
- TODO


# Examples

Map to function with a single argument and wait until the subprocess has finished:
```python
def single_arg_func(x):
    t.sleep(1)
    return x * x

import numpy
single_np_arg = numpy.array([1, 2, 3, 4, 5])
result = async.map(single_arg_func, single_np_arg, modules=['time as t', 'numpy'])
print result
```

Map to function with multiple argument and call on_exit() as soon as the subprocess has finished:
```python
def double_arg_func(x, y):
    t.sleep(1)
    return x * y

def on_exit(result):
    print 'Subprocess done:', result
        
double_arg = [[1,2], [3,4], [5,6]]
r = async.map(double_arg_func, double_arg, callback=on_exit, modules=['time as t'])
```

Map to a function which takes multiple lists as arguments and wait for the subprocess to finish
```python    
def double_list_arg_func(l1, l2):
    if isinstance(l1, list) and isinstance(l2, list):
        t.sleep(1)
        return l1, l2
    
double_list_arg =[[[1,2],[2,3]],[[4,5],[6,7]]]
r = async.map(double_list_arg_func, double_list_arg, modules=['time as t'])
```

Retun custom object by iterator object
```python
obj = CustomIter(10)
r = async.map(simple_return_func, obj, modules=['time as t'], runtime_globals=[ReturnObject])
print r

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
```
