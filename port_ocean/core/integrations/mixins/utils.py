from contextlib import contextmanager
from typing import Awaitable, Generator, Callable

from port_ocean.core.ocean_types import (
    ASYNC_GENERATOR_RESYNC_TYPE,
    RAW_RESULT,
)
from port_ocean.core.utils import validate_result
from port_ocean.exceptions.core import RawObjectValidationException, OceanAbortException


@contextmanager
def resync_error_handling() -> Generator[None, None, None]:
    try:
        yield
    except RawObjectValidationException as error:
        raise OceanAbortException(
            f"Failed to validate raw data for returned data from resync function, error: {error}"
        ) from error
    except StopAsyncIteration:
        raise
    except Exception as error:
        raise OceanAbortException(
            f"Failed to execute resync function, error: {error}"
        ) from error


async def resync_function_wrapper(
    fn: Callable[[str], Awaitable[RAW_RESULT]], kind: str
) -> RAW_RESULT:
    with resync_error_handling():
        results = await fn(kind)
        return validate_result(results)


async def resync_generator_wrapper(
    fn: Callable[[str], ASYNC_GENERATOR_RESYNC_TYPE], kind: str
) -> ASYNC_GENERATOR_RESYNC_TYPE:
    generator = fn(kind)
    errors = []
    try:
        while True:
            try:
                with resync_error_handling():
                    result = await anext(generator)
                    yield validate_result([result])[0]
            except OceanAbortException as error:
                errors.append(error)
    except StopAsyncIteration:
        if errors:
            raise ExceptionGroup(
                "At least one of the resync generator iterations failed", errors
            )
