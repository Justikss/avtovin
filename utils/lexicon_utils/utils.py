class BaseLexiconClass:
    def __init__(self, *args, **kwargs):
        # Инициализируем все атрибуты
        for key, value in self.__dict__.items():
            setattr(self, key, value)