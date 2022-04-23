# PIpeline RUnner -- (c)2022 David SPORN
# GPL3
########################################
from console.logger import trace, debug, info

pipeline_exec = None
pipeline_stages = ()
pipeline_jobs = []
pipeline_before_all = []
pipeline_before_each = []
pipeline_after_each = []
pipeline_after_all = []

def register_func(registry:list, func, stage:str=''):
    item = {
        'func':func,
        'stage':stage
    }
    trace(item)
    registry += item 
#
# Concepts :
# * pipeline stages
#
# class annotation
def pipeline(*, stages: tuple):
    trace(f"Register pipeline stages : {stages}")
    # TODO registers the sequence of stages
    def decorator_pipeline(func):
        # TODO scans the class to look for jobs and extension points.
        return func
    return decorator_pipeline

def job(_func=None, *, stage: str = ''):
    trace(f"Register job for stage '{stage}'")
    def decorator_job(func):
        def wrapper_job(*args, **kwargs):
            # before
            func(args, kwargs)
            # after
        return wrapper_job

    if _func is None:
        result = decorator_job
        register_func(pipeline_jobs, result, stage)
        return result
    else:
        result = decorator_job(_func)
        register_func(pipeline_jobs, result, stage)
        return result

def before_all(func):
    trace(f"Register before_all")
    def wrapper_before_all(* args, **kwargs):
        # before
        func(args, kwargs)
        # after
    return wrapper_before_all

def after_all(func):
    trace(f"Register after_all")
    def wrapper_after_all(* args, **kwargs):
        # before
        func(args, kwargs)
        # after
    return wrapper_after_all

def before_each(_func=None, *, stage: str = ''):
    trace(f"Register before_each for stage '{stage}'")
    def decorator_before_each(func):
        def wrapper_before_each(*args, **kwargs):
            # before
            func(args, kwargs)
            # after
        return wrapper_before_each

    if _func is None:
        return decorator_before_each
    else:
        return decorator_before_each(_func)

def after_each(_func=None, *, stage: str = ''):
    trace(f"Register after_each for stage '{stage}'")
    def decorator_after_each(func):
        def wrapper_after_each(*args, **kwargs):
            # before
            func(args, kwargs)
            # after
        return wrapper_after_each

    if _func is None:
        return decorator_after_each
    else:
        return decorator_after_each(_func)

def python_pipeline_runner(env: dict = {}):
    info(f"Start python_pipeline_runner")
    debug("---- JOBS ----")
    debug(pipeline_jobs)
    debug("--------------")
    pass
