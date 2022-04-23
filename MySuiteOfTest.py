from console.logger import trace, debug, info, ok, warn, error, fatal
from runner.piru import pipeline, job, before_all, before_each, after_all, after_each

@pipeline(stages=("first_stage","second_stage","third_stage"))
def performMySuiteOfTests(env:dict = {}):
    info("Start of pipeline -- init")
    debug(env)
    return env

# A stage is constitued by @jobs for the matching stage,
# in the order that they will be found while introspecting the class (no guaranteed order)
@job(stage="first_stage")
def B():
    info("performing... B")
    pass

@job(stage="first_stage")
def A():
    info("performing... A")
    pass

@job(stage="second_stage")
def C():
    info("performing... C")
    pass

@job(stage="second_stage")
def F():
    info("performing... F")
    pass

@job(stage="third_stage")
def E():
    info("performing... E")
    pass

@job(stage="second_stage")
def D():
    info("performing... D")
    pass

@job(stage="third_stage")
def G():
    info("performing... G")
    pass

@job()
def H(): # performed at each stage
    info("performing... H")
    pass

@before_all
def setup():
    info("performing... setup")
    pass

@after_all
def teardown():
    info("performing... teardown")
    pass

@before_each(stage="first_stage")
def enter_first_stage_job(): # called only before performing each job of a given stage
    info("performing... enter_first_stage_job")
    pass

@after_each
def exit_job(): # called after each jobs has been called during any stage.
    info("performing... exit_job")
    pass


### demo
if __name__ == "__main__":
    performMySuiteOfTests(env={'dir.current':'this/path', 'dir.basedir':'that/path'})
