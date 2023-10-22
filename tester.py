from utils.Lexicon import LEXICON

from googletrans import Translator


def optimize_and_translate_lexicon(lexicon, max_length=4000):
    translator = YandexTranslator(
        'YOUR_YANDEX_TRANSLATE_API_KEY')  # Замените YOUR_YANDEX_TRANSLATE_API_KEY на свой ключ

    # Объединяем значения словарей в одну строку
    combined_values = ' '.join(
        [' '.join(map(str, val.values())) if isinstance(val, dict) else str(val) for val in lexicon.values() if
         isinstance(val, (str, int))])

    # Разбиваем строку на части максимальной длины
    parts = [combined_values[i:i + max_length] for i in range(0, len(combined_values), max_length)]

    translated_lexicon = {}
    for part in parts:
        translation = translator.translate(part, 'ru-uz')

        # Ищем соответствие переводов значениям
        for key, value in lexicon.items():
            if key in translated_lexicon:
                continue  # Пропускаем уже переведенные значения
            if isinstance(value, dict):
                # Если значение - словарь, ищем перевод внутри словаря
                translated_value = {}
                for sub_key, sub_value in value.items():
                    if sub_key in translated_lexicon:
                        translated_value[sub_key] = translated_lexicon[sub_key]
                    else:
                        sub_translation = translator.translate(sub_value, 'ru-uz')
                        translated_value[sub_key] = sub_translation
                translated_lexicon[key] = translated_value
            elif isinstance(value, (str, int)):
                # Иначе просто присваиваем перевод значению
                translated_lexicon[key] = translation

    return translated_lexicon


# Получаем переведенный LEXICON на узбекский язык
uzbek_lexicon = optimize_and_translate_lexicon(LEXICON)

# Ваш новый LEXICON на узбекском языке
print(uzbek_lexicon)