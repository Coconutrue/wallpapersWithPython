import json
import os
import sys


class Cache:
    """Класс для кэширования настроек приложения в JSON файле"""

    def __init__(self):
        # Путь к файлу кэша (настройки хранятся в resources/cache/settings.json)
        self.filename = 'resources/cache/settings.json'
        # Проверяем существует ли файл, если нет - создаем
        self.checkExists()
        # Содержимое файла в виде строки
        self.content = False
        # Кэш в виде словаря Python
        self.cache = False
        # Загружаем данные из файла
        self.read()

    def checkExists(self):
        """Проверяет существование файла кэша, создает при отсутствии"""
        if not os.path.exists(self.filename):
            # Создаем пустой кэш с настройками по умолчанию
            self.createCache()
            # Сохраняем в файл
            self.save()

    def toString(self):
        """Преобразует словарь кэша в JSON строку с отступами для читаемости"""
        # indent=4 - красивое форматирование с отступами
        # ensure_ascii=False - поддержка русских символов
        return json.dumps(self.cache, indent=4, ensure_ascii=False)

    def writeToFile(self, content):
        """Записывает содержимое в файл кэша"""
        # Открываем файл в режиме записи с кодировкой UTF-8
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def save(self):
        """Сохраняет текущее состояние кэша в файл"""
        self.writeToFile(self.toString())

    def readFile(self):
        """Читает содержимое файла кэша в переменную content"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def read(self, i=0):
        """
        Загружает и парсит JSON из файла кэша
        i - счетчик попыток (для предотвращения бесконечной рекурсии)
        """
        if i > 1:
            # Если после 2 попыток не удалось прочитать - завершаем программу
            print('Error read cache file.')
            sys.exit()

        self.readFile()
        try:
            # Пытаемся преобразовать JSON строку в словарь
            self.cache = json.loads(self.content)
        except:
            # Если файл поврежден - создаем новый кэш
            self.createCache()
            self.save()
            # Рекурсивно пытаемся прочитать заново
            return self.read(i + 1)

    def createCache(self):
        """Создает структуру кэша со значениями по умолчанию"""
        self.cache = {
            'version': 'v1.0',  # Версия формата кэша
            # Другие настройки будут добавляться динамически через put()
        }

    def get(self, index, default):
        """
        Получает значение из кэша по ключу
        index - ключ (название настройки)
        default - значение по умолчанию, если ключ не найден
        """
        if index in self.cache:
            return self.cache[index]
        # Если ключа нет - сохраняем значение по умолчанию и возвращаем его
        self.put(index, default)
        return default

    def put(self, index, body):
        """
        Сохраняет значение в кэш по ключу
        index - ключ (название настройки)
        body - значение для сохранения
        """
        self.cache[index] = body
        # Автоматически сохраняем изменения в файл
        self.save()