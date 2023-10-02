"""Backends for Magenta Rapids. A backend is responsible for storing files
and retrieving them when necessary. Backends must implement the `store` and
`retrieve_all` methods, as well as several other helpers which abstract
away the underlying storage mechanism.
"""

import abc
import hashlib
import os
import typing as t


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

    @property
    @abc.abstractmethod
    def path(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def processed_path(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def unprocessed_path(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def retrieve_all(self):
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

    def store(self, file_object: t.BinaryIO, extension="mid"):
        file_object.seek(os.SEEK_SET)
        sha_to_store = hashlib.sha1(file_object.read()).hexdigest()
        full_target_path = os.path.join(
            self._root_path,
            self.UNPROCESSED_DIRECTORY_PREFIX,
            f"{sha_to_store}.{extension}",
        )
        if os.path.exists(full_target_path):
            with open(full_target_path, "rb") as existing_file_object:
                existing_sha = hashlib.sha1(existing_file_object.read()).hexdigest()
            if sha_to_store == existing_sha:
                raise ValueError(
                    f"Cannot store file at {full_target_path}, a file with that "
                    "hash already exists in this environment"
                )
        file_object.seek(os.SEEK_SET)
        with open(full_target_path, "wb") as file_obj:
            file_obj.write(file_object.read())
        file_object.seek(os.SEEK_SET)
        return full_target_path

    def initialize(self):
        if not os.path.isdir(
            os.path.join(self._root_path, self.PROCESSED_DIRECTORY_PREFIX)
        ):
            os.mkdir(os.path.join(self._root_path, self.PROCESSED_DIRECTORY_PREFIX))
        if not os.path.isdir(
            os.path.join(self._root_path, self.UNPROCESSED_DIRECTORY_PREFIX)
        ):
            os.mkdir(os.path.join(self._root_path, self.UNPROCESSED_DIRECTORY_PREFIX))

    async def retrieve_all(self) -> t.AsyncGenerator[t.BinaryIO, None]:
        for root, _, files in os.walk(self.unprocessed_path):
            for filename in files:
                path = os.path.join(root, filename)
                with open(path, "rb") as file_obj:
                    yield (file_obj, filename)

    def save(self, file: t.BinaryIO, filename: str):
        file.seek(os.SEEK_SET)
        with open(os.path.join(self.processed_path, filename), "wb") as file_obj:
            file_obj.write(file.read())
        file.seek(os.SEEK_SET)
