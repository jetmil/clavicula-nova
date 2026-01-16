# Деплой CLAVICULA NOVA на GitHub Pages

## Вариант 1: Через браузер (самый простой)

1. **Создай репозиторий на GitHub:**
   - Открой https://github.com/new
   - Имя: `clavicula-nova`
   - Описание: `CLAVICULA NOVA — Ключ Живого Огня. Гримуар для эпохи сетей.`
   - Public
   - НЕ добавляй README, .gitignore, license

2. **Загрузи файлы:**
   ```bash
   cd C:\Users\PC\Downloads\clavicula-nova-site
   git remote add origin https://github.com/ТВОЙ_USERNAME/clavicula-nova.git
   git branch -M main
   git push -u origin main
   ```

3. **Включи GitHub Pages:**
   - Открой Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, / (root)
   - Save

4. **Готово!**
   Сайт будет доступен через 1-2 минуты по адресу:
   `https://ТВОЙ_USERNAME.github.io/clavicula-nova/`

---

## Вариант 2: Через gh CLI

```bash
# Авторизация (один раз)
gh auth login

# Создание и деплой
cd C:\Users\PC\Downloads\clavicula-nova-site
gh repo create clavicula-nova --public --source=. --push

# Включить Pages
gh api repos/ТВОЙ_USERNAME/clavicula-nova/pages -X POST -f source[branch]=main -f source[path]=/
```

---

## Файлы в проекте

| Файл | Описание |
|------|----------|
| `index.html` | Главная страница — читалка книги |
| `book.json` | Контент книги (314 глав, 123,750 слов) |
| `convert_to_json.py` | Скрипт конвертации MD → JSON |

---

## Статистика книги

- **Глав:** 314
- **Слов:** 123,750
- **Строк:** 30,546
- **Темы:** Космология, Антропология, Пантеоны, Бестиарий, Травник, Лапидарий, Таро, Руны, Астрология, Нумерология, Ритуалы, Практики

---

## После деплоя

Сайт будет выглядеть так:
- Тёмная тема с золотыми акцентами
- Обложка с названием и кнопкой "Начать чтение"
- Боковое меню с оглавлением (314 глав)
- Навигация стрелками ← →
- Полоса прогресса чтения
- Адаптивный дизайн для мобильных
