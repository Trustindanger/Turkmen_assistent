#!/usr/bin/env python3
"""
Главный файл запуска Turkmen Assistant.
Демонстрирует возможности ассистента в интерактивном режиме.
"""

import sys
from pathlib import Path

# Добавляем корневую директорию в path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from TurkmenAssistant.core.assistant import TurkmenAssistant
from TurkmenAssistant.data.phrases import PhraseDatabase
from TurkmenAssistant.utils.helpers import LanguageHelper


def print_welcome():
    """Вывести приветственное сообщение."""
    print("=" * 60)
    print("  TURKMEN ASSISTANT - Профессиональный ассистент")
    print("  Поддержка языков: Туркменский, Русский, English")
    print("=" * 60)
    print()


def print_menu():
    """Вывести меню команд."""
    print("\n--- Доступные команды ---")
    print("  /lang <tk|ru|en>  - Изменить язык")
    print("  /phrases          - Показать все фразы")
    print("  /translate <текст> <from> <to> - Перевести текст")
    print("  /history          - Показать историю диалога")
    print("  /clear            - Очистить историю")
    print("  /help             - Показать эту справку")
    print("  /exit             - Выйти из программы")
    print("-----------------------\n")


def demo_mode(assistant: TurkmenAssistant):
    """Запустить демонстрационный режим."""
    print("\n=== ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ ===\n")
    
    # Приветствия на разных языках
    print("1. Приветствия на разных языках:")
    for lang in ['tk', 'ru', 'en']:
        assistant.set_language(lang)
        print(f"   [{lang}] {assistant.greet()}")
    
    # Получение фраз из базы
    print("\n2. Фразы из базы данных:")
    db = PhraseDatabase()
    categories = db.get_categories()
    for cat in categories[:2]:  # Первые две категории
        print(f"   Категория: {cat}")
        phrases = db.list_phrases(cat)
        for key, translations in phrases[cat].items():
            print(f"      - {key}: {translations}")
    
    # Простой перевод
    print("\n3. Примеры перевода:")
    helper = LanguageHelper()
    examples = [
        ('привет', 'ru', 'tk'),
        ('thank you', 'en', 'ru'),
        ('Salam', 'tk', 'en'),
    ]
    for text, from_lang, to_lang in examples:
        translation = helper.translate_simple(text, from_lang, to_lang)
        print(f"   {text} ({from_lang}) → {translation} ({to_lang})")
    
    # Обработка запросов
    print("\n4. Обработка запросов:")
    assistant.set_language('ru')
    requests = ['Привет', 'Спасибо', 'Какие языки ты знаешь?']
    for req in requests:
        response = assistant.process_request(req)
        print(f"   Запрос: '{req}'")
        print(f"   Ответ: '{response}'\n")
    
    print("=== ДЕМО ЗАВЕРШЕНО ===\n")


def interactive_mode(assistant: TurkmenAssistant):
    """Запустить интерактивный режим."""
    print_welcome()
    print_menu()
    
    # Начальное приветствие
    print(assistant.greet())
    
    while True:
        try:
            user_input = input("\nВы: ").strip()
            
            if not user_input:
                continue
            
            # Обработка команд
            if user_input.startswith('/'):
                command = user_input.lower().split()[0]
                
                if command == '/exit' or command == '/quit':
                    print("\nHoş sag boluň! До свидания! Goodbye!")
                    break
                
                elif command == '/help':
                    print_menu()
                
                elif command == '/lang':
                    parts = user_input.split()
                    if len(parts) >= 2:
                        new_lang = parts[1].lower()
                        if assistant.set_language(new_lang):
                            lang_names = {'tk': 'Туркменский', 'ru': 'Русский', 'en': 'English'}
                            print(f"Язык изменён на: {lang_names.get(new_lang, new_lang)}")
                        else:
                            print("Ошибка: неподдерживаемый язык. Используйте tk, ru или en.")
                    else:
                        print("Использование: /lang <tk|ru|en>")
                
                elif command == '/phrases':
                    db = PhraseDatabase()
                    categories = db.get_categories()
                    print(f"\nКатегории фраз: {', '.join(categories)}")
                    for cat in categories:
                        print(f"\n[{cat}]")
                        phrases = db.list_phrases(cat)
                        for key, translations in phrases[cat].items():
                            print(f"  {key}: {translations}")
                
                elif command == '/translate':
                    parts = user_input.split(maxsplit=3)
                    if len(parts) >= 4:
                        text = parts[1]
                        from_lang = parts[2].lower()
                        to_lang = parts[3].lower()
                        result = LanguageHelper.translate_simple(text, from_lang, to_lang)
                        print(f"Перевод: {result}")
                    else:
                        print("Использование: /translate <текст> <from_lang> <to_lang>")
                
                elif command == '/history':
                    history = assistant.get_conversation_history()
                    if history:
                        print("\n--- История диалога ---")
                        for msg in history[-10:]:  # Последние 10 сообщений
                            role = "Вы" if msg['role'] == 'user' else "Ассистент"
                            print(f"{role}: {msg['content']}")
                    else:
                        print("История пуста.")
                
                elif command == '/clear':
                    assistant.clear_history()
                    print("История очищена.")
                
                else:
                    print(f"Неизвестная команда: {command}. Введите /help для справки.")
            
            else:
                # Обычный запрос
                response = assistant.process_request(user_input)
                print(f"Ассистент: {response}")
        
        except KeyboardInterrupt:
            print("\n\nHoş sag boluň! До свидания!")
            break
        except EOFError:
            print("\n\nHoş sag boluň! До свидания!")
            break


def main():
    """Основная функция запуска."""
    assistant = TurkmenAssistant(default_language='ru')
    
    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == '--demo':
            demo_mode(assistant)
            return
        elif sys.argv[1] == '--test':
            # Быстрый тест
            print("Тестирование...")
            print(f"Приветствие: {assistant.greet()}")
            print(f"Обработка 'Привет': {assistant.process_request('Привет')}")
            return
    
    # Интерактивный режим по умолчанию
    interactive_mode(assistant)


if __name__ == '__main__':
    main()
