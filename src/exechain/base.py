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
import requests
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
    def __init__(self) -> None:
        pass


class Target:
    def __init__(self, target: Path, dependencies: list["callable"] = [], recept: list["callable"] = []) -> None:
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
    
    
    def __call__(self, vars=None):
        if self.target_run_lock:
           raise Exception(f"target '{str(self.target)}' already run")
        
        self.target_run_lock = True
        try:
            for dependency in self.dependencies:
                dependency(self.vars)
            
            if not self.target.exists():
                print(f"enter [target {str(self.target)}]")
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


# Метатаргет смотрит не на наличие файла а на наличее метки о выполнении в кеше
# class MetaTarget(Target):
#     def __init__(self, target: str, dependencies: list["callable"] = [], recept: list["callable"] = []) -> None:
#         super().__init__(target, dependencies, recept)

#     def __call__(self):
#         return super().__call__()
    

class TargetRef:
    def __init__(self, target) -> None:
        self.target = str(target)

    def __call__(self, vars = None):
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