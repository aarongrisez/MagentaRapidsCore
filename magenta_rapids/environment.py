import abc
import hashlib
import io
import os
import typing as t
import mido


class AbstractFileBackend(abc.ABC):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    def initialize(self):
        raise NotImplementedError

    @abc.abstractmethod
    def store(self, file_object: t.BinaryIO, extension: str = "mid"):
        raise NotImplementedError
    
    @abc.abstractproperty
    def path(self):
        raise NotImplementedError
    
    @abc.abstractproperty
    def processed_path(self):
        raise NotImplementedError
    
    @abc.abstractproperty
    def unprocessed_path(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    async def retrieve_all(self):
        raise NotImplementedError


class AbstractMutator(abc.ABC):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
    @abc.abstractmethod
    def mutate(self, file_object: t.BinaryIO) -> t.BinaryIO:
        raise NotImplementedError


class LocalFileBackend(AbstractFileBackend):
    PROCESSED_DIRECTORY_PREFIX = "processed"
    UNPROCESSED_DIRECTORY_PREFIX = "unprocessed"

    def __init__(self, local_root_path: str):
        self._root_path = local_root_path

    @property
    def path(self):
        return self._root_path
    
    @property
    def processed_path(self):
        return os.path.join(self._root_path, self.PROCESSED_DIRECTORY_PREFIX)
    
    @property
    def unprocessed_path(self):
        return os.path.join(self._root_path, self.UNPROCESSED_DIRECTORY_PREFIX)
    
    def store(self, file_object: t.BinaryIO, extension = "mid"):
        file_object.seek(os.SEEK_SET)
        sha_to_store = hashlib.sha1(file_object.read()).hexdigest()
        full_target_path = os.path.join(
            self._root_path,
            self.UNPROCESSED_DIRECTORY_PREFIX,
            f"{sha_to_store}.{extension}"
        )
        if os.path.exists(full_target_path):
            with open(full_target_path, 'rb') as existing_file_object:
                existing_sha = hashlib.sha1(existing_file_object.read()).hexdigest()
            if sha_to_store == existing_sha:
                raise ValueError(f"Cannot store file at {full_target_path}, a file with that "
                                  "hash already exists in this environment")
        file_object.seek(os.SEEK_SET)
        with open(full_target_path, 'wb') as f:
            f.write(file_object.read())
        file_object.seek(os.SEEK_SET)
        return full_target_path
    
    def initialize(self):
        if not os.path.isdir(os.path.join(self._root_path, self.PROCESSED_DIRECTORY_PREFIX)):
            os.mkdir(os.path.join(self._root_path, self.PROCESSED_DIRECTORY_PREFIX))
        if not os.path.isdir(os.path.join(self._root_path, self.UNPROCESSED_DIRECTORY_PREFIX)):
            os.mkdir(os.path.join(self._root_path, self.UNPROCESSED_DIRECTORY_PREFIX))
    
    async def retrieve_all(self) -> t.AsyncGenerator[t.BinaryIO, None]:
        for root, _, files in os.walk(self.unprocessed_path):
            for filename in files:
                path = os.path.join(root, filename)
                with open(path, 'rb') as f:
                    yield (f, filename)
    
    def save(self, file: t.BinaryIO, filename: str):
        file.seek(os.SEEK_SET)
        with open(os.path.join(self.processed_path, filename), 'wb') as f:
            f.write(file.read())
        file.seek(os.SEEK_SET)


class SimpleMutator(AbstractMutator):

    def __init__(self, *args, **kwargs):
        pass

    def __alter_note(self, message: mido.Message) -> mido.Message:
        if message.type == "note_off":
            note_off_delay = 50
        else:
            note_off_delay = 0
        return message.copy(
            time=
                int(
                    message.time + 
                    note_off_delay +
                    ((60 / message.note ** 2) * (message.time ** 1.1 + message.note ** 1.9))
                )
        )
    
    def mutate(self, file_object: t.BinaryIO, n: int) -> t.BinaryIO:
        file_object.seek(os.SEEK_SET)
        file = mido.MidiFile(file=file_object)
        file_object.seek(os.SEEK_SET)
        for track in file.tracks:
            for idx, message in enumerate(track):
                if message.type in ("note_on", "note_off"):
                    for i in range(n):
                        message = self.__alter_note(message)
                    track[idx] = message
        new_file_object = t.cast(t.BinaryIO, io.BytesIO())
        file.save(file=new_file_object)
        new_file_object.seek(os.SEEK_SET)
        return new_file_object


class Environment:
    """A standard Magenta Rapids environment
    """

    def __init__(self, backend, mutator):
        self._backend = backend
        self._mutator = mutator
    
    def initialize(self):
        self._backend.initialize()
    
    def store(self, file_object: t.BinaryIO, extension = "mid"):
        return self._backend.store(file_object, extension)
    
    async def mutate(self, n):
        mutated = dict()
        gen = self._backend.retrieve_all()
        async for (file, filename) in gen:
            mutated[filename] = self._mutator.mutate(file, n)
        for filename, file in mutated.items():
            self._backend.save(file, filename)