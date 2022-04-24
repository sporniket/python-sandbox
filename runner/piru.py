# PIpeline RUnner -- (c)2022 David SPORN
# GPL3
########################################
import copy
from console.logger import trace, debug, info, ok, warn

pipeline_exec = None
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
    registry.append(item)
#
# Concepts :
# * pipeline stages
#
# class annotation
def pipeline(_func=None, *, stages: tuple):
    trace(f"Register pipeline stages : {stages}")
    # TODO registers the sequence of stages
    def decorator_pipeline(func):
        def wrapper_pipeline(*args, **kwargs):
            info(f"===[ START OF PIPELINE {func.__name__} ]===")
            result = func(*args, **kwargs)
            for befa in pipeline_before_all:
                befa['func'](env=result)
            for stage in stages:
                info(f"======[ START OF STAGE {stage} ]======")
                jobs = [j for j in pipeline_jobs if j['stage'] == stage or j['stage'] == '']
                before_each = [j for j in pipeline_before_each if j['stage'] == stage or j['stage'] == '']
                after_each = [j for j in pipeline_after_each if j['stage'] == stage or j['stage'] == '']
                for job in jobs:
                    env = copy.deepcopy(result)
                    for befe in before_each:
                        befe['func'](env=env)
                    job['func'](env=env)
                    for afte in after_each:
                        afte['func'](env=env)
                ok(f"======[ END OF STAGE {stage} ]======")
            for afta in pipeline_after_all:
                afta['func'](env=env)
            ok(f"===[ END OF PIPELINE {func.__name__} ]===")
            return result
        return wrapper_pipeline
    global pipeline_exec
    if _func is None:
        result = decorator_pipeline
        pipeline_exec = result
        return result
    else:
        result = decorator_pipeline(_func)
        pipeline_exec = result
        return result

def job(_func=None, **kwargs):
    trace("Register job")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        register_func(pipeline_jobs, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

def before_all(func):
    trace(f"Register before_all")
    def wrapper_before_all(* args, **kwargs):
        # before
        # func(kwargs)
        # after
        pass
    result = func
    register_func(pipeline_before_all, result)
    return result

def after_all(func):
    trace(f"Register after_all")
    def wrapper_after_all(* args, **kwargs):
        # before
        # func(kwargs)
        # after
        pass
    result = func
    register_func(pipeline_after_all, result)
    return result


def before_each(_func=None, *args, **kwargs):
    trace("Register before_each")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        register_func(pipeline_before_each, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)

def after_each(_func=None, **kwargs):
    trace("Register after_each")
    def decorator(func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        stage = kwargs['stage'] if 'stage' in kwargs else ''
        register_func(pipeline_after_each, wrapper, stage)
        return wrapper
    if _func is None:
        return decorator
    else:
        return decorator(_func)
