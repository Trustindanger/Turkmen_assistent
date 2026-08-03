#!/usr/bin/env python3
"""
Turkmen Assistant - Простой ассистент с поддержкой туркменского языка
"""

class TurkmenAssistant:
    """Базовый класс ассистента для туркменского языка"""
    
    def __init__(self):
        self.greetings = {
            'ru': 'Здравствуйте! Я туркменский ассистент.',
            'tk': 'Salam! Men türkmen kömekçisi.',
            'en': 'Hello! I am a Turkmen assistant.'
        }
        
        self.phrases = {
            'hello': {'tk': 'Salam', 'ru': 'Здравствуйте', 'en': 'Hello'},
            'thank_you': {'tk': 'Sag boluň', 'ru': 'Спасибо', 'en': 'Thank you'},
            'goodbye': {'tk': 'Hoş sagadyň', 'ru': 'До свидания', 'en': 'Goodbye'},
            'how_are_you': {'tk': 'Nähili?', 'ru': 'Как дела?', 'en': 'How are you?'}
        }
    
    def greet(self, language='ru'):
        """Приветствие пользователя"""
        return self.greetings.get(language, self.greetings['en'])
    
    def get_phrase(self, phrase_key, language='tk'):
        """Получение фразы на указанном языке"""
        if phrase_key in self.phrases:
            return self.phrases[phrase_key].get(language, 'Phrase not available')
        return 'Unknown phrase'
    
    def translate_basic(self, text, from_lang='en', to_lang='tk'):
        """Базовый перевод простых фраз"""
        for key, translations in self.phrases.items():
            if translations.get(from_lang) == text:
                return translations.get(to_lang, text)
        return text  # Возвращаем оригинал, если перевод не найден
    
    def list_phrases(self, language='tk'):
        """Список всех доступных фраз на указанном языке"""
        result = []
        for key, translations in self.phrases.items():
            result.append(f"{key}: {translations.get(language, 'N/A')}")
        return result


def main():
    """Основная функция демонстрации"""
    assistant = TurkmenAssistant()
    
    print("=" * 50)
    print("Turkmen Assistant - Демо версия")
    print("=" * 50)
    
    # Приветствия на разных языках
    print("\n📢 Приветствия:")
    for lang in ['ru', 'tk', 'en']:
        print(f"  {lang}: {assistant.greet(lang)}")
    
    # Примеры фраз на туркменском
    print("\n📚 Основные фразы (туркменский):")
    for phrase in assistant.list_phrases('tk'):
        print(f"  {phrase}")
    
    # Демонстрация перевода
    print("\n🔄 Примеры перевода:")
    examples = [
        ('Hello', 'en', 'tk'),
        ('Спасибо', 'ru', 'tk'),
        ('Sag boluň', 'tk', 'ru')
    ]
    
    for text, from_lang, to_lang in examples:
        translated = assistant.translate_basic(text, from_lang, to_lang)
        print(f"  {text} ({from_lang}) → {translated} ({to_lang})")
    
    print("\n" + "=" * 50)
    print("Демо завершено!")
    print("=" * 50)


if __name__ == '__main__':
    main()
