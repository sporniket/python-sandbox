from console.logger import trace, debug, info, ok, warn, error, fatal
from runner.piru import pipeline, job, before_all, before_each, after_all, after_each, python_pipeline_runner

@pipeline(stages=("first_stage","second_stage","third_stage"))
class MySuiteOfTestWithExplicitStages:
    def __init__(self):
        trace("MySuiteOfTestWithExplicitStages -- Instanciation")
        pass

    def __call__(self):
        trace("MySuiteOfTestWithExplicitStages -- Call")
        pass

    # A stage is constitued by @jobs for the matching stage,
    # in the order that they will be found while introspecting the class (no guaranteed order)
    @job(stage="first_stage")
    def B(self):
        trace("MySuiteOfTestWithExplicitStages -- B")
        pass

    @job(stage="first_stage")
    def A(self):
        trace("MySuiteOfTestWithExplicitStages -- A")
        pass

    @job(stage="second_stage")
    def C(self):
        trace("MySuiteOfTestWithExplicitStages -- C")
        pass

    @job(stage="second_stage")
    def F(self):
        trace("MySuiteOfTestWithExplicitStages -- F")
        pass

    @job(stage="third_stage")
    def E(self):
        trace("MySuiteOfTestWithExplicitStages -- E")
        pass

    @job(stage="second_stage")
    def D(self):
        trace("MySuiteOfTestWithExplicitStages -- D")
        pass

    @job(stage="third_stage")
    def G(self):
        trace("MySuiteOfTestWithExplicitStages -- G")
        pass

    @job()
    def H(self): # performed at each stage
        trace("MySuiteOfTestWithExplicitStages -- H")
        pass

    @before_all
    def setup(self):
        trace("MySuiteOfTestWithExplicitStages -- setup")
        pass

    @after_all
    def teardown(self):
        trace("MySuiteOfTestWithExplicitStages -- teardown")
        pass

    @before_each(stage="first_stage")
    def enter_first_stage_job(self): # called only before performing each job of a given stage
        trace("MySuiteOfTestWithExplicitStages -- enter_first_stage_job")
        pass

    @after_each
    def exit_job(self): # called after each jobs has been called during any stage.
        trace("MySuiteOfTestWithExplicitStages -- exit_job")
        pass


### demo
if __name__ == "__main__":
    instance = MySuiteOfTestWithExplicitStages()
    debug(instance)
    #python_pipeline_runner(MySuiteOfTestWithExplicitStages())
