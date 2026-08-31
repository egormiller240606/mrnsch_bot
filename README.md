# ⚽ Football Telegram Bot

Telegram-бот для автоматической отправки расписания футбольных матчей выбранных команд.

Бот получает данные через **Live Football API**, формирует расписание и отправляет его в Telegram. Автоматическая рассылка запускается через **GitHub Actions** по расписанию.

## ✨ Возможности

* 📅 Получение расписания матчей
* ⚽ Поддержка нескольких футбольных клубов
* 🏆 Учет различных турниров и лиг
* 📊 Использование Live Football API
* 🤖 Автоматическая отправка сообщений в Telegram
* ⏰ Автоматический запуск через GitHub Actions
* 🔐 Хранение API-ключей в GitHub Secrets

## 🏟️ Поддерживаемые команды

1. 🔵 Barcelona
2. ⚪ Real Madrid
3. 🔴 Bayern München
4. 🟡 Fenerbahçe
5. 🔵 Al-Hilal
6. 🟡 Al-Nassr
7. 🔵 Chelsea
8. 🔵 Inter

## 🛠️ Стек

* Python 3
* python-telegram-bot
* Live Football API
* GitHub Actions
* Cron
* YAML

## 🚀 Установка

### Клонирование репозитория

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

## 🔑 Получение ключей

Для работы бота понадобятся следующие данные:

### Telegram Bot Token

Создай Telegram-бота через **@BotFather** и получи токен.

### Chat ID

Узнать свой Telegram ID можно через **@userinfobot**.

### Football API Key

Зарегистрируйся на **Live Football API** и получи API-ключ.

## 🔐 Настройка GitHub Secrets

Чтобы ключи не хранились непосредственно в коде, необходимо добавить их в GitHub Secrets.

Открой:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Добавь следующие секреты:

| Name               | Description                |
| ------------------ | -------------------------- |
| `BOT_TOKEN`        | Токен Telegram-бота        |
| `CHAT_ID`          | ID чата Telegram           |
| `FOOTBALL_API_KEY` | API-ключ Live Football API |


## ⏰ Автоматическая рассылка

Автоматический запуск настроен в файле:

```text
.github/workflows/schedule.yml
```

GitHub Actions использует формат **Cron**.

Например:

```yaml
schedule:
  - cron: '0 6 * * *'
```

Это означает запуск каждый день в:

```text
06:00 UTC
```

Москва находится в часовом поясе UTC+3, поэтому:

```text
06:00 UTC = 09:00 МСК
```


## ▶️ Локальный запуск

После настройки переменных окружения запусти:

```bash
python bot.py
```

Для macOS также можно использовать:

```bash
python3 bot.py
```

## 🤖 GitHub Actions

Workflow автоматически запускает бота согласно расписанию.

Файл:

```text
.github/workflows/schedule.yml
```

Пример:

```yaml
name: Football Schedule

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  send-schedule:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run bot
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
          FOOTBALL_API_KEY: ${{ secrets.FOOTBALL_API_KEY }}
        run: python bot.py
```

## 🔄 Ручной запуск

В workflow предусмотрен:

```yaml
workflow_dispatch:
```

Это позволяет запустить рассылку вручную через GitHub:

```text
Actions
→ Football Schedule
→ Run workflow
```

## 📡 API

Для получения футбольных данных используется:

**Live Football API**

API используется для получения информации о матчах, расписании, командах и турнирах.

## 🔒 Безопасность

Не добавляй секреты непосредственно в Python-код.

❌ Плохо:

```python
BOT_TOKEN = "123456:ABCDEF..."
```

✅ Хорошо:

```python
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
```

Также рекомендуется добавить `.env` в `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

## 📌 TODO

* [ ] Добавить больше команд
* [ ] Добавить уведомления о начале матча
* [ ] Добавить live-счёт
* [ ] Добавить уведомления о голах
* [ ] Добавить турнирные таблицы
* [ ] Добавить выбор любимых команд
* [ ] Добавить настройку времени рассылки для пользователей
* [ ] Добавить поддержку нескольких Telegram-чатов

## 📄 License

This project is intended for personal and educational use.
