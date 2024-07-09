"""
Copyright (c) 2024 Leonov Artur (depish.eskry@yandex.ru)

Permission is hereby granted to use, copy, modify, and distribute this code in any form, provided that the above copyright notice and this permission notice appear in all copies.

DISCLAIMER:
This source code is provided "as is", without any warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the code is with you.



Copyright (c) 2024 Леонов Артур (depish.eskry@yandex.ru)

Разрешается использовать, копировать, изменять и распространять этот код в любом виде, при условии сохранения данного уведомления.

ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ:
Этот исходный код предоставляется "как есть" без каких-либо гарантий, явных или подразумеваемых, включая, но не ограничиваясь, подразумеваемыми гарантиями товарной пригодности и пригодности для конкретной цели. Вся ответственность за использование данного кода лежит на вас.
"""


import os
import re


def exchain_replace_variables(string: str, variables: dict) -> str:
    """Заменяет {placholder} подстроки в строке в соответствии со словарем variables

    Формат плейсхолдера '{имя_переменной}'. Например: "Эй! {name} привет!"
    Пример вывода:
        `print(exchain_replace_variables("Эй! {name} привет!"), {"name":"Jon"})` - Выведет "Эй! Jon привет!".
    
    Args:
        string (str): Исходная строка
        variables (dict): Словарь с переменными. Где именем является {placeholder} строки а значением строка которая встанет на место {placeholder}

    Returns:
        str: строку с замененными плейсхолдерами
    """
    # Находим все подстроки в фигурных скобках
    placeholders = re.findall(r"\{(.*?)\}", string)
    # missing_keys = []

    # Заменяем подстроки на значения из словаря
    for placeholder in placeholders:
        if placeholder in variables:
            string = string.replace(f"{{{placeholder}}}", str(variables[placeholder]))
        # else:
            # missing_keys.append(placeholder)
    
    # Проверяем, есть ли отсутствующие ключи в словаре
    # if missing_keys:
        # print(f"Missing keys in dictionary: {', '.join(missing_keys)}")
    
    return string


def file1_newer_file2(file1, file2):
    return os.path.getmtime(file1) > os.path.getmtime(file2)
