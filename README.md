Бот для автоматизациии ответов техподдержки
======

Бот-автоотвечик на самые часты вопросы. Работает в вк и телеграмме.

Пример работы:

### [Вконтакте](https://vk.com/im?&sel=-201684484)<br> 
![hippo](https://dvmn.org/media/filer_public/1e/f6/1ef61183-56ad-4094-b3d0-21800bdb8b09/demo_vk_bot.gif)

### [Телеграм](https://t.me/devman_the_game_of_verbs_bot)<br>
![hippo](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

#### Бот работает с версиями Python 3.6+ <br>С версиями ниже бот не работает!!!

## Настройка для использования на личном ПК
1. Скачайте проект с гитхаба
2. Перейдите в папку с ботом с помощью консоли и команды `cd <путь до проекта>`<br>
3. Установить зависимости из файла `requirements.txt`<br>
   Библиотеки к установке: `requests`, `python-telegram-bot`, `python-dotenv`, `google-cloud-dialogflow`, `vk-api`.<br>
   
   Возможные команды для установки:<br>
   `pip3 install -r requirements.txt`<br>
   `python -m pip install -r requirements.txt`<br>
   `python3.6 -m pip install -r requirements.txt`
4. Создайте файл .env
5. Запишите в файл .env переменные:
    `VKONTAKTE_GROUP_TOKEN=ваш_токен_группы вконтакте`<br>
    `TELEGRAM_TOKEN=ваш_токен_телеграм_бота`<br>
    `TELEGRAM_CHAT_ID=ваш_телеграм_айди`<br>
    `GOOGLE_APPLICATION_CREDENTIALS=путь_до_json_ключа_от_гугла.json`<br>
    `путь_до_json_ключа_от_гугла={"type": "service_account", ...}` (весь `json` скопировать в поле)<br>
    `GOOGLE_APPLICATION_PROJECT_ID=project_id_проекта_на_гугл_облаке`<br>
6. Запустите бота<br>
   Возможные команды для запуска(из консоли, из папки с ботом):<br>
   ```
   python3 vk_bot.py
   python3 telegram_bot.py
   ```
   или
   ```
   python vk_bot.py
   python telegram_bot.py
   ```
   или
   ```
   python3.6 main.py
   python3.6 telegram_bot.py
   ```
   
## Настройка для деплоя в облако Heroku
Если не знаем что такое Heroku - гуглим мануал или используем настройку бота из предыдущего туториала
1. Создайте `app` на Heroku 
2. Перейдите в созданный `app` и выберите GitHub в качестве `Deployment method`
3. Укажите адрес до **вашего!!!** проекта на гитхабе
4. Зайдите в раздел `Settings`
5. Запишите в раздел `Config Vars` переменные `KEY` и `VALUE`:
    `VKONTAKTE_GROUP_TOKEN=ваш_токен_группы вконтакте`<br>
    `TELEGRAM_TOKEN=ваш_токен_телеграм_бота`<br>
    `TELEGRAM_CHAT_ID=ваш_телеграм_айди`<br>
    `GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json`<br>
    `GOOGLE_CREDENTIALS ={"type": "service_account", ...}` (весь `json` скопировать в поле)<br>
    `GOOGLE_APPLICATION_PROJECT_ID=project_id_проекта_на_гугл_облаке`<br>
6. Добавьте в раздел `Buildpacks` `https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack`<br>
7. Зайдите в раздел `Deploy`, выберите ветку main в разделе `Manual deploy` и нажмите на кнопку `Deploy Branch`<br>
8. Перейдите в раздел `Resources` и включите бота<br> 
   Логи можно посмотреть в `More` -> `View logs`
  
