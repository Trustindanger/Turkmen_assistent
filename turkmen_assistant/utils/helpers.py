"""
Вспомогательные функции для работы с языками.
Предоставляет утилиты для перевода и обработки текста.
"""

from typing import Dict, Optional


class LanguageHelper:
    """
    Утилиты для работы с языками и переводами.
    
    Предоставляет базовый функционал для простого перевода
    и обработки многоязычного текста.
    """
    
    # Базовый словарь для простого перевода
    _basic_dictionary = {
        'привет': {'tk': 'Salam', 'en': 'Hello'},
        'здравствуйте': {'tk': 'Salam', 'en': 'Hello'},
        'спасибо': {'tk': 'Sag boluň', 'en': 'Thank you'},
        'пока': {'tk': 'Hoş sag boluň', 'en': 'Goodbye'},
        'да': {'tk': 'Hawa', 'en': 'Yes'},
        'нет': {'tk': 'Ýok', 'en': 'No'},
        'хорошо': {'tk': 'Gowy', 'en': 'Good'},
        'плохо': {'tk': 'Erbet', 'en': 'Bad'},
        'помощь': {'tk': 'Kömek', 'en': 'Help'},
        'друг': {'tk': 'Dost', 'en': 'Friend'},
        'семья': {'tk': 'Maşgala', 'en': 'Family'},
        'работа': {'tk': 'Iş', 'en': 'Work'},
        'дом': {'tk': 'Öý', 'en': 'Home'},
        'вода': {'tk': 'Suw', 'en': 'Water'},
        'еда': {'tk': 'Iýmit', 'en': 'Food'},
        
        'hello': {'tk': 'Salam', 'ru': 'Здравствуйте'},
        'thank': {'tk': 'Sag boluň', 'ru': 'Спасибо'},
        'goodbye': {'tk': 'Hoş sag boluň', 'ru': 'До свидания'},
        'yes': {'tk': 'Hawa', 'ru': 'Да'},
        'no': {'tk': 'Ýok', 'ru': 'Нет'},
        'good': {'tk': 'Gowy', 'ru': 'Хорошо'},
        'bad': {'tk': 'Erbet', 'ru': 'Плохо'},
        'help': {'tk': 'Kömek', 'ru': 'Помощь'},
        'friend': {'tk': 'Dost', 'ru': 'Друг'},
        'family': {'tk': 'Maşgala', 'ru': 'Семья'},
        'work': {'tk': 'Iş', 'ru': 'Работа'},
        'home': {'tk': 'Öý', 'ru': 'Дом'},
        'water': {'tk': 'Suw', 'ru': 'Вода'},
        'food': {'tk': 'Iýmit', 'ru': 'Еда'},
        
        'salam': {'ru': 'Здравствуйте', 'en': 'Hello'},
        'sag': {'ru': 'Спасибо', 'en': 'Thank'},
        'how': {'ru': 'Как', 'en': 'How'},
        'nähili': {'ru': 'Какой', 'en': 'How'},
        'gowy': {'ru': 'Хорошо', 'en': 'Good'},
    }
    
    @classmethod
    def translate_simple(cls, text: str, from_lang: str, to_lang: str) -> str:
        """
        Выполнить простой перевод текста.
        
        Args:
            text: Текст для перевода
            from_lang: Исходный язык
            to_lang: Целевой язык
            
        Returns:
            Переведенный текст или оригинал если перевод не найден
        """
        if from_lang == to_lang:
            return text
        
        text_lower = text.lower().strip()
        
        # Прямой поиск в словаре
        if text_lower in cls._basic_dictionary:
            translations = cls._basic_dictionary[text_lower]
            if to_lang in translations:
                return translations[to_lang]
        
        # Поиск по словам
        words = text_lower.split()
        translated_words = []
        
        for word in words:
            if word in cls._basic_dictionary:
                translations = cls._basic_dictionary[word]
                if to_lang in translations:
                    translated_words.append(translations[to_lang])
                else:
                    translated_words.append(word)
            else:
                translated_words.append(word)
        
        result = ' '.join(translated_words)
        
        # Если ничего не изменилось, возвращаем оригинал
        if result == text:
            return f"[Перевод недоступен] {text}"
        
        return result
    
    @classmethod
    def detect_language(cls, text: str) -> Optional[str]:
        """
        Определить язык текста (базовая эвристика).
        
        Args:
            text: Текст для анализа
            
        Returns:
            Код языка ('tk', 'ru', 'en') или None
        """
        text_lower = text.lower()
        
        # Туркменские специфические символы и слова
        tk_markers = ['ň', 'ü', 'ö', 'ç', 'ş', 'ä', 'ý', 'salam', 'sag bol', 'nähili']
        for marker in tk_markers:
            if marker in text_lower:
                return 'tk'
        
        # Русские специфические символы
        ru_markers = ['привет', 'здравствуйте', 'спасибо', 'пока', 'хорошо']
        for marker in ru_markers:
            if marker in text_lower:
                return 'ru'
        
        # Английские маркеры
        en_markers = ['hello', 'thank', 'goodbye', 'please', 'how are']
        for marker in en_markers:
            if marker in text_lower:
                return 'en'
        
        return None
    
    @classmethod
    def normalize_text(cls, text: str) -> str:
        """
        Нормализовать текст (удалить лишние пробелы, привести к нижнему регистру).
        
        Args:
            text: Исходный текст
            
        Returns:
            Нормализованный текст
        """
        return ' '.join(text.lower().split())
    
    @classmethod
    def get_language_name(cls, lang_code: str) -> str:
        """
        Получить полное название языка по коду.
        
        Args:
            lang_code: Код языка ('tk', 'ru', 'en')
            
        Returns:
            Название языка
        """
        names = {
            'tk': 'Туркменский',
            'ru': 'Русский',
            'en': 'Английский'
        }
        return names.get(lang_code, 'Неизвестный')
