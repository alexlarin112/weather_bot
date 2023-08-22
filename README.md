# weather_bot

Описание бота:

- Получения информации о погоде: температура, влажность, давление, индекс UV;
- Погода определяется по заданному пользователем городу или переданной геолокации (только мобильные устройства);
- Возможность создать постояное уведомление по местному времени пользователя;
- Сообщение с погодой формируется в виде изображения;
- Данные с сервисов кешируются и не запрашиваются заново, пока не устрареют;
- Сохранение данных пользователей после перезапуска бота.

![photo](https://github.com/alexlarin112/weather_bot/assets/109760128/e5a70f59-507f-4354-8e6c-7c07d56196ff)

Ограничения:
- 1000 запросов - максимальное беспланое количество запросов к сервису https://openweathermap.org/
- 50 запросов - максимальное беспланое количество запросов к сервису https://www.openuv.io/ 

Настройка бота: 

1) В файле .env.example нужно заменить api-ключи для корректной работы бота после чего переименновать файл в .env
- OPEN_WEATHER_API_KEY - API Token с сайта https://openweathermap.org/
- OPENUV_API_KEY - API Token с сайта https://www.openuv.io/
- BOT_TOKEN - Token телеграм бота 
- TIMEZONEDB_API_KEY - Token с сайта https://timezonedb.com/ (необязательно)
- ADMIN_IDS - id администратора бота в телеграме 

2) Необходимо установить Ubuntu для Windows (можно из microsoft store) после чего установить в нем redis

Запуск бота: 

1) Зупустить Ubuntu
2) Запустить redis командой: $ sudo service redis-server start
3) Ввести пароль пользователя
4) Запустить бота командой: python bot.py

Установка redis в Ubuntu на Windows:

1) Зайти в Microsoft Store, найти в поиске и установить Ubuntu
2) Через поиск в пуске зайти в Ubuntu
3) В открывшейся консоли создать пользователя и пароль   
4) Ввести:
- $ sudo apt-add-repository ppa:redislabs/redis
- $ sudo apt-get update
- $ sudo apt-get upgrade
- $ sudo apt-get install redis-server
- $ sudo apt-get install redis-tools
- $ sudo service redis-server restart


python 3.11.4
