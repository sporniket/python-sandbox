# PIpeline RUnner -- (c)2022 David SPORN
# GPL3
########################################
from console.logger import debug, info
#
# Concepts :
# * pipeline stages
#
# class annotation
def pipeline(*, stages: tuple):
    debug(f"pipeline stages : {stages}")
    # TODO registers the sequence of stages
    def decorator_pipeline(func):
        # TODO scans the class to look for jobs and extension points.
        return func
    return decorator_pipeline

def job(_func=None, *, stage: str = None):
    def decorator_job(func):
        def wrapper_job(*args, **kwargs):
            # before
            func(args, kwargs)
            # after
        return wrapper_job

    if _func is None:
        return decorator_job
    else:
        return decorator_job(_func)

def before_all(func):
    def wrapper_before_all(* args, **kwargs):
        # before
        func(args, kwargs)
        # after
    return wrapper_before_all

def after_all(func):
    def wrapper_after_all(* args, **kwargs):
        # before
        func(args, kwargs)
        # after
    return wrapper_after_all

def before_each(_func=None, *, stage: str = None):
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

def after_each(_func=None, *, stage: str = None):
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

def python_pipeline_runner(p, env: dict = {}):
    if p is pipeline:
        # if p instance of pipeline --> p.execute(env,...)
        p.execute(env)
    else:
        # else scan class to spot methods decorated with @stages, and execute them in that order
        Pipeline(p).execute(env)
