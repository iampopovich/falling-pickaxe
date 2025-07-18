#!/usr/bin/env python3
"""
Тест функции validate_live_stream_id
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем функцию (нужно временно закомментировать API инициализацию в youtube.py для тестирования)
import re

def validate_live_stream_id(input_string):
    """
    Извлекает ID видео из YouTube URL или возвращает строку как есть, если это уже ID.
    """
    if not input_string:
        return None
    
    # Паттерны для различных форматов YouTube URL
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtube\.com/live/)([a-zA-Z0-9_-]{11})',  # watch?v= или live/
        r'youtu\.be/([a-zA-Z0-9_-]{11})',  # youtu.be/
        r'^([a-zA-Z0-9_-]{11})$'  # Прямой ID (11 символов)
    ]
    
    for pattern in patterns:
        match = re.search(pattern, input_string)
        if match:
            return match.group(1)
    
    return None

# Тестовые случаи
test_cases = [
    "https://www.youtube.com/watch?v=uvubgYqg9VQ",
    "https://www.youtube.com/live/uvubgYqg9VQ?si=dfmI1IOGu4NRlxtM", 
    "https://youtu.be/uvubgYqg9VQ",
    "uvubgYqg9VQ",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s",
    "invalid_url",
    ""
]

print("Тестирование функции validate_live_stream_id:")
print("=" * 50)

for test_url in test_cases:
    result = validate_live_stream_id(test_url)
    print(f"Вход: {test_url}")
    print(f"Результат: {result}")
    print("-" * 30)
