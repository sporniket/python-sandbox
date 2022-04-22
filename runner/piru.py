# PIpeline RUnner -- (c)2022 David SPORN
# GPL3
########################################$
#
# Concepts :
# * pipeline stages
#
# class annotation
class pipeline:
    def __init__(self, clazz=None, *, stages: tuple = ()):
        self.stages = stages
        self.clazz = clazz

    def __call__(self, *args, **kwargs):
        self.instance = self.clazz(args, kwargs)
        return self

    def execute(env):
        # foreach stage listed, execute self.instance[stage](env)
        pass

def job(func, *, stage: str = None):
    def wrapper_stage(*args, **kwargs):
        # before
        func(args, kwargs)
        # after
    return wrapper_stage

def python_pipeline_runner(p, env: dict = {}):
    if p is pipeline:
        # if p instance of pipeline --> p.execute(env,...)
        p.execute(env)
    else:
        # else scan class to spot methods decorated with @stages, and execute them in that order
        Pipeline(p).execute(env)
