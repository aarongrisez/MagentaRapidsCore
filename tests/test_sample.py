"""
Sample Test
"""
# pylint: disable=redefined-outer-name, unused-argument

import pytest
import magenta_rapids.biz


@pytest.fixture
def sample_fixture():
    """Setup test fixture"""
    return 1


def test_func(sample_fixture):
    """Test the sample function"""
    assert magenta_rapids.biz.sample_func(1) == 2


def test_negative(sample_fixture):
    """Negative test of sample function"""
    assert magenta_rapids.biz.sample_func(-2) == -1
