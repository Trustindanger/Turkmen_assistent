"""
Основной класс TurkmenAssistant - ядро системы.
Обрабатывает запросы пользователя, управляет диалогами и предоставляет ответы.
"""

from typing import Optional, Dict, List
from ..data.phrases import PhraseDatabase
from ..utils.helpers import LanguageHelper


class TurkmenAssistant:
    """
    Профессиональный ассистент с поддержкой туркменского языка.
    
    Attributes:
        language (str): Текущий язык общения ('tk', 'ru', 'en')
        phrase_db (PhraseDatabase): База данных фраз
        lang_helper (LanguageHelper): Утилиты для работы с языками
    """
    
    SUPPORTED_LANGUAGES = ['tk', 'ru', 'en']
    
    def __init__(self, default_language: str = 'ru'):
        """
        Инициализация ассистента.
        
        Args:
            default_language: Язык по умолчанию ('tk', 'ru' или 'en')
        """
        if default_language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Неподдерживаемый язык: {default_language}")
        
        self.language = default_language
        self.phrase_db = PhraseDatabase()
        self.lang_helper = LanguageHelper()
        self._conversation_history: List[Dict[str, str]] = []
    
    def greet(self) -> str:
        """
        Получить приветствие на текущем языке.
        
        Returns:
            Строка с приветствием
        """
        greetings = {
            'tk': 'Salam! Men Türkmen kömekçisi. Size nähili kömek edip bilerin?',
            'ru': 'Здравствуйте! Я туркменский ассистент. Чем могу вам помочь?',
            'en': 'Hello! I am a Turkmen assistant. How can I help you?'
        }
        return greetings.get(self.language, greetings['ru'])
    
    def set_language(self, language: str) -> bool:
        """
        Установить язык общения.
        
        Args:
            language: Код языка ('tk', 'ru', 'en')
            
        Returns:
            True если язык установлен успешно, иначе False
        """
        if language in self.SUPPORTED_LANGUAGES:
            self.language = language
            return True
        return False
    
    def get_phrase(self, category: str, key: str) -> Optional[str]:
        """
        Получить фразу из базы данных.
        
        Args:
            category: Категория фразы
            key: Ключ фразы
            
        Returns:
            Фраза на текущем языке или None если не найдена
        """
        return self.phrase_db.get_phrase(category, key, self.language)
    
    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Перевести текст между поддерживаемыми языками.
        
        Args:
            text: Текст для перевода
            from_lang: Исходный язык
            to_lang: Целевой язык
            
        Returns:
            Переведенный текст
        """
        return self.lang_helper.translate_simple(text, from_lang, to_lang)
    
    def process_request(self, request: str) -> str:
        """
        Обработать запрос пользователя.
        
        Args:
            request: Текст запроса от пользователя
            
        Returns:
            Ответ ассистента
        """
        request_lower = request.lower().strip()
        
        # Сохраняем в историю
        self._conversation_history.append({
            'role': 'user',
            'content': request
        })
        
        # Простая логика обработки
        if any(word in request_lower for word in ['салам', 'salam', 'привет', 'hello']):
            response = self.greet()
        elif any(word in request_lower for word in ['саг бол', 'спасибо', 'thank']):
            response = self._get_thanks_response()
        elif any(word in request_lower for word in ['язык', 'dil', 'language']):
            response = self._get_language_info()
        else:
            response = self._get_default_response()
        
        # Сохраняем ответ в историю
        self._conversation_history.append({
            'role': 'assistant',
            'content': response
        })
        
        return response
    
    def _get_thanks_response(self) -> str:
        """Получить ответ на благодарность."""
        responses = {
            'tk': 'Sag boluň! Her wagt kömege taýýar.',
            'ru': 'Пожалуйста! Всегда готов помочь.',
            'en': "You're welcome! Always ready to help."
        }
        return responses.get(self.language, responses['ru'])
    
    def _get_language_info(self) -> str:
        """Получить информацию о поддерживаемых языках."""
        info = {
            'tk': 'Men türkmen, rus we iňlis dillerinde gürleşip bilerin.',
            'ru': 'Я могу общаться на туркменском, русском и английском языках.',
            'en': 'I can communicate in Turkmen, Russian and English.'
        }
        return info.get(self.language, info['ru'])
    
    def _get_default_response(self) -> str:
        """Получить ответ по умолчанию."""
        responses = {
            'tk': 'Bagyşlaň, men düşünmedim. Başga soragyňyz barmy?',
            'ru': 'Извините, я не понял. Есть ли у вас другой вопрос?',
            'en': "Sorry, I didn't understand. Do you have another question?"
        }
        return responses.get(self.language, responses['ru'])
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Получить историю диалога.
        
        Returns:
            Список сообщений диалога
        """
        return self._conversation_history.copy()
    
    def clear_history(self) -> None:
        """Очистить историю диалога."""
        self._conversation_history.clear()
    
    def list_phrases(self, category: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """
        Получить список всех фраз или фраз определенной категории.
        
        Args:
            category: Категория фраз (опционально)
            
        Returns:
            Словарь с фразами
        """
        return self.phrase_db.list_phrases(category)
