# map
maya asynchronous processing

# Overview
**map** allows to evaluate python functions from within Maya in an independent Python
interpreter wrapping the multiprocessing package to achieve asynchronous processing.
In particular *map* wrappes the multiprocessing.Pool().map() method, a parallel equivalent
of python's build-in map() function.

# Dependencies
**map** depends on *dill*.
```
pip install dill
```

## async.map()
```python
async.map(func, iterable, callback=None, chunk_size=1, callback=None, modules=None, runtime_globals=None)
```
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
r = async.map(double_arg_func, double_arg, callback=on_exit, modules=['time as t', 'os', 'numpy'])
```

Map to a function which takes multiple lists as arguments and wait for the subprocess to finish
```python    
def double_list_arg_func(l1, l2):
    if isinstance(l1, list) and isinstance(l2, list):
        t.sleep(1)
        return l1, l2
    
double_list_arg =[[[1,2],[2,3]],[[4,5],[6,7]]]
r = async.map(double_list_arg_func, double_list_arg, modules=['time as t', 'os', 'numpy'])
```
