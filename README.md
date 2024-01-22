# Бот-квест по другому измерению.
Телеграм бот для интерактивного квеста.
## Описание
Квест состоит из предисловия(preface) и 3-х уровней(1_level,
2_level, 3_level). Игрок должен выбирать локации которые он освободит. 
В конце 3-го уровня он узнает правильный он сделал выбор или нет.

## Как настроить:
1) Откройте терминал проекта и напишите команду
`git clone https://github.com/Palenhame/bot_2.git`.
2) Затем команду`python3 -m venv venv`.
3) Потом `source ./venv/Scripts/activate`
### Теперь запустим проект:
1) Откройте терминал проекта и напишите команду `cd bot_2` и 
`pip install -r requirements.txt`.
2) Затем команду `python3 start_settings.py`. Этот файл заполнит базу `json` файл сюжетом.
3) После этого `nano .env` и пишем в этот файл `TOKEN=<ваш токен>` и сохраняем.
4) И запускаем командой `python3 main.py`.