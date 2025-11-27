from app.db.mongo import schema
from typing import Any
import inspect


def set_user_id_all(resume: dict, user_id: str) -> dict:
    """
    Auto-detects dict sections and list-of-dict sections,
    and sets user_id everywhere it appears.
    """

    for key, value in resume.items():

        # Case 1: Value is a dict (profile)
        if isinstance(value, dict):
            value["user_id"] = user_id

        # Case 2: Value is a list (education, work_experience)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    item["user_id"] = user_id

    return resume


async def get_if_awaitable(obj:Any) -> bool:
    ''' Check if an object is awaitable (i.e., a coroutine) '''
    if inspect.isawaitable(obj):
        return await obj
    return obj