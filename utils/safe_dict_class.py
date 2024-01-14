import traceback


class SafeDict:
    def __init__(self, data, language='ru'):
        self._data = data
        self.language = language

    async def set_language(self, language):
        # Здесь могут быть асинхронные операции, если они нужны
        self.language = language

    def __getitem__(self, key):
        if isinstance(self._copy(self._data[self.language]), str):
            ic(self._copy(self._data[self.language]), key)
        ic()
        ic(self.language)
        ic(self._data.keys(), len(self._data['ru']), len(self._data['uz']))
        ic(self._data[self.language][key])
        return self._copy(self._data[self.language][key])

    def __iter__(self):
        return iter(self._copy(self._data[self.language]))

    def get(self, key, default=None):
        return self._copy(self._data[self.language].get(key, default))

    def __repr__(self):
        output_value = self._copy(self._data[self.language])
        ic(output_value)
        if isinstance(output_value, str):
            return self._copy(self._data[self.language])

    def __str__(self):
        output_value = self._copy(self._data[self.language])
        ic(output_value)
        ic()
        if isinstance(output_value, str):
            return self._copy(self._data[self.language])

    def _copy(self, item):
        if isinstance(item, dict):
            return {k: self._copy(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._copy(i) for i in item]
        # ic(item, type(item))
        return item