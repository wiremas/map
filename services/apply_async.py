import sys
import types
import base64
import dill
import importlib
import multiprocessing

if __name__ == '__main__':

    # decode and unpickle function and input list
    code = dill.loads(base64.decodestring(sys.argv[1]))
    args = dill.loads(base64.decodestring(sys.argv[2]))
    kwargs = dill.loads(base64.decodestring(sys.argv[3]))
    modules = dill.loads(base64.decodestring(sys.argv[4]))
    runtime_globals = dill.loads(base64.decodestring(sys.argv[5]))

    # run import & generate globals for the function
    for module in modules:
        module = module.split(' as ')
        if len(module) == 2:
            name = module[1]
            module = importlib.import_module(module[0])
            globals()[name] = module
        else:
            module = importlib.import_module(module[0])
            globals()[module.__name__] = module

    # add runtime globals
    for glb in runtime_globals:
        globals()[glb.__name__] = glb

    # create funcrtion from code object
    func = types.FunctionType(code, globals(), 'remote_func')

    if args and kwargs:
        result = func(*args, **kwargs)
    elif args and not kwargs:
        result = func(*args)
    elif not args and kwargs:
        result = func(**kwargs)
    else:
        result = func()

    result_encoded = '<<retval>>{}'.format(base64.encodestring(dill.dumps(result)).replace('\n',''))

    # return results
    sys.stdout.write(result_encoded)
    sys.stdout.flush()
    sys.exit(0)


