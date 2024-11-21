import typing
from flytekit import task, workflow
from flytekit.core.task import Echo

from agent import Foo, FooTask

foo_task = FooTask(name="foo_task")
echo = Echo(name="echo", inputs={"message": str})


@task
def foos_task(foos: typing.Optional[typing.List[Foo]]) -> str:
    if not foos:
        return "no foos"
    return f"hi {foos}"


@workflow
def foo_wf() -> None:
    res = foo_task(foos=[Foo(val="a"), Foo(val="b")])
    foos_task(foos=res.foos)


if __name__ == "__main__":
    foo_wf()
