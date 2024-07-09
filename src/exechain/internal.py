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
import string
from pathlib import Path


_GLOBAL_VARIBLE_POOL: dict = {}


def set_var(name: str, value) -> None:
    _GLOBAL_VARIBLE_POOL[name] = value


def get_var(name: str) -> any:
    return _GLOBAL_VARIBLE_POOL.get(name, None)


class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            return kwargs.get(key, f'{{{key}}}')
        else:
            return string.Formatter.get_value(key, args, kwargs)


_formatter = SafeFormatter()
def safe_format(input: str, vars: dict):
    return _formatter.format(input, **vars)


def safe_format_with_global(input: str, vars: dict = {}) -> str:
    tmp = safe_format(input, _GLOBAL_VARIBLE_POOL)
    return safe_format(tmp, vars)


def which(name):
    search_dirs = os.environ["PATH"].split(os.pathsep)
    
    for path in search_dirs:
        test = Path(path) / name
        if test.is_file() and os.access(test, os.X_OK):
            return test

    return None


def exit_with_message(message, code):
    print(message)
    exit(code)


def _get_path(path) -> Path:
    if isinstance(path, str):
        return Path(path)
    else:
        return path


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


def include(file) -> None:
    """Включает файл сборки в текущий файл

    Args:
        file (Path | str): Путь до файла *.exechain

    Raises:
        FileNotFoundError: Файл не найден
    """
    path = _get_path(file)
    
    if not path.exists():
        raise FileNotFoundError(f"error include file '{str(path)}': not found file")
    
    script = """
    from exechain.exechain import *

    """

    with open(path, "r") as f:
        script += f.read()

    exec(script)
    
    
    