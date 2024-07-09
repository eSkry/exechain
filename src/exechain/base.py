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
from pathlib import Path
import json
import shutil
import platform
import subprocess
import glob
import os

_IS_WINDOWS = platform.system().lower() == "windows"
_IS_LINUX = platform.system().lower() == "linux"
_IS_MACOS = platform.system().lower() == "darwin"


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


_TARGET_POOL: dict = {}


def get_target_by_name(name: str ):
    return _TARGET_POOL[name]


def get_target_names() -> list[str]:
    return list(_TARGET_POOL.keys())


def exec_target(name: str):
    if name not in _TARGET_POOL:
        raise Exception(f"error target '{name}': not found")
    return _TARGET_POOL[name]()


def target_pool() -> dict:
    return _TARGET_POOL


class BaseTool:
    """Данный класс служит меткой для обозначения подклассов инструментов.
    
    Инструмент - это callable который выполняется при выполнении инструкций у класса Target и его подклассов.
    """
    def __init__(self) -> None:
        pass


class Target:
    """
    Target class выполняет цепочки действий в зависимости от состояния target. (Аналогично тому как работают цели в Makefile).
    
    Как и у make - у класса Target целью является файл или папка. И дальшее выполнение инструкций выполняется в зависимости от состояния этой цели.
    Если файл/папка не существует - данная цель будет выполнена.
    Если файл/папка существует - этап сборки этой цели будет пропущен.
    
    При создании экземпляра класса он автоматически добавляется в пулл целей.
    
    Attributes
    ----------
    target : Path
        Файл/папка или произвольное название - проверяемая цель для выполнения цепочки действий.
        Если файла не существует то это означает необходимость его создать для этой цели выполняются цепочки действий по порядку,
        сперва выполняется обработка dependecies затем recept.
        
    dependencies : list[&quot;callable&quot;]
        Список зависимостей которые будут выполнены перед рецептами (recept) для сборки данного target.
        Данные зависимости определяют что необходимо выполнить чтобы далее выполнить сборку данной цели (recept).
        
    recept : list[&quot;callable&quot;]
        Инструкции которые будут выполнены. Предполагается что выполнение данных инструкций удовлетворит требование target.
        
    target_name : str
        Имя цели в виде строки
        
    target_run_lock : bool
        Флаг указывающий что данная цель уже выполняется. Необходимо для предотвращения циклической зависимости
        
    vars : dict
        Список переменных которые будут использованы при выполнении цепочки действий. 
        Данные переменные могут использоваться для подстановки плейсхолдеров у строк.
    """
    def __init__(self, target: Path, dependencies: list["callable"] = [], recept: list["callable"] = []) -> None:
        """
        Args:
            target (Path): Путь к файлу или папке а так же цель для выполнения цепочки действий (сборки).
            dependencies (list[&quot;callable&quot;], optional): Список зависимостей которые будут выполнены перед рецептами (recept) для сборки данного target.. Defaults to [].
            recept (list[&quot;callable&quot;], optional): Список зависимостей которые будут выполнены после dependencies и предполагают содание требуемого объекта target.. Defaults to [].

        Raises:
            Exception: _description_
            Exception: _description_
        """
        self.target: Path = _get_path(target)
        self.recept: list["callable"] = recept
        self.dependencies: list["callable"]  = dependencies
        self.target_name = str(target)

        if dependencies is None and recept is None:
            raise Exception(f"error [target {str(self.target)}: nothing to do]")
        
        if self.target_name in _TARGET_POOL:
            raise Exception(f"error [target {str(self.target)}: already exists]")
        
        _TARGET_POOL[self.target_name] = self
        self.target_run_lock = False
        
        self.vars = {
            "target-name": self.target_name
        }
    
    
    def __str__(self) -> str:
        return f"target [{self.target_name}]"
    
    
    def __call__(self, vars = None):
        if self.target_run_lock:
           raise Exception(f"target '{str(self.target)}' already run")
        
        self.target_run_lock = True
        try:
            if self.need_exec_target():
                print(f"enter [target {str(self.target)}]")
                for dependency in self.dependencies:
                    dependency(self.vars)
                
                for cmd in self.recept:
                    if not cmd(self.vars):
                        exit_with_message(f"Ошибка при выполнении: [{str(cmd)}]", -1)
                
                print(f"leave [target {str(self.target)}]")
            else:
                print(f"skip [target {str(self.target)}]")
        except Exception as e:
            exit_with_message(f"Ошибка при выполнении:  [{str(e)}]",  -2)
        
        self.target_run_lock = False
        return True
    
    
    def need_exec_target(self) -> bool:
        return not self.target.exists()
    

class TargetRef:
    """Класс TargetRef управляет ссылками на целевые объекты, которые хранятся в глобальном пуле целей (_TARGET_POOL).
    
    Конструктор:
    -------------
    __init__(self, target) -> None
        Инициализирует экземпляр класса TargetRef. Преобразует целевую задачу в строку и сохраняет её.

        Параметры:
        target : любое значение, которое может быть преобразовано в строку;
            Имя или файл/папка.

    Методы:
    -------
    __call__(self, vars = None)
        Вызывает объект из глобального пула целей (_TARGET_POOL) по имени, если он существует.
        
        Параметры:
        vars : dict, optional
            Необязательный словарь переменных. 

        Возвращает:
        Объект из пула целей (_TARGET_POOL) по имени.

        Исключения:
        KeyError
            Если целевая задача не найдена в пуле целей (_TARGET_POOL), выбрасывается исключение с соответствующим сообщением.
    """
    def __init__(self, target) -> None:
        self.target = str(target)

    def __call__(self, vars = None):
        """
        Вызывает объект из глобального пула целей (_TARGET_POOL) по имени, если он существует.
        
        Параметры:
        vars : dict, optional
            Необязательный словарь переменных.

        Возвращает:
        Объект из пула целей (_TARGET_POOL) по имени.

        Исключения:
        KeyError
            Если целевая задача не найдена в пуле целей (_TARGET_POOL), выбрасывается исключение с соответствующим сообщением.
        """
        if self.target not in _TARGET_POOL:
            raise KeyError(f"not found target {self.target} for TargetRef class")
        return _TARGET_POOL[self.target]()


class ConditionalTarget:
    def __init__(self, condition, if_true: callable = None, if_false: callable = None):
        self.if_true = if_true
        self.if_false = if_false
        self.condition = condition

    def __call__(self, vars = None):
        res = None
        if isinstance(self.condition, callable):
            res = self.condition()
        else:
            res = self.condition
        
        if res:
            if self.if_true is not None:
                self.if_true()
        else:
            if self.if_false is not None:
                self.if_false()
        
        return True


class TargetShellContains(Target):
    def __init__(self, target: Path, check_command: str, dependencies: list = [], recept: list = []) -> None:
        super().__init__(target, dependencies, recept)
        self.check_command = check_command
    
    def need_exec_target(self) -> bool:
        result = subprocess.run(
            self.check_command, 
            shell=True, 
            check=True, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        return self.target_name not in result.stdout


class ForEachFileTarget:
    def __init__(self, 
                 target, 
                 dependency: list["callable"] =[], 
                 recept: list["callable"] = [],  
                 glob_pattern = "*",
                 target_suffix = None) -> None:
        
        self.target = _get_path(target)
        self.pattern = glob_pattern
        self.dependency = dependency
        self.recept = recept
        self.suffix = target_suffix

        self.__call__()
        
    def __call__(self, vars = None):
        fpath = str(self.target / self.pattern)
        files = glob.glob(fpath)
        if not files:
            raise Exception(f"error target '{str(self.target)}' pattern '{fpath}' ({self.pattern}): not found files")

        if self.suffix:
            suffixed = []
            for file in files:
                suffixed.append(
                    Target(f"{file}{self.suffix}", dependencies=[
                        Target(file, dependencies=self.dependency, recept=self.recept)
                    ])
                )
                
            Target(self.target, dependencies=suffixed)
        else:
            Target(self.target, dependencies=[Target(file if not self.suffix else f"{file}{self.suffix}", dependencies=self.dependency, recept=self.recept) for file in files])
     

# def make_targets_for_files(directory, file_pattern = "*", dependencies=[], recept_appender: callable = None):
#     target = _get_path(directory)
#     files = glob.glob(str(target / file_pattern))
    
#     refs = []
#     for file in files:
#         Target(file, dependencies=dependencies, recept=recept_appender(file))
#         refs.append(TargetRef(file))
    
#     return refs



_IMPORT_STRINGS = """
from exechain.exechain import *

"""


def include(file) -> None:
    path = _get_path(file)
    
    if not path.exists():
        raise Exception(f"error include file '{str(path)}': not found file")
    
    script = _IMPORT_STRINGS
    
    with open(path, "r") as f:
        script += f.read()

    exec(script)