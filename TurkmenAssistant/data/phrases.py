"""
База данных фраз для Turkmen Assistant.
Содержит многоязычные фразы для различных категорий.
"""

from typing import Optional, Dict


class PhraseDatabase:
    """
    База данных многоязычных фраз.
    
    Хранит фразы в структурированном виде по категориям
    с поддержкой туркменского, русского и английского языков.
    """
    
    def __init__(self):
        """Инициализация базы данных фраз."""
        self._phrases = self._load_phrases()
    
    def _load_phrases(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Загрузить фразы в базу данных.
        
        Returns:
            Словарь с фразами по категориям
        """
        return {
            'greetings': {
                'hello': {
                    'tk': 'Salam',
                    'ru': 'Здравствуйте',
                    'en': 'Hello'
                },
                'good_morning': {
                    'tk': 'Haýyrly ertir',
                    'ru': 'Доброе утро',
                    'en': 'Good morning'
                },
                'good_evening': {
                    'tk': 'Haýyrly agşam',
                    'ru': 'Добрый вечер',
                    'en': 'Good evening'
                },
                'how_are_you': {
                    'tk': 'Işiňiz nähili?',
                    'ru': 'Как ваши дела?',
                    'en': 'How are you?'
                }
            },
            'courtesy': {
                'thank_you': {
                    'tk': 'Sag boluň',
                    'ru': 'Спасибо',
                    'en': 'Thank you'
                },
                'please': {
                    'tk': 'Haýyş',
                    'ru': 'Пожалуйста (просьба)',
                    'en': 'Please'
                },
                'you_are_welcome': {
                    'tk': 'Hiç zat däl',
                    'ru': 'Пожалуйста (ответ)',
                    'en': "You're welcome"
                },
                'sorry': {
                    'tk': 'Bagyşlaň',
                    'ru': 'Извините',
                    'en': 'Sorry'
                }
            },
            'basics': {
                'yes': {
                    'tk': 'Hawa',
                    'ru': 'Да',
                    'en': 'Yes'
                },
                'no': {
                    'tk': 'Ýok',
                    'ru': 'Нет',
                    'en': 'No'
                },
                'goodbye': {
                    'tk': 'Hoş sag boluň',
                    'ru': 'До свидания',
                    'en': 'Goodbye'
                },
                'i_dont_understand': {
                    'tk': 'Men düşünmedim',
                    'ru': 'Я не понимаю',
                    'en': "I don't understand"
                }
            },
            'help': {
                'help_me': {
                    'tk': 'Kömek ediň',
                    'ru': 'Помогите мне',
                    'en': 'Help me'
                },
                'what_is_your_name': {
                    'tk': 'Adyňyz näme?',
                    'ru': 'Как вас зовут?',
                    'en': 'What is your name?'
                },
                'my_name_is': {
                    'tk': 'Meniň adym...',
                    'ru': 'Меня зовут...',
                    'en': 'My name is...'
                }
            }
        }
    
    def get_phrase(self, category: str, key: str, language: str) -> Optional[str]:
        """
        Получить фразу по категории и ключу.
        
        Args:
            category: Категория фразы
            key: Ключ фразы
            language: Код языка ('tk', 'ru', 'en')
            
        Returns:
            Фраза на указанном языке или None если не найдена
        """
        if category not in self._phrases:
            return None
        
        if key not in self._phrases[category]:
            return None
        
        if language not in self._phrases[category][key]:
            return None
        
        return self._phrases[category][key][language]
    
    def list_phrases(self, category: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Получить список всех фраз или фраз определенной категории.
        
        Args:
            category: Категория фраз (опционально)
            
        Returns:
            Словарь с фразами
        """
        if category is None:
            return self._phrases.copy()
        
        if category in self._phrases:
            return {category: self._phrases[category].copy()}
        
        return {}
    
    def get_categories(self) -> list:
        """
        Получить список всех категорий.
        
        Returns:
            Список названий категорий
        """
        return list(self._phrases.keys())
    
    def add_phrase(self, category: str, key: str, translations: Dict[str, str]) -> bool:
        """
        Добавить новую фразу в базу данных.
        
        Args:
            category: Категория фразы
            key: Ключ фразы
            translations: Словарь переводов {язык: фраза}
            
        Returns:
            True если фраза добавлена успешно
        """
        if category not in self._phrases:
            self._phrases[category] = {}
        
        self._phrases[category][key] = translations
        return True
    
    def search_phrases(self, search_term: str, language: str = 'ru') -> Dict[str, Dict[str, str]]:
        """
        Поиск фраз по содержимому.
        
        Args:
            search_term: Строка для поиска
            language: Язык для поиска
            
        Returns:
            Словарь с найденными фразами
        """
        results = {}
        search_lower = search_term.lower()
        
        for category, phrases in self._phrases.items():
            for key, translations in phrases.items():
                if language in translations and search_lower in translations[language].lower():
                    if category not in results:
                        results[category] = {}
                    results[category][key] = translations
        
        return results
