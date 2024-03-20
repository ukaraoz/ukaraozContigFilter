import functools
import json as json_
import subprocess
import sys
import os
import inspect
import time as time_
import functools

debug = True # toggle to turn off debug printing

subproc_run = functools.partial(
        subprocess.run, stdout=sys.stdout, stderr=sys.stderr, shell=True, executable='/bin/bash')

TAG_WIDTH = 80
MAX_LINES = 15

def dprint(*args, run='py', json=True, where=False, time=False, max_lines=60, exit=False, 
           subproc_run_kwargs={}, print_kwargs={}):
    '''Debug print'''

    if debug is not True:
        return None # dprint can be expected to return retcode

    print = functools.partial(__builtins__['print'], **print_kwargs)

    def print_format(arg):
        if json is True and isinstance(arg, (dict, list)):
            arg_json = json_.dumps(arg, indent=3, default=str)
            if max_lines is not None and arg_json.count('\n') > max_lines:
                arg_json = '\n'.join(arg_json.split('\n')[0:max_lines] + ['...'])
            print(arg_json)
        else:
            print(arg)

    print('#' * TAG_WIDTH)

    if where:
        stack = inspect.stack()
        print("(%s, line %d, %s)" % (stack[1][1], stack[1][2], stack[1][3])) # file, line, func
    
    for arg in args:
        if time:
            t0 = time_.time()
        if run:
            print('>> ' + arg)
            if run in ['cli', 'shell', 'bash']:
                completed_proc = subproc_run(arg, **subproc_run_kwargs)
                retcode = completed_proc.returncode
            elif isinstance(run, dict):
                print_format(eval(arg, run))
            elif run in ['py', 'python']:
                frame = inspect.stack()[1].frame
                env = {**frame.f_globals, **frame.f_locals}
                print_format(eval(arg, env))
            else:
                assert False
        else:
            print_format(arg)
        if time:
            t = time_.time() - t0
            print('[%fs]' % t)
    
    print('-' * TAG_WIDTH)

    if exit:
        sys.exit(0)
    
    # return last retcode
    if run in ['cli', 'shell']:
        return retcode


def where_am_i(f):
    '''Decorator'''
    def f_new(*args, **kwargs):
        dprint("where am i? in module `%s` method `%s`" % (globals()['__name__'], f.__qualname__))
        f(*args, **kwargs)
    return f_new


class TimePartition:
    def __init__(self):
        self.start = time_.time()
    def emit(self, duration_label):
        t = time_.time() - self.start
        dprint(
            '%s: %d min %d s' % (
                duration_label,
                round(t / 60),
                round(t % 60)
            ),
            run=None
        )
        self.start = time_.time()
