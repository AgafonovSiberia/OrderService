# OrderService - Fullstack WebApp (Flask + React)
Work for Каналсервис / Unwind Digital
<br>
Реализовано:
* **Базовое решение:**
  * Получение данных из таблицы по GoogleSheetsAPI
  * Получение текущего курса доллара по API ЦБ РФ
  * Работа с БД PostgreSQL + SQLAlchemy
  * Автоматическое обновление данных в БД (с учётом пересчёта стоимости заказа в рубли по текущуему курсу)
  * Docker/docker-compose
* **FullStackAPP** (расширение для базового решения)
  * backend - FlaskApp
  * frontend - ReactJS
  * периодические/длинные задачи вынесены в Celery
  * рассылка сообщений о просроченных заказах в Telegram
  (периодически в 9:00 по Мск, либо принудительно через ручку <code>GET 0.0.0.0:9090/api/check_expire_orders</code>
  
____________________________________________
### CREDENTIALS
**ВНИМАНИЕ** прежде чем развернуть приложение, необходимо получить данные авторизации для **TelegramBotAPI** и **GoogleSheetsAPI**
<br>
**1. TelegramBotAPI**
* Получить [Telegram BotToken](https://core.telegram.org/bots/features#creating-a-new-bot)
* Получить [ChatID](https://t.me/my_id_bot) пользователей, которые будут получать рассылку от бота.

**2. GoogleSheetsAPI**
* Создать новый проект в [Google Cloud Platform](https://console.cloud.google.com/)
* Подключить к проекту **GoogleSheetsAPI** и **GoogleDriveAPI**
* Создать для проекта **ServiceAccount** и получить **JSON-key**
* Получить [GoogleServiceAccount](https://habr.com/ru/post/575160/)
* Создать таблицу и заполнить её (либо, если вам был передан **env.dev** и предоставлены права Редактора, воспользоваться готовой [TestTable](https://docs.google.com/spreadsheets/d/1QThPLQHXtqHGG4OZ07zH7vdxsd7_ZotuWgXZdA3h5e4/edit#gid=0)
* Дать доступ сервисному аккаунту к вашей GoogleSheet
* [Примерная инструкция](https://habr.com/ru/post/575160/)

____________________________________________

### RUN / DEPLOY
**ВНИМАНИЕ** для развёртывания приложения необходимо убедиться, что на вашей машине установлены  <a href="https://docs.docker.com/">Docker</a> и <a href="https://docs.docker.com/compose/">Docker compose V2</a>
1. Перейдите в директорию, в которую планируете клонировать проект
```
mkdir some_dir
cd some_dir
```
2. Склонируйте репозиторий себе на локальный компьютер
```
git clone https://github.com/AgafonovSiberia/OrderService.git
```
3. Перейдите в директорию проекта 
```
cd OrderService
```
4.Переименуйте файл <code>dist.env</code> в <code>dev.env</code> (либо скопируйте **env.dev** в директорию проекта, если он был выдан вам ранее)
```
mv dist.env dev.env
либо
mv ../some_folder/dev.env dev.env
```
5.Заполните файл <code>dev.env</code> - <i>смотреть комментарии в файле</i> <code>dev.env</code>

**6. Режимы развёртывания приложения**
<br>
6.1. Для **запуска базового** решения (только скрипт обновления БД) выполните команду 
``` make run_base ```
<br>Для **остановки базового** </u> решения ``` make stop_base ```
<br><br>
6.2. Для **запуска** Fullstack App выполните команду  ``` make run ```
<br> Для **остановки** выполните команду ``` make stop ```

____________________________________________

### REST API
* <code>GET 0.0.0.0:9090/api/orders</code> - получить список всех заказов
* <code>GET 0.0.0.0:9090/api/total</code> - получить сумму всех заказов в долларах и рублях по текущему курсу
* <code>GET 0.0.0.0:9090/api/price_dynamic</code> - получить стоимость заказов в долларах, отсортированную по дате
* <code>GET 0.0.0.0:9090/api/get_expire_orders</code> - получить список заказов, срок поставки которых истекает сегодня
* <code>GET 0.0.0.0:9090/api/check_expire_orders</code> - принудительно запустить таску проверки истекующих заказов (вызовет рассылку сообщений в Telegram)

