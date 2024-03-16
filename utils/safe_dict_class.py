import contextvars
import hashlib
import json
import traceback

from icecream import ic

current_language = contextvars.ContextVar('current_language', default='ru')

# ic.disable()

class SafeDict:
    def __init__(self, data, language=current_language.get()):
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
            return self._copy(self._data[language])

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


class SmartGetAttrMeta(type):
    def __getattr__(cls, item):
        # Создаём временный экземпляр для единоразовой выдачи атрибута
        temp_instance = cls()
        return getattr(temp_instance, item)


import threading

# _thread_locals = threading.local()

# class SmartGetattr:
    # Хранилище для атрибутов всех экземпляров
    # _global_attrs = {}
    #
    # def __getattribute__(self, item):
    #     if hasattr(_thread_locals, 'in_getattribute') and _thread_locals.in_getattribute:
    #         return object.__getattribute__(self, item)
    #
    #     _thread_locals.in_getattribute = True
    #     try:
    #         # Создаем новый экземпляр класса
    #         instance = object.__getattribute__(self, '__class__')()
    #         # Инициализируем его атрибуты из глобального хранилища
    #         instance.__dict__.update(SmartGetattr._global_attrs)
    #         # Возвращаем значение атрибута
    #         return getattr(instance, item)
    #     finally:
    #         _thread_locals.in_getattribute = False
    #
    # def __setattr__(self, key, value):
    #     # Обновляем значение в глобальном хранилище
    #     SmartGetattr._global_attrs[key] = value
    #     # Устанавливаем значение атрибута напрямую для текущего экземпляра
    #     object.__setattr__(self, key, value)