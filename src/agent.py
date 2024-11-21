from __future__ import annotations

import typing
from dataclasses import dataclass

from flyteidl.core.execution_pb2 import TaskExecution
from flytekit import FlyteContextManager
from flytekit.core.type_engine import TypeEngine
from flytekit.configuration import SerializationSettings
from flytekit.core.base_task import PythonTask
from flytekit.core.interface import Interface
from flytekit.extend.backend.base_agent import (
    AgentRegistry,
    Resource,
    SyncAgentBase,
    SyncAgentExecutorMixin,
)
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate

@dataclass
class Foo:
    val: str


class FooAgent(SyncAgentBase):
    def __init__(self) -> None:
        super().__init__(task_type_name="foo")

    async def do(
        self,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
        **kwargs: typing.Any,
    ) -> Resource:
        ctx = FlyteContextManager.current_context()
        input_python_value = TypeEngine.literal_map_to_kwargs(
            ctx, inputs, {"foos": typing.Optional[typing.List[Foo]]}
        )

        return Resource(
            phase=TaskExecution.SUCCEEDED,
            outputs={
                "foos": input_python_value["foos"]
            },
        )


AgentRegistry.register(FooAgent())


class FooTask(SyncAgentExecutorMixin, PythonTask):  # type: ignore
    _TASK_TYPE = "foo"

    def __init__(self, name: str, **kwargs: typing.Any) -> None:
        inputs = {"foos": typing.Optional[typing.List[Foo]]}
        outputs = {"foos": typing.Optional[typing.List[Foo]]}

        super().__init__(
            task_type=self._TASK_TYPE,
            name=name,
            interface=Interface(inputs=inputs, outputs=outputs),
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> typing.Dict[str, typing.Any]:
        return {}
