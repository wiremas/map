""" wrapper functions that utilize the multiprocessing module in a seperate
childe process. This allows to overcome Maya's limitation of not beeing able
to run the multiprocessing module inside Maya's python interpreter """

import os
import dill
import types
import base64
import platform
import threading
import subprocess
from functools import wraps


def map(func, iterable, chunk_size=1, callback=None, modules=None):
    """ A wrapper function for multiprocessing.map().
    A parallel equivalent of the map() built-in function (it supports only one
    iterable argument though) in a seperate subprocess.
    The chunksize argument chops the iterable into a number of chunks which
    are submitted to the process pool as separate tasks. The (approximate) size
    of these chunks can be specified by setting chunksize to a positive integer.
    If a callback is given the subprocess is executed in a seperate thread to
    keep Maya responsive. In this case the thread which runs the subprocess is
    returned. Otherwise this functions waits for the result and returns it.
    Any module used in the function must be given in the modules argument.
    The modules argument must be a list of module names (strings). Modules
    can also be imported like:
        ['os', 'numpy as np']
    :param func: callable the be executed
    :type func: callable
    :param iterable: the iterable that will be mapped against the callable
    :type iterable:
    :param chunk_size: chunks size per process
    :param callback: function that will be called when the subprocess is finished
    :param modules: modules that will imported in the child process
    :return: Thread object if callback, else result
    """

    if not isinstance(func, types.FunctionType):
        raise RuntimeError('First argument must be of type function')

        #  raise RuntimeError('First argument must be of type function')

    client = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'services', 'map_async.py')

    encoded_code = base64.encodestring(dill.dumps(func.func_code))
    encoded_list = base64.encodestring(dill.dumps(iterable))
    encoded_chunksize = base64.encodestring(dill.dumps(chunk_size))
    encoded_modules = base64.encodestring(dill.dumps(modules))
    cmd = ['python', client, encoded_code, encoded_list, encoded_chunksize,
           encoded_modules]

    return start_subprocess(cmd, callback)

def start_subprocess(cmd, callback):
    """ initialize running subprocess. if a callback is given run the
    subprocess in a new thread and return the thread. otherwise wait for the
    result and return it. """

    if callback:
        thread = threading.Thread(target=run_subprocess, args=(cmd, callback))
        thread.start()
        return thread
    else:
        return run_subprocess(cmd, None)


def run_subprocess(cmd, callback):
    """ run the command in the actual subprocess """

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    # get return object and reconstruct result
    result = None
    for line in out.splitlines():
        if line.startswith('<<retval>>'):
            result = dill.loads(base64.decodestring(line[10:]))
            break
    if result is None:
        raise RuntimeError('Failed to run map_async:\n{}\n{}'.format(out, err))

    if callback:
        callback(result)
    else:
        return result

