#!/usr/bin/env python3
"""Integrate generated images into book chapters"""

import json
import re

# Map chapters to relevant images
CHAPTER_IMAGES = {
    1: [  # Что такое Соломонова магия
        ("images/cover-main.jpg", "Гримуар CLAVICULA NOVA"),
        ("images/book-open-grimoire.jpg", "Раскрытый гримуар"),
        ("images/magician-study.jpg", "Маг за изучением текстов"),
    ],
    2: [  # Каббалистическая космология
        ("images/tree-of-life-full.jpg", "Древо Жизни"),
        ("images/four-worlds.jpg", "Четыре мира Каббалы"),
        ("images/ain-soph-aur.jpg", "Эйн Соф Аур - Бесконечный Свет"),
        ("images/sephirah-kether.jpg", "Кетер - Корона"),
        ("images/sephirah-tiphareth.jpg", "Тиферет - Красота"),
        ("images/sephirah-malkuth.jpg", "Малкут - Царство"),
    ],
    3: [  # Природа духов
        ("images/upper_realm.jpg", "Высшие сферы"),
        ("images/middle_realm.jpg", "Средние сферы"),
        ("images/lower_realm.jpg", "Нижние сферы"),
        ("images/goetia_spirit.jpg", "Дух Гоэтии"),
    ],
    4: [  # Святой Ангел-Хранитель
        ("images/archangel.jpg", "Архангел"),
        ("images/angel-human-contact.jpg", "Контакт ангела с человеком"),
        ("images/higher-self-connection.jpg", "Связь с Высшим Я"),
    ],
    5: [  # Законы магической операции
        ("images/ritual-circle.jpg", "Магический круг"),
        ("images/ritual_altar.jpg", "Ритуальный алтарь"),
    ],
    6: [  # Подготовка мага
        ("images/ritual-meditation.jpg", "Медитация"),
        ("images/energy-cleansing.jpg", "Энергетическое очищение"),
        ("images/initiation-ceremony.jpg", "Церемония инициации"),
    ],
    7: [  # Большой Ключ Соломона
        ("images/pentacle.jpg", "Пентакль Соломона"),
        ("images/ritual-consecration.jpg", "Консекрация инструментов"),
    ],
    8: [  # Пентакли Соломона — полный свод
        ("images/pentacle-saturn-1.jpg", "Первый пентакль Сатурна"),
        ("images/pentacle-jupiter-1.jpg", "Первый пентакль Юпитера"),
        ("images/pentacle-mars-1.jpg", "Первый пентакль Марса"),
        ("images/pentacle-sun-1.jpg", "Первый пентакль Солнца"),
        ("images/pentacle-venus-1.jpg", "Первый пентакль Венеры"),
        ("images/pentacle-mercury-1.jpg", "Первый пентакль Меркурия"),
        ("images/pentacle-moon-1.jpg", "Первый пентакль Луны"),
    ],
    9: [  # Малый Ключ — Гоэтия
        ("images/ritual-triangle.jpg", "Треугольник вызывания"),
        ("images/ritual-evocation.jpg", "Эвокация духа"),
    ],
    10: [  # 72 духа Гоэтии — полный свод
        ("images/goetia-bael.jpg", "Баэль - первый дух"),
        ("images/goetia-paimon.jpg", "Паймон - великий король"),
        ("images/goetia-asmodeus.jpg", "Асмодей"),
        ("images/goetia-astaroth.jpg", "Астарот"),
        ("images/goetia-belial.jpg", "Белиал"),
        ("images/goetia-dantalion.jpg", "Данталион"),
    ],
    11: [  # Шемхамфораш — 72 имени
        ("images/symbol-tetragrammaton.jpg", "Тетраграмматон"),
        ("images/symbol-hexagram.jpg", "Гексаграмма"),
    ],
    12: [  # 72 ангела Шемхамфораш
        ("images/archangel-metatron.jpg", "Метатрон"),
        ("images/archangel-michael.jpg", "Михаэль"),
        ("images/archangel-gabriel.jpg", "Гавриэль"),
        ("images/archangel-raphael.jpg", "Рафаэль"),
        ("images/archangel-uriel.jpg", "Уриэль"),
    ],
    13: [  # Божественные и ангельские имена
        ("images/vibration-names.jpg", "Вибрация священных имён"),
        ("images/symbol-tetragrammaton.jpg", "Святое Имя"),
    ],
    14: [  # Духи планет и элементов
        ("images/planet-saturn.jpg", "Сатурн"),
        ("images/planet-jupiter.jpg", "Юпитер"),
        ("images/planet-mars.jpg", "Марс"),
        ("images/planet-sun.jpg", "Солнце"),
        ("images/planet-venus.jpg", "Венера"),
        ("images/planet-mercury.jpg", "Меркурий"),
        ("images/planet-moon.jpg", "Луна"),
        ("images/element-fire.jpg", "Элемент Огня"),
        ("images/element-water.jpg", "Элемент Воды"),
        ("images/element-air.jpg", "Элемент Воздуха"),
        ("images/element-earth.jpg", "Элемент Земли"),
    ],
    15: [  # Храм и круг
        ("images/temple-setup.jpg", "Устройство храма"),
        ("images/ritual-circle.jpg", "Магический круг"),
    ],
    16: [  # Инструменты мага
        ("images/tool-wand.jpg", "Жезл"),
        ("images/tool-sword.jpg", "Меч"),
        ("images/tool-cup.jpg", "Чаша"),
        ("images/tool-pentacle.jpg", "Пентакль"),
        ("images/tool-censer.jpg", "Кадильница"),
        ("images/tool-lamp.jpg", "Лампа"),
        ("images/tool-robe.jpg", "Ритуальное облачение"),
        ("images/tool-altar.jpg", "Алтарь"),
    ],
    17: [  # Эвокация — полный ритуал
        ("images/ritual-evocation.jpg", "Эвокация"),
        ("images/ritual-triangle.jpg", "Треугольник искусства"),
        ("images/seance-spirit.jpg", "Появление духа"),
    ],
    18: [  # Тайминг операций
        ("images/planetary-hours.jpg", "Планетарные часы"),
        ("images/moon-phases.jpg", "Фазы Луны"),
        ("images/solar-year.jpg", "Солнечный год"),
        ("images/astrology_zodiac.jpg", "Зодиакальный круг"),
    ],
    19: [  # Инвокация божественных сил
        ("images/ritual-invocation.jpg", "Инвокация"),
        ("images/ritual-lbrp.jpg", "Малый ритуал пентаграммы"),
        ("images/merkaba-vehicle.jpg", "Меркаба"),
    ],
    20: [  # Диагностика и решение проблем
        ("images/ritual-scrying.jpg", "Скраинг"),
        ("images/crystals.jpg", "Кристаллы для работы"),
    ],
    21: [  # Защита и изгнание
        ("images/protection-sphere.jpg", "Защитная сфера"),
        ("images/banishing-ritual.jpg", "Ритуал изгнания"),
        ("images/home-warding.jpg", "Защита дома"),
        ("images/protection_magic.jpg", "Защитная магия"),
    ],
    22: [  # Обретение знания и мудрости
        ("images/vision-astral.jpg", "Астральное видение"),
        ("images/ritual-meditation.jpg", "Глубокая медитация"),
    ],
    23: [  # Влияние и коммуникация
        ("images/goetia-paimon.jpg", "Паймон - мастер влияния"),
        ("images/goetia-dantalion.jpg", "Данталион - знаток мыслей"),
    ],
    24: [  # Материальное благополучие
        ("images/pentacle-jupiter-4.jpg", "Пентакль Юпитера для богатства"),
        ("images/goetia-bune.jpg", "Буне - дух богатства"),
    ],
    25: [  # Любовь и отношения
        ("images/pentacle-venus-1.jpg", "Пентакль Венеры"),
        ("images/goetia-sitri.jpg", "Ситри"),
    ],
    26: [  # Исцеление и здоровье
        ("images/archangel-raphael.jpg", "Рафаэль - ангел исцеления"),
        ("images/goetia-marbas.jpg", "Марбас - дух исцеления"),
    ],
    27: [  # Таблицы соответствий
        ("images/tree-of-life-pillars.jpg", "Три столпа Древа"),
    ],
    28: [  # 72 духа Гоэтии (приложение)
        ("images/goetia-vassago.jpg", "Вассаго"),
        ("images/goetia-barbatos.jpg", "Барбатос"),
        ("images/goetia-gusion.jpg", "Гусион"),
        ("images/goetia-foras.jpg", "Форас"),
        ("images/goetia-orobas.jpg", "Оробас"),
    ],
    29: [  # 72 ангела Шемхамфораш (приложение)
        ("images/archangel-tzadkiel.jpg", "Цадкиэль"),
        ("images/archangel-camael.jpg", "Камаэль"),
        ("images/archangel-haniel.jpg", "Ханиэль"),
        ("images/archangel-tzaphkiel.jpg", "Цафкиэль"),
        ("images/archangel-sandalphon.jpg", "Сандальфон"),
    ],
    30: [  # Образцы ритуалов
        ("images/ritual_altar.jpg", "Подготовленный алтарь"),
        ("images/ritual-consecration.jpg", "Консекрация"),
    ],
    31: [  # Глоссарий
        ("images/symbol-pentagram.jpg", "Пентаграмма"),
        ("images/symbol-hexagram.jpg", "Гексаграмма"),
        ("images/symbol-ankh.jpg", "Анкх"),
        ("images/symbol-caduceus.jpg", "Кадуцей"),
        ("images/symbol-ouroboros.jpg", "Уроборос"),
        ("images/symbol-eye-providence.jpg", "Всевидящее око"),
        ("images/symbol-rose-cross.jpg", "Розовый крест"),
    ],
    32: [  # Пентакли Соломона — полное описание
        ("images/pentacle-saturn-1.jpg", "1-й пентакль Сатурна"),
        ("images/pentacle-saturn-2.jpg", "2-й пентакль Сатурна"),
        ("images/pentacle-saturn-3.jpg", "3-й пентакль Сатурна"),
        ("images/pentacle-jupiter-1.jpg", "1-й пентакль Юпитера"),
        ("images/pentacle-jupiter-2.jpg", "2-й пентакль Юпитера"),
        ("images/pentacle-jupiter-3.jpg", "3-й пентакль Юпитера"),
        ("images/pentacle-mars-1.jpg", "1-й пентакль Марса"),
        ("images/pentacle-mars-2.jpg", "2-й пентакль Марса"),
        ("images/pentacle-sun-1.jpg", "1-й пентакль Солнца"),
        ("images/pentacle-sun-2.jpg", "2-й пентакль Солнца"),
        ("images/pentacle-venus-1.jpg", "1-й пентакль Венеры"),
        ("images/pentacle-venus-2.jpg", "2-й пентакль Венеры"),
        ("images/pentacle-mercury-1.jpg", "1-й пентакль Меркурия"),
        ("images/pentacle-mercury-2.jpg", "2-й пентакль Меркурия"),
        ("images/pentacle-moon-1.jpg", "1-й пентакль Луны"),
        ("images/pentacle-moon-2.jpg", "2-й пентакль Луны"),
    ],
    33: [  # Искусство сигилов
        ("images/symbol-sigil-template.jpg", "Шаблон сигила"),
        ("images/symbol-kamea-template.jpg", "Магический квадрат"),
        ("images/symbol-rose-cross.jpg", "Розовый крест для сигилов"),
    ],
    34: [  # Внутренний огонь — прямой контакт с Источником
        ("images/five-souls.jpg", "Пять уровней души"),
        ("images/yechidah-spark.jpg", "Йехида - божественная искра"),
        ("images/inner-fire-awakening.jpg", "Пробуждение внутреннего огня"),
        ("images/kundalini-rising.jpg", "Подъём Кундалини"),
        ("images/prayer-direct.jpg", "Прямая молитва"),
    ],
    35: [  # Магия Псалмов
        ("images/psalm-protection.jpg", "Псалом защиты"),
        ("images/psalm-healing.jpg", "Псалом исцеления"),
        ("images/vibration-names.jpg", "Вибрация священных слов"),
    ],
    36: [  # Современные адаптации — магия XXI века
        ("images/modern-urban-magic.jpg", "Городская магия"),
        ("images/modern-digital-sigil.jpg", "Цифровой сигил"),
        ("images/modern-quick-ritual.jpg", "Быстрый ритуал"),
        ("images/modern-meditation-commute.jpg", "Медитация в пути"),
    ],
    37: [  # Сигил Внутреннего Творца
        ("images/sigil-inner-creator.jpg", "Сигил Внутреннего Творца"),
        ("images/pleroma-personal.jpg", "Личная Плерома"),
        ("images/demiurge-cooperation.jpg", "Сотрудничество с демиургами"),
        ("images/ain-soph-aur.jpg", "Эйн Соф Аур - объединяющий Свет"),
    ],
}

def add_images_to_chapter(content, images, chapter_id):
    """Add image references to chapter content"""
    if not images:
        return content

    # Create image gallery section
    gallery_md = "\n\n---\n\n## Иллюстрации\n\n"
    for img_path, alt_text in images:
        gallery_md += f"![{alt_text}]({img_path})\n*{alt_text}*\n\n"

    # For specific chapters, insert images inline
    lines = content.split('\n')
    result_lines = []

    # Add first image after the first heading for visual appeal
    first_img_added = False
    for i, line in enumerate(lines):
        result_lines.append(line)

        # After the title (first # line), add the main chapter image
        if not first_img_added and line.startswith('# ') and len(images) > 0:
            img_path, alt_text = images[0]
            result_lines.append(f"\n![{alt_text}]({img_path})\n")
            first_img_added = True

    # Add remaining images at the end as a gallery if more than 1 image
    if len(images) > 1:
        result_lines.append("\n---\n\n### Галерея иллюстраций\n")
        for img_path, alt_text in images[1:]:
            result_lines.append(f"\n![{alt_text}]({img_path})")

    return '\n'.join(result_lines)

def main():
    print("Loading book.json...")
    with open('book.json', 'r', encoding='utf-8') as f:
        book = json.load(f)

    print(f"Found {len(book['chapters'])} chapters")

    updated = 0
    for chapter in book['chapters']:
        ch_id = chapter['id']
        if ch_id in CHAPTER_IMAGES:
            images = CHAPTER_IMAGES[ch_id]
            chapter['content'] = add_images_to_chapter(chapter['content'], images, ch_id)
            print(f"  Chapter {ch_id}: Added {len(images)} images")
            updated += 1

    print(f"\nSaving updated book.json...")
    with open('book.json', 'w', encoding='utf-8') as f:
        json.dump(book, f, ensure_ascii=False, indent=2)

    print(f"Done! Updated {updated} chapters with images.")

    # Update index.html cover image
    print("\nUpdating index.html cover image...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('images/cover.png', 'images/cover-main.jpg')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Cover image reference updated.")

if __name__ == '__main__':
    main()
