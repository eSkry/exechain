# exechain

**exechain** - система сборки, вдохновленная популярной системой сборки make. Целью проекта является предоставление удобного и гибкого инструмента для автоматизации процесса сборки и управления зависимостями в проектах.


## Введение

**exechain** - это утилита, которая позволяет описывать и выполняет цепочки команд, необходимые для сборки вашего проекта и управления его зависимостями, аналогично тому, как это делает make. Это удобный и мощный инструмент, подходящий для различных типов проектов и сценариев.

## Список возможностей

- [x] Описание процесса сборки декларативным методом
- [x] Отслеживание изменения файлов для пересборки только необходимых файлов
- [x] Включение скриптов сборки из подкаталогов

## Установка

Установка утилиты выполняется командой: `pip install exechain`. Так же можно установить из GitVerse: `pip install --index-url https://gitverse.ru/api/packages/Depish/pypi/simple/ exechain`

## Начало работы

Подробная документация по началу работы с exechain будет добавлена, как только проект достигнет более стабильной версии. На данный момент основная концепция работы аналогична работе целей в make.

## Примеры использования

Для создания сценария сборки необходимо создать файл `exechain`. В данном файле используется язык программирования Python и доступны все его функции. 

Пример сборочного скрипта:
```python
# Данный импорт для подсказок в IDE
from exechain.exechain import *

Target("hello",
    dependencies = [
        Target("main.cpp", recept=[
            Shell("echo 'int main() {return 0;}' > {{target.name}}")
        ])
    ],
    recept=[
        Shell("g++ main.cpp -o hello")
    ]
)
```

После создания сборочного скрипта нам необходимо его запустить. Для этого в пакете exechain имеется утилита `ech`. 
Необходимо перейти в каталог с файлом `exechain` и выполнить команду

```shell
ech hello
```

Где **hello** это имя цели которую необходимо выполнить. Можно указать несколько целей. Любая цель из любого места в файле может быть вызвана через аргументы.

Данный проект так же [собирается с помощью exechain](https://gitverse.ru/Depish/exechain/content/master/exechain).

# Пример конфигурационного файла

```python
Target("hello",
    dependencies = [
        Target("main.cpp", recept=[
            Shell("echo 'int main() {return 0;}' > {{target.name}}")
        ])
    ],
    recept=[
        Shell("g++ main.cpp -o hello")
    ]
)
```

## Состояние проекта

Проект находится на ранней стадии разработки. Многие функции все еще находятся в стадии проектирования и реализации. Следите за обновлениями и новыми релизами.

## Вклад

Мы приветствуем вклад в развитие проекта. Если у вас есть идеи, исправления или улучшения, пожалуйста, создайте issue или pull request в этом репозитории.

## Лицензия

Подробности можно найти в файле LICENSE.md.

---

Благодарим вас за интерес к exechain! Надеемся, что этот инструмент окажется полезным и облегчит вашу работу над проектами.