from src.agent import FooTask, Foo

def test_agent_complex_type():
    foo_task = FooTask(name="foo_task")
    res = foo_task(foos=[Foo(val="a"), Foo(val="b")])
    assert res.foos[1].val == "b"