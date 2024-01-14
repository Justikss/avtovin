import pymtl
import pymt
def main():
    # Инициализируем библиотеку PyMTL
    pymtl.init()

    # Задаем исходный язык и целевой язык
    src_lang = "ru"
    tgt_lang = "uz"

    # Переводим слово "привет"
    translation = pymtl.translate(src_lang, tgt_lang, "привет")

    # Печатаем перевод
    print(translation)

if __name__ == "__main__":
    main()