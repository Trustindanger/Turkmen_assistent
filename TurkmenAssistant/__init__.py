"""
Turkmen Assistant - Профессиональный ассистент с поддержкой туркменского языка.

Пакет предоставляет функционал для:
- Многоязычного общения (туркменский, русский, английский)
- Перевода базовых фраз
- Распознавания намерений пользователя
"""

__version__ = "1.0.0"
__author__ = "Turkmen Assistant Team"

from TurkmenAssistant.core.assistant import TurkmenAssistant
from TurkmenAssistant.data.phrases import PhraseDatabase
from TurkmenAssistant.utils.helpers import LanguageHelper

__all__ = [
    "TurkmenAssistant",
    "PhraseDatabase",
    "LanguageHelper",
]
