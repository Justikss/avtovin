from typing import Optional


async def one_element_in_object(element: Optional[list]):
    if isinstance(element, list) and len(element) == 1:
        return element[0]
    else:
        return element