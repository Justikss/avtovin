
class SafeDict:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._copy(self._data[key])

    def __iter__(self):
        return iter(self._copy(self._data))

    def get(self, key, default=None):
        return self._copy(self._data.get(key, default))

    def _copy(self, item):
        if isinstance(item, dict):
            return {k: self._copy(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._copy(i) for i in item]
        return item
