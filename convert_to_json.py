#!/usr/bin/env python3
"""
Конвертер CLAVICULA NOVA из Markdown в JSON для сайта-книги
"""

import json
import re
from pathlib import Path

def parse_clavicula(md_path: str) -> dict:
    """Парсит markdown-файл и возвращает структуру книги"""

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Структура книги
    book = {
        "title": "CLAVICULA NOVA",
        "subtitle": "КЛЮЧ ЖИВОГО ОГНЯ",
        "description": "Гримуар для эпохи сетей",
        "books": [],
        "chapters": []
    }

    # Разбиваем на секции по # КНИГА или # Глава
    lines = content.split('\n')

    current_book = None
    current_chapter = None
    chapter_content = []
    chapter_num = 0

    for line in lines:
        # Детектируем книги (# КНИГА ПЕРВАЯ, # КНИГА ВТОРАЯ и т.д.)
        book_match = re.match(r'^#\s+КНИГА\s+(\w+):\s*(.+)$', line, re.IGNORECASE)
        if book_match:
            book_name = book_match.group(2).strip()
            current_book = {
                "name": book_name,
                "chapters": []
            }
            book["books"].append(current_book)
            continue

        # Детектируем главы (# Глава I., ## Глава II. и т.д.)
        chapter_match = re.match(r'^#{1,2}\s+Глава\s+([IVXLCDM]+)[.:]?\s*(.*)$', line, re.IGNORECASE)
        if chapter_match:
            # Сохраняем предыдущую главу
            if current_chapter and chapter_content:
                current_chapter["content"] = '\n'.join(chapter_content).strip()
                book["chapters"].append(current_chapter)

            chapter_num += 1
            roman = chapter_match.group(1)
            title = chapter_match.group(2).strip() or f"Глава {roman}"

            current_chapter = {
                "id": chapter_num,
                "roman": roman,
                "title": title,
                "book": current_book["name"] if current_book else "Введение"
            }
            chapter_content = []

            if current_book:
                current_book["chapters"].append(chapter_num)
            continue

        # Детектируем другие главы по ## НАЗВАНИЕ (все заглавные)
        alt_chapter_match = re.match(r'^#{1,3}\s+([А-ЯЁ][А-ЯЁ\s]+)$', line)
        if alt_chapter_match and len(alt_chapter_match.group(1)) > 5:
            title = alt_chapter_match.group(1).strip()
            # Пропускаем если это не похоже на главу
            if title in ['ТРИ ЦАРСТВА', 'СЕМЬ СИЛ', 'ПЯТЬ ОБОЛОЧЕК']:
                if current_chapter and chapter_content:
                    current_chapter["content"] = '\n'.join(chapter_content).strip()
                    book["chapters"].append(current_chapter)

                chapter_num += 1
                current_chapter = {
                    "id": chapter_num,
                    "roman": "",
                    "title": title.title(),
                    "book": current_book["name"] if current_book else "Введение"
                }
                chapter_content = []

                if current_book:
                    current_book["chapters"].append(chapter_num)
                continue

        # Собираем контент главы
        if current_chapter is not None:
            chapter_content.append(line)

    # Сохраняем последнюю главу
    if current_chapter and chapter_content:
        current_chapter["content"] = '\n'.join(chapter_content).strip()
        book["chapters"].append(current_chapter)

    return book


def parse_by_headers(md_path: str) -> dict:
    """Альтернативный парсер - разбивает по ## заголовкам"""

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    book = {
        "title": "CLAVICULA NOVA",
        "subtitle": "КЛЮЧ ЖИВОГО ОГНЯ",
        "description": "Гримуар для эпохи сетей",
        "chapters": []
    }

    # Разбиваем по ## заголовкам
    sections = re.split(r'\n(?=##?\s+)', content)

    chapter_num = 0
    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        first_line = lines[0]

        # Извлекаем заголовок
        header_match = re.match(r'^#{1,3}\s+(.+)$', first_line)
        if header_match:
            title = header_match.group(1).strip()
            chapter_num += 1

            # Контент без заголовка
            content_lines = lines[1:]
            content_text = '\n'.join(content_lines).strip()

            # Пропускаем пустые секции
            if len(content_text) < 100:
                continue

            book["chapters"].append({
                "id": chapter_num,
                "title": title,
                "content": content_text
            })

    return book


if __name__ == "__main__":
    import sys

    md_path = sys.argv[1] if len(sys.argv) > 1 else "/mnt/c/Users/PC/Downloads/CLAVICULA_NOVA_COMPLETE_FINAL.md"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "book.json"

    print(f"Парсинг: {md_path}")
    book = parse_by_headers(md_path)

    print(f"Найдено глав: {len(book['chapters'])}")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(book, f, ensure_ascii=False, indent=2)

    print(f"Сохранено: {output_path}")

    # Показываем оглавление
    print("\nОглавление:")
    for ch in book["chapters"][:20]:
        print(f"  {ch['id']:2d}. {ch['title'][:50]}")
    if len(book["chapters"]) > 20:
        print(f"  ... и ещё {len(book['chapters']) - 20} глав")
