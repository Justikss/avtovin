async def sort_objects_alphabetically(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj.name)
    return sorted_objects