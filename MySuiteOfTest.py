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
def B(*, env:dict = {}):
    info("performing... B")
    pass

@job(stage="first_stage")
def A(*, env:dict = {}):
    info("performing... A")
    pass

@job(stage="second_stage")
def C(*, env:dict = {}):
    info("performing... C")
    pass

@job(stage="second_stage")
def F(*, env:dict = {}):
    info("performing... F")
    pass

@job(stage="third_stage")
def E(*, env:dict = {}):
    info("performing... E")
    pass

@job(stage="second_stage")
def D(*, env:dict = {}):
    info("performing... D")
    pass

@job(stage="third_stage")
def G(*, env:dict = {}):
    info("performing... G")
    pass

@job()
def H(*, env:dict = {}): # performed at each stage
    info("performing... H")
    pass

@before_all
def setup(*, env:dict = {}):
    info("performing... setup")
    pass

@after_all
def teardown(*, env:dict = {}):
    info("performing... teardown")
    pass

@before_each(stage="first_stage")
def enter_first_stage_job(*, env:dict = {}): # called only before performing each job of a given stage
    info("performing... enter_first_stage_job")
    pass

@after_each
def exit_job(*, env:dict = {}): # called after each jobs has been called during any stage.
    info("performing... exit_job")
    pass

### demo
if __name__ == "__main__":
    warn("before calling pipeline")
    performMySuiteOfTests(env={'dir.current':'this/path', 'dir.basedir':'that/path'})
    warn("after calling pipeline")
