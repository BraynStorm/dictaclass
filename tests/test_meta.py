import os
import pytest


in_docker = os.path.exists(os.path.expanduser("/.dockerenv"))


def _test_all_python(py_version: str):
    try:
        assert (
            os.system(
                f"docker build"
                f" -q"
                f" -t dictaclass-test:{py_version}"
                f" -f test.Dockerfile"
                f" --build-arg PY_VERSION={py_version}"
                f" ."
            )
            == 0
        )
        assert os.system(f"docker run -t --rm dictaclass-test:{py_version}") == 0
    finally:
        os.system(f"docker image rm dictaclass-test:{py_version}")


@pytest.mark.skip("3.6 is not supported.")
@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_6():
    _test_all_python("3.6")


@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_7():
    _test_all_python("3.7")


@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_7_2():
    _test_all_python("3.7.2")


@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_8():
    _test_all_python("3.8")


@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_9():
    _test_all_python("3.9")


@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_10():
    _test_all_python("3.10")


@pytest.mark.skipif(in_docker, reason="DinDon't")
def test_all_python_3_11():
    _test_all_python("3.11")
