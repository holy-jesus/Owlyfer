# Owlyfer

![Logo](https://telegra.ph/file/3112bd2e899d1a97c364c.png)

# Бот-предложка для вашего Телеграм канала

## Информация

Данный бот позволяет добавить функционал предложенных записей для вашего Телеграм канала  
Поддерживает все типы каналов - от публичных до приватных

## Требования

- Свой сервер (бота можно запустить на компьютере, но компьютер придётся постоянно держать включённым)

- Docker Compose

  ИЛИ

- Python
- MongoDB
- PostgreSQL

## Установка

### Docker Compose

TODO

### TODO

1. Создайте бота у [BotFather](https://t.me/BotFather).
2. [Скачайте бота в браузере](https://github.com/holy-jesus/Owlyfer/archive/refs/heads/main.zip) ИЛИ склонируйте репозиторий командой ниже.

```
git clone https://github.com/holy-jesus/Owlyfer
```

3. Скопируйте settings.ini.example с новым названием settings.ini.
4. Измените settings.ini, вставив туда bot_token, ID канала, данные от MongoDB и PostgreSQL, после чего добавьте бота в канал, выдав ему право публикации сообщений.
5. Установите зависимости

```
pip install -r requirements.txt
```

6. Запустите бота

```
python3 main.py
```
