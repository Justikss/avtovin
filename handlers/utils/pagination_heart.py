class Pagination:
    def __init__(self, data, page_size, current_page: int = 0):
        self.data = data
        self.page_size = page_size
        self.current_page = current_page
        self.total_pages = max((len(data) + page_size - 1) // page_size, 1)  # Вычисление общего количества страниц, минимум 1 страница

    async def get_page(self, operation: str):
        print('current_page 1 ', operation, self.current_page)
        if operation == '-':
            self.current_page -= 1
        elif operation == '+':
            self.current_page += 1
        print('current_page 2 ', operation, self.current_page)
        if not (1 <= self.current_page <= self.total_pages):
            # Если номер страницы вне допустимого диапазона, возвращаем False
            return False

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        # self.current_page += self.page_size
        return self.data[start_index:end_index]


    async def to_dict(self):
        # Возвращаем словарь, представляющий объект
        return {
            'data': self.data,
            'page_size': self.page_size,
            'current_page': self.current_page
            # 'total_pages': self.total_pages
        }

