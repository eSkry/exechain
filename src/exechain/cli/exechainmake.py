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


import argparse
import importlib
from pathlib import Path
import sys


IMPORT_STRINGS = """
from exechain.exechain import *
from exechain.base import exec_target, target_pool, get_target_names
from exechain.internal import update_env_variables

"""

ENTRY_POINT = """

try:
    update_env_variables()
    for target in args.targets:
        exec_target(target)
except Exception as e:
    print(f"ERROR: [{e}]")
"""


def cli(argv: list[str] | None = None) -> None:
    entry_point_file = Path.cwd() / "exechain"
    
    parser = argparse.ArgumentParser()
    parser.add_argument('targets', nargs='*', default=["all"])
    args = parser.parse_args(argv)
    
    SCRIPT = IMPORT_STRINGS
    
    if entry_point_file.exists():
        with open(entry_point_file, "r") as f:
            data = f.read()
            SCRIPT += data
        
        SCRIPT += ENTRY_POINT
        
        exec(SCRIPT)
    else:
        print(f"exechain make file not found!")
        exit(1)
    