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
SPREADSHEET_ID=ВАШ_ID_GOOGLE_ТАБЛИЦЫ
TELEGRAM_TOKEN=ВАШ_ТЕЛЕГРАМ_ТОКЕН
TG_CHAT_ID=НАЗВАНИЕ_ТЕЛЕГРАМ_КАНАЛА
VK_ACCESS_TOKEN=ВАШ_КЛЮЧ_ДОСТУПА_ВК
VK_GROUP_ID=ID_ГРУППЫ_ВК
OK_ACCESS_TOKEN=ВАШ_ОК_ТОКЕН
OK_APPLICATION_KEY=ПУБЛИЧНЫЙ_КЛЮЧ_ПРИЛОЖЕНИЯ_ОК
OK_APPLICATION_SECRET_KEY=СЕКРЕТНЫЙ_КЛЮЧ_ПРИЛОЖЕНИЯ_ОК
OK_GROUP_ID=ID_ГРУППЫ_ОК
```

## Запуск

Для запуска сервиса понадобится Python третьей версии.

Скачайте код с GitHub. Установите зависимости:

`pip install -r requirements.txt`

Запустить

`phyton publisher.py`
