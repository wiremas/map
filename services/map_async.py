import sys
import types
import base64
import dill
import importlib
import multiprocessing

if __name__ == '__main__':

    # decode and unpickle function and input list
    code = dill.loads(base64.decodestring(sys.argv[1]))
    iterable = dill.loads(base64.decodestring(sys.argv[2]))
    chunk_size = dill.loads(base64.decodestring(sys.argv[3]))
    modules = dill.loads(base64.decodestring(sys.argv[4]))
    #  service = dill.loads(base64.decodestring(sys.argv[5]))

    # run import & generate globals for the function
    runtime_globals = {}
    for module in modules:
        module = module.split(' as ')
        if len(module) == 2:
            name = module[1]
            module = importlib.import_module(module[0])
            runtime_globals[name] = module
        else:
            module = importlib.import_module(module[0])
            runtime_globals[module.__name__] = module

    # create funcrtion from code object
    func = types.FunctionType(code, runtime_globals, 'remote_func')

    # create a hook that can be pickled by Pool's Queue
    def hook(args):
        # pass arguments to function if iterable
        if hasattr(args, '__iter__'):
            return func(*args)
        # otherwise pass single argument
        else:
            return func(args)

    # initialize the pool
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(pool_size)

    # parallel map & encode results
    result = pool.map(hook, iterable, chunk_size) #pool.map_async(hook, iterable)
    pool.close()
    result_encoded = '<<retval>>{}'.format(base64.encodestring(dill.dumps(result)).replace('\n',''))

    # return results
    sys.stdout.write(result_encoded)
    sys.stdout.flush()
    sys.exit(0)
