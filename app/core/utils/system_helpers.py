''' Utility functions for system / state operations '''
import inspect
from typing import Any


async def get_if_awaitable(obj:Any) -> bool:
    ''' Check if an object is awaitable (i.e., a coroutine) '''
    if inspect.isawaitable(obj):
        return await obj
    return obj