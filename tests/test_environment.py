"""
Sample Test
"""
# pylint: disable=redefined-outer-name, unused-argument

import os
import pytest
import tempfile

import magenta_rapids.environment

@pytest.fixture
def local_file_backend():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield magenta_rapids.environment.LocalFileBackend(tmpdir)

def test_local_file_backend_initialization(local_file_backend):
    local_file_backend.initialize()
    assert os.path.exists(local_file_backend.processed_path)
    assert os.path.exists(local_file_backend.unprocessed_path)

