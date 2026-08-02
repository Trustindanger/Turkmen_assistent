"""
Turkmen Assistant - Профессиональный ассистент с поддержкой туркменского языка.

Пакет предоставляет функционал для:
- Многоязычного общения (туркменский, русский, английский)
- Перевода базовых фраз
- Распознавания намерений пользователя
"""

__version__ = "1.0.0"
__author__ = "Turkmen Assistant Team"

from .core.assistant import TurkmenAssistant
from .data.phrases import PhraseDatabase
from .utils.helpers import LanguageHelper

__all__ = [
    "TurkmenAssistant",
    "PhraseDatabase",
    "LanguageHelper",
]
