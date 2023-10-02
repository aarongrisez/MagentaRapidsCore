"""Environment definition for Magenta Rapids. An environment follows
the delegator pattern, and is responsible for delegating to a backend
and a mutator. Backends and mutators are injected into the environment
on initialization, and the environment will call the appropriate methods
on the backend and mutator when necessary.
"""

import typing as t


class Environment:
    """A standard Magenta Rapids environment"""

    def __init__(self, backend, mutator):
        self._backend = backend
        self._mutator = mutator

    def initialize(self):
        self._backend.initialize()

    def store(self, file_object: t.BinaryIO, extension="mid"):
        return self._backend.store(file_object, extension)

    async def mutate(self, number_steps):
        mutated = {}
        gen = self._backend.retrieve_all()
        async for (file, filename) in gen:
            mutated[filename] = self._mutator.mutate(file, number_steps)
        for filename, file in mutated.items():
            self._backend.save(file, filename)
