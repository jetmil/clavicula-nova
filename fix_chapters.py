#!/usr/bin/env python3
"""
Удаление шаблонного мусора из глав и добавление картинок к релевантным главам
"""

import json
import re

# Шаблонный мусор который нужно удалить
TEMPLATE_GARBAGE = [
    r"## Исторический контекст\s*\n\n.*?унаследовали сегодня\.\s*\n\n",
    r"## Космология и метафизика\s*\n\n.*?в обоих мирах\.\s*\n\n",
    r"## Основные практики\s*\n\n.*?многолетней подготовки\.\s*\n\n",
    r"## Этика и предупреждения\s*\n\n.*?с силами традиции\s*\n\n",
    r"## Интеграция в современную практику\s*\n\n.*?обстоятельств практика\.\s*\n*",
    r"## Подготовка к практике\s*\n\n.*?Размытое намерение даёт размытый результат\.\s*\n\n",
    r"## Пошаговое выполнение\s*\n\n.*?возникающих ощущений\s*\n\n",
    r"### Фаза 1: Открытие\s*\n\n.*?направляющих сил\s*\n\n",
    r"### Фаза 2: Основная работа\s*\n\n.*?возникающих ощущений\s*\n\n",
    r"### Фаза 3: Закрытие\s*\n\n.*?обычными делами\s*\n\n",
    r"## Признаки успешной практики\s*\n\n.*?заметен спустя время\.\s*\n\n",
    r"## Возможные трудности\s*\n\n.*?проявиться позже\.\s*\n\n",
    r"## Дальнейшее развитие\s*\n\n.*?конкретные ситуации\s*\n*",
    r"Каждая духовная традиция — это уникальный путь.*?места человека во вселенной\.\s*\n\n",
    r"Любая магическая практика — это мост.*?во внешнем мире\.\s*\n\n",
    r"данная традиция",
    r"данной традиции",
    r"данную традицию",
]

# Картинки для конкретных глав (по ID или ключевым словам в названии)
CHAPTER_IMAGES = {
    # Три царства
    "верхн": "upper_realm.png",
    "небесн": "upper_realm.png",
    "средн": "middle_realm.png",
    "нижн": "lower_realm.png",
    "подземн": "lower_realm.png",

    # Планетарные силы
    "солнц": "sun_force.png",
    "солярн": "sun_force.png",
    "лун": "moon_force.png",

    # Традиции
    "эллин": "greek_tradition.png",
    "греческ": "greek_tradition.png",
    "египет": "egyptian_tradition.png",
    "северн": "nordic_tradition.png",
    "скандинав": "nordic_tradition.png",
    "один": "nordic_tradition.png",
    "рун": "nordic_tradition.png",
    "кельт": "celtic_tradition.png",
    "друид": "celtic_tradition.png",
    "славян": "slavic_tradition.png",
    "перун": "slavic_tradition.png",
    "велес": "slavic_tradition.png",
    "сварог": "slavic_tradition.png",
    "месопотам": "mesopotamian_tradition.png",
    "вавилон": "mesopotamian_tradition.png",
    "шумер": "mesopotamian_tradition.png",
    "индуист": "hindu_tradition.png",
    "ганеш": "hindu_tradition.png",
    "шива": "hindu_tradition.png",
    "вишну": "hindu_tradition.png",
    "японск": "japanese_tradition.png",
    "синто": "japanese_tradition.png",
    "ками": "japanese_tradition.png",
    "китайск": "chinese_tradition.png",
    "даос": "chinese_tradition.png",
    "каббал": "kabbalah_tradition.png",
    "сефир": "kabbalah_tradition.png",
    "шемхамфораш": "kabbalah_tradition.png",

    # Ангелы и демоны
    "архангел": "archangel.png",
    "михаил": "archangel.png",
    "гоэти": "goetia_spirit.png",
    "демон": "goetia_spirit.png",

    # Элементали
    "огн": "fire_elemental.png",
    "саламандр": "fire_elemental.png",
    "вод": "water_elemental.png",
    "ундин": "water_elemental.png",
    "воздух": "air_elemental.png",
    "сильф": "air_elemental.png",
    "земл": "earth_elemental.png",
    "гном": "earth_elemental.png",
    "элементал": "fire_elemental.png",

    # Инструменты
    "пентакл": "pentacle.png",
    "соломон": "pentacle.png",
    "алтар": "ritual_altar.png",
    "ритуал": "ritual_altar.png",
    "таро": "tarot_spread.png",
    "аркан": "tarot_spread.png",
    "кристалл": "crystals.png",
    "камн": "crystals.png",
    "защит": "protection_magic.png",

    # Астрология и нумерология
    "астролог": "astrology_zodiac.png",
    "зодиак": "astrology_zodiac.png",
    "планет": "astrology_zodiac.png",
    "нумеролог": "numerology_magic.png",
    "числ": "numerology_magic.png",
}

def clean_chapter(content):
    """Удаляем шаблонный мусор"""
    if not content:
        return content

    for pattern in TEMPLATE_GARBAGE:
        content = re.sub(pattern, "", content, flags=re.DOTALL | re.IGNORECASE)

    # Убираем множественные пустые строки
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content.strip()

def get_image_for_chapter(title):
    """Определяем подходящую картинку для главы"""
    title_lower = title.lower()

    for keyword, image in CHAPTER_IMAGES.items():
        if keyword in title_lower:
            return image

    return None

def add_image_to_chapter(content, image_name, title):
    """Добавляем картинку в начало главы"""
    if not image_name:
        return content

    # Формируем markdown для картинки
    image_md = f"\n\n![{title}](images/{image_name})\n\n"

    # Вставляем после первого абзаца (если есть) или в начало
    paragraphs = content.split('\n\n')
    if len(paragraphs) > 1:
        # Вставляем после первого абзаца
        return paragraphs[0] + image_md + '\n\n'.join(paragraphs[1:])
    else:
        return image_md + content

def main():
    # Загружаем книгу
    with open('book.json', 'r', encoding='utf-8') as f:
        book = json.load(f)

    chapters = book['chapters']
    cleaned_count = 0
    images_added = 0

    for i, chapter in enumerate(chapters):
        title = chapter.get('title', '')
        content = chapter.get('content', '')
        original_len = len(content)

        # Чистим от шаблонного мусора
        content = clean_chapter(content)

        # Проверяем, добавлена ли уже картинка
        if '![' not in content:
            # Определяем картинку для главы
            image = get_image_for_chapter(title)
            if image:
                content = add_image_to_chapter(content, image, title)
                images_added += 1
                print(f"+ Картинка: {chapter.get('id', i)}: {title[:40]}... -> {image}")

        if len(content) != original_len:
            cleaned_count += 1

        chapters[i]['content'] = content

    # Сохраняем
    book['chapters'] = chapters
    with open('book.json', 'w', encoding='utf-8') as f:
        json.dump(book, f, ensure_ascii=False, indent=2)

    # Пересчитываем статистику
    total_words = sum(len(ch.get('content', '').split()) for ch in chapters)

    print(f"\n{'='*60}")
    print(f"Очищено глав: {cleaned_count}")
    print(f"Добавлено картинок: {images_added}")
    print(f"Всего слов теперь: {total_words:,}")

if __name__ == "__main__":
    main()
