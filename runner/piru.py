# PIpeline RUnner -- (c)2022 David SPORN
# GPL3
########################################
import copy
from console.logger import trace, debug, info, ok

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
            info(f"Start of pipeline {func.__name__}")
            debug(args)
            debug(kwargs)
            result = func(kwargs)
            trace("call each before_all")
            for befa in pipeline_before_all:
                befa['func'](env=result)
            trace("for each stage...")
            for stage in stages:
                trace("  \\--filter jobs by stage and execute")
                jobs = [j for j in pipeline_jobs if j['stage'] == stage or j['stage'] == '']
                before_each = [j for j in pipeline_before_each if j['stage'] == stage or j['stage'] == '']
                after_each = [j for j in pipeline_after_each if j['stage'] == stage or j['stage'] == '']
                for job in jobs:
                    env = copy.deepcopy(result)
                    for befe in before_each:
                        debug(befe)
                        befe['func'](env=env)
                    job['func'](env=env)
                    for afte in after_each:
                        afte['func'](env=env)
            for afta in pipeline_after_all:
                trace("call each after_all")
                afta['func'](env=env)
            ok(f"End of pipeline {func.__name__}")
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

def job(_func=None, *, stage: str = ''):
    trace(f"Register job for stage '{stage}'")
    def decorator_job(func):
        def wrapper_job(*args, **kwargs):
            # before
            # func(kwargs)
            # after
            pass
        return func

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

def before_each(_func=None, **kwargs):
    trace(kwargs)
    raw_stage = kwargs['stage']
    stage = {} if None == raw_stage else raw_stage
    trace(f"Register before_each for stage '{stage}'")
    def decorator_before_each(*args,**kwargs):
        debug(args)
        debug(kwargs)
        if len(args) > 0:
            return args[0] # this is the function
        def wrapper_before_each(kwargs):
            # before
            return func(kwargs)
            # after
            pass
        return wrapper_before_each

    if _func is None:
        result = decorator_before_each
        register_func(pipeline_before_each, result, stage)
        return result
    else:
        result = _func
        register_func(pipeline_before_each, result, stage)
        return result

def after_each(_func=None, *, stage: str = ''):
    trace(f"Register after_each for stage '{stage}'")
    def decorator_after_each(func):
        def wrapper_after_each(*args, **kwargs):
            # before
            # func(kwargs)
            # after
            pass
        return func

    if _func is None:
        result = decorator_after_each
        register_func(pipeline_after_each, result, stage)
        return result
    else:
        result = decorator_after_each(_func)
        register_func(pipeline_after_each, result, stage)
        return result
