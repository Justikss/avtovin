class Pagination:
    def __init__(self, data, page_size, current_page: int = 0):
        self.data = data
        self.page_size = page_size
        self.current_page = current_page
        self.total_pages = max((len(data) + page_size - 1) // page_size, 1)  # Вычисление общего количества страниц, минимум 1 страница

    async def get_page(self, operation: str):
        print('current_page before operation: ', self.current_page)

        if operation == '-':
            self.current_page -= 1
        elif operation == '+':
            self.current_page += 1

        print('current_page after operation: ', self.current_page)
        ic(operation, self.data, self.current_page)
        if self.current_page < 1 or self.current_page > self.total_pages:
            # if self.total_pages > 1:
                # Если текущая страница вне диапазона и всего страниц больше одной
                # Переход на противоположный конец данных
            self.current_page = self.total_pages if self.current_page < 1 else 1
            # else:
            #     # Если только одна страница, возвращаем False
            #     return False

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        ic(self.current_page)
        return self.data[start_index:end_index]


    async def to_dict(self):
        # Возвращаем словарь, представляющий объект
        return {
            'data': self.data,
            'page_size': self.page_size,
            'current_page': self.current_page
            # 'total_pages': self.total_pages
        }

