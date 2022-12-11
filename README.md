#### Описание бота:
Бот предназначен для личного использования. Возможны ошибки в работе.
Бот позволяет выкачивать аудиодорожку из видеофайла и отправлять ее, в виде аудиофайла, в ваш чат. 

#### Порядок работы с ботом
После запуска бота, отправьте ему ссылку на плейлист Youtube в виде сообщения.
Далее бот сообщит количество новых (еще не скачанных) файлов. 
- `/start` - сканирование плейлиста на наличие новых файлов;
- `/send` - задание на закачку новых аудиофайлов.

#### Требования:
> В связи с вероятностью загрузки файлов рамером свыше 50 Mb, для снятия ограничений необходимо использовать личный `local-bot-api-server`.
https://core.telegram.org/bots/api#using-a-local-bot-api-server

#### Использование репозитория

Создание образа:
```shell
docker build -t aiogram/aio_bot:latest .
```

Запуск docker-контейнера:
```shell
docker run -e serv_addr=<ip_your_local-bot-api-server> -e bot_token=<your_bot_token> -e chat_bot_id=<your_chat_id> --name aio_bot -d aiogram/aio_bot:latest
```
где `environments`:
- `serv_addr` - ip адрес `local-bot-api-server`;
- `bot_token` - токен вашего бота;
- `chat_bot_id` - id чата, куда бот будет отправлять аудиофайлы (бот должен быть участником этого чата).

#### Опционально

```shell
docker volume create --opt type=none --opt o=bind --opt device=<path_to_volume> <volume>

docker run -e serv_addr=<ip_your_local-bot-api-server> -e bot_token=<your_bot_token> -e chat_bot_id=<your_chat_id> --name aio_bot -v <volume>:/dir-bot/bot-db -d aiogram/aio_bot:latest
```
где:
- `-v <volume>:/dir-bot/bot-db` - доступ к файлам базы данных SQLite контейнера, через монтирование 