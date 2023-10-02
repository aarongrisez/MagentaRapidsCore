"""Tests for Magenta Rapids backends
"""
# pylint: disable=redefined-outer-name, unused-argument

import os
import tempfile
import pytest

from magenta_rapids import backends


@pytest.fixture
def local_file_backend():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield backends.LocalFileBackend(tmpdir)


def test_local_file_backend_initialization(local_file_backend):
    local_file_backend.initialize()
    assert os.path.exists(local_file_backend.processed_path)
    assert os.path.exists(local_file_backend.unprocessed_path)
