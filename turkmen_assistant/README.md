# Turkmen Assistant

Профессиональный многоязычный ассистент с поддержкой туркменского, русского и английского языков.

## 📋 Описание

Turkmen Assistant — это модульная Python-библиотека, предоставляющая функционал для:
- Многоязычного общения (туркменский, русский, английский)
- Перевода базовых фраз
- Распознавания намерений пользователя
- Ведения истории диалога
- Работы с базой данных фраз по категориям

## 🏗️ Структура проекта

```
turkmen_assistant/
├── __init__.py           # Основной пакет
├── main.py               # Точка входа и CLI интерфейс
├── core/
│   ├── __init__.py
│   └── assistant.py      # Основной класс TurkmenAssistant
├── data/
│   ├── __init__.py
│   └── phrases.py        # База данных фраз
├── utils/
│   ├── __init__.py
│   └── helpers.py        # Вспомогательные функции
└── tests/
    ├── __init__.py
    └── test_assistant.py # Unit-тесты
```

## 🚀 Быстрый старт

### Установка

Клонирование репозитория:
```bash
git clone <repository-url>
cd turkmen_assistant
```

### Запуск демонстрации

```bash
python turkmen_assistant/main.py --demo
```

### Интерактивный режим

```bash
python turkmen_assistant/main.py
```

### Запуск тестов

```bash
python -m pytest turkmen_assistant/tests/
# или
python turkmen_assistant/tests/test_assistant.py
```

## 💡 Примеры использования

### Базовое использование

```python
from turkmen_assistant import TurkmenAssistant

# Создание ассистента
assistant = TurkmenAssistant(default_language='ru')

# Приветствие
print(assistant.greet())

# Обработка запроса
response = assistant.process_request('Привет')
print(response)

# Смена языка
assistant.set_language('tk')
print(assistant.greet())
```

### Работа с фразами

```python
from turkmen_assistant import PhraseDatabase

db = PhraseDatabase()

# Получение фразы
phrase = db.get_phrase('greetings', 'hello', 'tk')
print(phrase)  # Salam

# Список категорий
categories = db.get_categories()

# Поиск фраз
results = db.search_phrases('спасибо', 'ru')
```

### Перевод

```python
from turkmen_assistant import LanguageHelper

# Простой перевод
translation = LanguageHelper.translate_simple('привет', 'ru', 'tk')
print(translation)  # Salam

# Определение языка
lang = LanguageHelper.detect_language('Salam, nähili?')
print(lang)  # tk
```

## 📖 API Reference

### TurkmenAssistant

Основной класс ассистента.

**Методы:**
- `greet()` - Получить приветствие
- `set_language(lang)` - Установить язык ('tk', 'ru', 'en')
- `process_request(request)` - Обработать запрос пользователя
- `get_phrase(category, key)` - Получить фразу из базы
- `translate(text, from_lang, to_lang)` - Перевести текст
- `get_conversation_history()` - Получить историю диалога
- `clear_history()` - Очистить историю
- `list_phrases(category)` - Получить список фраз

### PhraseDatabase

База данных многоязычных фраз.

**Методы:**
- `get_phrase(category, key, language)` - Получить фразу
- `list_phrases(category)` - Список фраз категории
- `get_categories()` - Список всех категорий
- `add_phrase(category, key, translations)` - Добавить фразу
- `search_phrases(search_term, language)` - Поиск фраз

### LanguageHelper

Утилиты для работы с языками.

**Методы:**
- `translate_simple(text, from_lang, to_lang)` - Простой перевод
- `detect_language(text)` - Определить язык текста
- `normalize_text(text)` - Нормализовать текст
- `get_language_name(lang_code)` - Название языка по коду

## 🎯 Команды CLI

В интерактивном режиме доступны следующие команды:

| Команда | Описание |
|---------|----------|
| `/lang <tk\|ru\|en>` | Изменить язык общения |
| `/phrases` | Показать все фразы |
| `/translate <текст> <from> <to>` | Перевести текст |
| `/history` | Показать историю диалога |
| `/clear` | Очистить историю |
| `/help` | Показать справку |
| `/exit` | Выйти из программы |

## 🧪 Тестирование

Проект включает comprehensive unit-тесты:

```bash
# Запуск всех тестов
python -m unittest discover turkmen_assistant/tests

# Запуск конкретного теста
python turkmen_assistant/tests/test_assistant.py
```

## 📝 Поддерживаемые языки

- **tk** - Туркменский (Türkmençe)
- **ru** - Русский
- **en** - English

## 🔮 Планы развития

- [ ] Интеграция с NLP моделями для лучшего понимания
- [ ] Голосовой ввод/вывод
- [ ] Расширение базы фраз
- [ ] REST API для веб-интеграции
- [ ] Мобильное приложение
- [ ] Поддержка дополнительных языков

## 📄 Лицензия

MIT License

## 👥 Авторы

Turkmen Assistant Team

---
**Версия:** 1.0.0
