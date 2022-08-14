from dataclasses import dataclass

import pytest

from jmapc.methods import Response


def test_method_base_get_method_name() -> None:
    @dataclass
    class TestResponseModel(Response):
        method_namespace = "Test"
        method_type = "echo"

    assert TestResponseModel.get_method_name() == "Test/echo"


def test_method_base_get_method_name_no_method_type() -> None:
    @dataclass
    class TestResponseModel(Response):
        method_namespace = "Test"

    with pytest.raises(ValueError):
        TestResponseModel.get_method_name()


def test_method_base_get_method_name_no_method_namespace() -> None:
    @dataclass
    class TestResponseModel(Response):
        method_type = "echo"

    with pytest.raises(ValueError):
        TestResponseModel.get_method_name()
