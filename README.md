# Сайт для донорв ОПК ГБК 52

Наша цель - разработка веб-сайта для Доноров ОПК ГКБ 52, с помощью которого доноры получают возможность:

Спланировать донации в соответствии с потребностями отделения
Получать информацию о количестве донаций
Узнавать полезную информацию, включая потребности отделения
Идея создания сайта возникла в связи с неравномерностью потока доноров, которая создает дополнительную нагрузку на персонал отделения
либо не даёт возможности оперативно мобилизовать доноров в случае наличия высокой потребности в крови или её компонентов.

Сайт доступен по ссылке http://95.131.149.248:2008/

# Запуск сайта

Для запуска нужно приложение doker,
если его нет, то скачайте с официального сайта
https://www.docker.com/

После того, когда скачаете docker
откройте terminal и клонируйте репозиторий с githab

```bash
git clone https://github.com/Amir1510/medicine_site.git
```
Затем  перейдите
в корневую директорию проекта
и находясь в корневой директории

Введите в terminal
```bash
docker compose build
```

Затем 
```bash
docker compose up
```

после этого прейдете по локальному хосту
http://localhost:8000/
