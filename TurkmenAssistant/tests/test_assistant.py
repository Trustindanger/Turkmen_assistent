"""
Unit-тесты для Turkmen Assistant.
Тестирует основные компоненты системы.
"""

import unittest
import sys
from pathlib import Path

# Добавляем корневую директорию в path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from TurkmenAssistant.core.assistant import TurkmenAssistant
from TurkmenAssistant.data.phrases import PhraseDatabase
from TurkmenAssistant.utils.helpers import LanguageHelper


class TestTurkmenAssistant(unittest.TestCase):
    """Тесты для класса TurkmenAssistant."""
    
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.assistant = TurkmenAssistant()
    
    def test_initialization(self):
        """Тест инициализации ассистента."""
        self.assertEqual(self.assistant.language, 'ru')
        self.assertIsNotNone(self.assistant.phrase_db)
        self.assertIsNotNone(self.assistant.lang_helper)
    
    def test_greet_russian(self):
        """Тест приветствия на русском."""
        greeting = self.assistant.greet()
        self.assertIn('Здравствуйте', greeting)
    
    def test_greet_turkmen(self):
        """Тест приветствия на туркменском."""
        self.assistant.set_language('tk')
        greeting = self.assistant.greet()
        self.assertIn('Salam', greeting)
    
    def test_greet_english(self):
        """Тест приветствия на английском."""
        self.assistant.set_language('en')
        greeting = self.assistant.greet()
        self.assertIn('Hello', greeting)
    
    def test_set_language(self):
        """Тест установки языка."""
        self.assertTrue(self.assistant.set_language('tk'))
        self.assertEqual(self.assistant.language, 'tk')
        
        self.assertTrue(self.assistant.set_language('en'))
        self.assertEqual(self.assistant.language, 'en')
        
        self.assertFalse(self.assistant.set_language('de'))
    
    def test_process_request_greeting(self):
        """Тест обработки приветствия."""
        response = self.assistant.process_request('Привет')
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)
    
    def test_process_request_thanks(self):
        """Тест обработки благодарности."""
        response = self.assistant.process_request('Спасибо')
        self.assertIn('Пожалуйста', response)
    
    def test_conversation_history(self):
        """Тест истории диалога."""
        self.assistant.process_request('Привет')
        history = self.assistant.get_conversation_history()
        
        self.assertEqual(len(history), 2)  # запрос + ответ
        self.assertEqual(history[0]['role'], 'user')
        self.assertEqual(history[1]['role'], 'assistant')
    
    def test_clear_history(self):
        """Тест очистки истории."""
        self.assistant.process_request('Привет')
        self.assistant.clear_history()
        
        self.assertEqual(len(self.assistant.get_conversation_history()), 0)


class TestPhraseDatabase(unittest.TestCase):
    """Тесты для базы данных фраз."""
    
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.db = PhraseDatabase()
    
    def test_get_phrase_greeting(self):
        """Тест получения приветствия."""
        phrase = self.db.get_phrase('greetings', 'hello', 'ru')
        self.assertEqual(phrase, 'Здравствуйте')
        
        phrase = self.db.get_phrase('greetings', 'hello', 'tk')
        self.assertEqual(phrase, 'Salam')
    
    def test_get_phrase_not_found(self):
        """Тест получения несуществующей фразы."""
        phrase = self.db.get_phrase('nonexistent', 'key', 'ru')
        self.assertIsNone(phrase)
        
        phrase = self.db.get_phrase('greetings', 'nonexistent', 'ru')
        self.assertIsNone(phrase)
    
    def test_list_categories(self):
        """Тест списка категорий."""
        categories = self.db.get_categories()
        self.assertIn('greetings', categories)
        self.assertIn('courtesy', categories)
        self.assertIn('basics', categories)
    
    def test_add_phrase(self):
        """Тест добавления новой фразы."""
        new_translations = {
            'tk': 'Test',
            'ru': 'Тест',
            'en': 'Test'
        }
        result = self.db.add_phrase('test_category', 'test_key', new_translations)
        self.assertTrue(result)
        
        phrase = self.db.get_phrase('test_category', 'test_key', 'ru')
        self.assertEqual(phrase, 'Тест')
    
    def test_search_phrases(self):
        """Тест поиска фраз."""
        results = self.db.search_phrases('спасибо', 'ru')
        self.assertTrue(len(results) > 0)


class TestLanguageHelper(unittest.TestCase):
    """Тесты для вспомогательных функций языка."""
    
    def test_translate_simple_ru_to_tk(self):
        """Тест простого перевода с русского на туркменский."""
        translation = LanguageHelper.translate_simple('привет', 'ru', 'tk')
        self.assertEqual(translation, 'Salam')
    
    def test_translate_simple_ru_to_en(self):
        """Тест простого перевода с русского на английский."""
        translation = LanguageHelper.translate_simple('спасибо', 'ru', 'en')
        self.assertEqual(translation, 'Thank you')
    
    def test_translate_same_language(self):
        """Тест перевода на тот же язык."""
        translation = LanguageHelper.translate_simple('привет', 'ru', 'ru')
        self.assertEqual(translation, 'привет')
    
    def test_detect_language_turkmen(self):
        """Тест определения туркменского языка."""
        lang = LanguageHelper.detect_language('Salam, nähili?')
        self.assertEqual(lang, 'tk')
    
    def test_detect_language_russian(self):
        """Тест определения русского языка."""
        lang = LanguageHelper.detect_language('Привет, как дела?')
        self.assertEqual(lang, 'ru')
    
    def test_detect_language_english(self):
        """Тест определения английского языка."""
        lang = LanguageHelper.detect_language('Hello, how are you?')
        self.assertEqual(lang, 'en')
    
    def test_normalize_text(self):
        """Тест нормализации текста."""
        normalized = LanguageHelper.normalize_text('  Привет   Мир  ')
        self.assertEqual(normalized, 'привет мир')
    
    def test_get_language_name(self):
        """Тест получения названия языка."""
        self.assertEqual(LanguageHelper.get_language_name('tk'), 'Туркменский')
        self.assertEqual(LanguageHelper.get_language_name('ru'), 'Русский')
        self.assertEqual(LanguageHelper.get_language_name('en'), 'Английский')


if __name__ == '__main__':
    unittest.main()
