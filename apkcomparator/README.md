# Сравнение сборок
Скрипт предназначен для сравнение двух APK сборок между собой
и анализирует разницу в размере, количестве методов и манифестах. Отчёт
публикуется в `result/report.txt` файл.

Входная точка - `python -m apkcomparator.start`.

## Окружение
Перед запуском убедитесь, что у вас установлена переменная окружения
`ANDROID_HOME` и `JAVA_HOME` версии 1.8.

## Варианты работы
#### Параметры запуска

`--prev-apk-path`: путь до предыдущего APK

`--apk-path`: путь до текущего APK

`--output`: опциональный путь до вывода, по умолчанию сохранение репорта происходит
в директорию `result`