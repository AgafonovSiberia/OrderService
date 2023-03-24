# OrderService - Fullstack WebApp (Flask + React)
Test work for Unwind Digital

### ЗАПУСК
**ВНИМАНИЕ** для развёртывания приложения необходимо установить  <a href="https://docs.docker.com/">Docker</a> и <a href="https://docs.docker.com/compose/">Docker-compose</a>
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
4.Преименуйте файл <code>dist.env</code> в <code>dev.env</code>
```
mv dist.env dev.env
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


