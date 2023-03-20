# Сервис SMM Planer

Сервис  позволяет автоматизировать публикацию рекламы в соцсетях. Информация: ссылка на Google
документ с текстом объявления, фотография товара, дата публикации, целевая социальная сеть, - 
хранится в Google таблице.

![image](https://user-images.githubusercontent.com/76903715/226282870-012c9b6b-22d3-46cb-a3c9-1084eb179f0c.png)


##Настройка среды выполнения

Для работы с сервисом необходимо настроить взаимодействие с API Google и социальных сетей:

- [API Google](https://developers.google.com/sheets?hl=ru)
- [API Телеграмм](https://habr.com/ru/post/543676/)
- [API ВКонтакте](https://dev.vk.com/api/callback/getting-started)
- [API Одноклассники](https://apiok.ru/)

Полученные данные присвоить переменным окружения в файле ".env".

```python
SPREADSHEET_ID=

TELEGRAM_TOKEN=
TG_CHAT_ID=

VK_ACCESS_TOKEN=
VK_GROUP_ID=

OK_ACCESS_TOKEN=
OK_APPLICATION_KEY=
OK_APPLICATION_SECRET_KEY=
OK_GROUP_ID=
```

## Запуск

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Установите зависимости:

`pip install -r requirements.txt`
