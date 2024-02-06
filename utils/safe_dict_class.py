import contextvars
import hashlib
import json
import traceback

from icecream import ic

current_language = contextvars.ContextVar('current_language', default='ru')

# ic.disable()

class SafeDict:
    def __init__(self, data, language='ru'):
        self._data = data
        self.language = language

    async def set_language(self, language):
        # Здесь могут быть асинхронные операции, если они нужны
        self.language = language

    def __getitem__(self, key):
        # if isinstance(self._copy(self._data[self.language]), str):
        #     ic(self._copy(self._data[self.language]), key)
        # ic()
        # ic(self.language)
        # ic(key)
        # ic(self._data.keys(), len(self._data['ru']), len(self._data['uz']))
        # ic(self._data[self.language][key])
        language = current_language.get()
        ic(language, key)
        return self._copy(self._data[language][key])

    def __iter__(self):
        language = current_language.get()
        return iter(self._copy(self._data[language]))

    def get(self, key, default=None):
        language = current_language.get()

        return self._copy(self._data[language].get(key, default))

    def __repr__(self):
        language = current_language.get()
        output_value = self._copy(self._data[language])
        # ic(output_value, type(output_value))
        if isinstance(output_value, str):
            return output_value
        return None

    def __str__(self):
        language = current_language.get()
        output_value = self._copy(self._data[language])
        ic(output_value)
        # ic()
        if isinstance(output_value, str):
            return self._copy(self._data[self.language])

    def __eq__(self, other):
        if isinstance(other, SafeDict):
            return self._data == other._data
        return False

    def __hash__(self):
        # Создаем хеш из строкового представления отсортированного словаря
        sorted_data_str = str(sorted(self._data.items()))
        return int(hashlib.md5(sorted_data_str.encode()).hexdigest(), 16)

    def _copy(self, item):
        if isinstance(item, dict):
            return {k: self._copy(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._copy(i) for i in item]
        # ic(item, type(item))
        return item

import threading

_thread_locals = threading.local()

class SmartGetattr:
    def __getattribute__(self, item):
        if hasattr(_thread_locals, 'in_getattribute') and _thread_locals.in_getattribute:
            return object.__getattribute__(self, item)

        _thread_locals.in_getattribute = True
        try:
            instance = object.__getattribute__(self, '__class__')()
            return getattr(instance, item)
        finally:
            _thread_locals.in_getattribute = False

class ReinitOnAttrAccess:
    def __getattribute__(self, name):
        # Чтобы предотвратить рекурсию при обращении к __class__ и другим "внутренним" атрибутам,
        # обрабатываем их особым образом.
        if name.startswith('__') and name.endswith('__'):
            return object.__getattribute__(self, name)

        # Создаем новый экземпляр класса.
        new_instance = object.__getattribute__(self, '__class__')()

        # Для безопасности используйте object.__getattribute__ для получения атрибута из нового экземпляра,
        # чтобы избежать возможной рекурсии через переопределенный __getattribute__.
        return object.__getattribute__(new_instance, name)