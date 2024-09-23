from utils.misc import is_access_denied_exception
from typing import Optional, Dict, Any


class MockException(Exception):
    def __init__(self, response: Optional[Dict[str, Any]]) -> None:
        self.response = response


def test_access_denied_exception_with_response() -> None:
    e = MockException(response={"Error": {"Code": "AccessDenied"}})
    assert is_access_denied_exception(e) is True


def test_access_denied_exception_without_response() -> None:
    e = MockException(response=None)
    assert is_access_denied_exception(e) is False


def test_access_denied_exception_with_other_error() -> None:
    e = MockException(response={"Error": {"Code": "SomeOtherError"}})
    assert is_access_denied_exception(e) is False


def test_access_denied_exception_no_response_attribute() -> None:
    e = Exception("Test exception")
    assert is_access_denied_exception(e) is False
