def display_history_page(history_stack, current_page, command):
    items_per_page = 3  # Количество элементов на каждой странице

    if not history_stack:
        print("История запросов пуста.")
        return

    total_pages = len(history_stack) // items_per_page
    if len(history_stack) % items_per_page != 0:
        total_pages += 1

    if command == "вперед":
        if current_page < total_pages:
            current_page += 1
    elif command == "назад":
        if current_page > 1:
            current_page -= 1

    start_index = (current_page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(history_stack))

    if start_index < end_index:
        print(f"Страница {current_page} из {total_pages}:")
        for i in range(start_index, end_index):
            print(history_stack[i])

    return current_page


# Пример использования функции
history = ["Запрос 1", "Запрос 2", "Запрос 3", "Запрос 4", "Запрос 5", "Запрос 6"]
current_page = 1

while True:
    print("-" * 20)
    print("Введите команду ('вперед' или 'назад'):")
    command = input()

    if command in ["вперед", "назад"]:
        current_page = display_history_page(history, current_page, command)
    else:
        print("Неверная команда. Введите 'вперед' или 'назад'.")
