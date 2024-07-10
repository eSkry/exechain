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
import fnmatch
import subprocess
from pathlib import Path
from jinja2 import Template

from exechain.internal import (
    _get_path, 
    file1_newer_file2, 
    exit_with_message, 
    jn_format_with_global,
    JnString
)


_TARGET_POOL: dict = {}


def get_target_by_name(name: str ):
    return _TARGET_POOL[name]


def get_target_names() -> list[str]:
    return list(_TARGET_POOL.keys())


def exec_target(name: str):
    if name not in _TARGET_POOL:
        raise Exception(f"error target '{name}': not found")
    return _TARGET_POOL[name]._invoke(None)


def target_pool() -> dict:
    return _TARGET_POOL


class BaseTool:
    """Данный класс служит меткой для обозначения подклассов инструментов.
    
    Инструмент - это callable который выполняется при выполнении инструкций у класса Target и его подклассов.
    """
    def __init__(self) -> None:
        pass
    
    def _invoke(self, vars: dict = None):
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
    target : Path | str
        Файл/папка или произвольное название - проверяемая цель для выполнения цепочки действий.
        Если файла не существует то это означает необходимость его создать для этой цели выполняются цепочки действий по порядку,
        сперва выполняется обработка dependecies затем recept.
    
    dependencies : list[&quot;callable&quot;]
        Список зависимостей которые будут выполнены перед рецептами (recept) для сборки данного target.
        Данные зависимости определяют что необходимо выполнить чтобы далее выполнить сборку данной цели (recept).
        
    recept : list[&quot;callable&quot;]
        Инструкции которые будут выполнены. Предполагается что выполнение данных инструкций удовлетворит требование target.
    
    target_run_lock : bool
        Флаг указывающий что данная цель уже выполняется. Необходимо для предотвращения циклической зависимости
    
    user_vars : dict
        Словарь передаваемый в __init__ как vars.
        
    target_vars : dict
        Словарь локальных переменных цели. Содержит такие переменные как "имя цели".
    """
    def __init__(self, 
                 target, 
                 dependencies: list["Target"] = None, 
                 recept = None,
                 vars: dict = None) -> None:
        self.target: JnString = JnString(target)
        
        if self.target.raw_string in _TARGET_POOL:
            raise Exception(f"error [target {self.target.raw_string}: already exists]")
        
        self.recept = recept if recept else []
        self.dependencies: list["Target"] = dependencies if dependencies else []
        self.target_run_lock = False
        
        self.user_vars: dict = vars if vars else {}
        self.target_vars = {
            'target': {
                'name': self.target.raw_string
            }
        }
        
        # TODO: Реализовать лучший способ регистрации целей в пуле
        _TARGET_POOL[self.target.raw_string] = self
    
    
    def __str__(self) -> str:
        return self.target.raw_string
    
    
    def _is_file(self) -> bool:
        """Вспомогательный метод для определения того, стоит ли обращаться с целью как с файлом или папкой.

        Returns:
            bool: Является ли цель файлом или папкой
        """ 
        return True

    
    def _prepare_invoke_environment(self, parent):
        """Подготавливает окружение в котором возможно резолвить переменные в строках.
        
        Данный метод должен быть вызван до _invoke или непосредственно в _invoke но до обращений к переменным зависящих от окружения.

        Args:
            parent (Target): Родительская цель для получения родительских переменных
            restore_cache (bool, optional): Предварительно удалить прошлый результат работы фукнции. Defaults to False.
        """
        vars_merged: dict = {}
        if parent:
            vars_merged = parent.user_vars.copy()
        vars_merged.update(self.user_vars)
        vars_merged.update(self.target_vars)

        resolved_target_name = self.target.precessed_string(vars_merged)
        
        return {
            'vars_merged': vars_merged,
            'resolved_target_name': resolved_target_name
        }
        
    
    def _invoke(self, parent):
        # TODO: Возможно стоит ставить флаг что цель была собрана и выполнена
        
        environment = self._prepare_invoke_environment(parent)
        vars_merged = environment['vars_merged']
        
        if self.target_run_lock:
            print(f"❕ Предотвращение циклической зависимости {parent.target.raw_string if parent else '_'} -> {environment['resolved_target_name']}")
            return

        self.target_run_lock = True
        # try:
        def _run_recept():
            print(f"🔹 target [{environment['resolved_target_name']} ({self.target.raw_string})]")
            for cmd in self.recept:
                if isinstance(cmd, BaseTool):
                    if not cmd._invoke(vars_merged):
                        exit_with_message(f"Ошибка при выполнении: {str(cmd)}", -1)
                else: 
                    if not cmd(vars_merged):
                        exit_with_message(f"Ошибка при выполнении: {str(cmd)}", -1)
        
        def _run_dependencies(dependency_list):
            for dependency in dependency_list:
                dependency._invoke(self)
        
        need_exec, dep_list = self.need_exec_target(environment=environment)
        if need_exec:
            _run_dependencies(dep_list)
            _run_recept()
            
        # except Exception as e:
        #     exit_with_message(f"‼️ Ошибка при выполнении: {str(e)}",  -2)
        self.target_run_lock = False

    
    def need_exec_target(self, parent = None, environment: dict = None):
        """Определяет требуется ли выполнить данную цель а так же определяет список зависимостей которые требуют выполнения.

        ВАЖНО! Передавать следует только один аргумент - parent либо environment. Так как если указать оба аргумента в приоритете будет environment. 
        
        Args:
            parent (Target, optional): Родительский объект. Defaults to None.
            environment (dict, optional): Окружение с которым производить проверку. Defaults to None.

        Returns:
            list: Первый элемент это булево значение означающее нужно ли выполнять данную цель. 
                Второй параметр это список зависимостей которые нужно выполнить.
        """
        env = None
        if environment:
            env = environment
        else:
            env = self._prepare_invoke_environment(parent)
        
        resolved_target_path = _get_path(env['resolved_target_name'])
        # Если цель не существует то необходимо выполнить все для ее построения
        if not resolved_target_path.exists():
            return (True, self.dependencies)
        else:
            dependencies_to_run = []
            for dep in self.dependencies:
                dep_env = dep._prepare_invoke_environment(self)
                need_add, _ = dep.need_exec_target(environment=dep_env)
                if need_add:
                    dependencies_to_run.append(dep)
                elif dep._is_file():
                    if file1_newer_file2(dep_env['resolved_target_name'], env['resolved_target_name']):
                        dependencies_to_run.append(dep)
            
            if dependencies_to_run:
                return (True, dependencies_to_run)
        return (False, [])
    

class TargetRef:
    """Класс TargetRef управляет ссылками на целевые объекты, которые хранятся в глобальном пуле целей (_TARGET_POOL).
    """
    def __init__(self, target) -> None:
        self.target: JnString = JnString(target)


    def _invoke(self, parent: Target):
        """
        Вызывает объект из глобального пула целей (_TARGET_POOL) по имени, если он существует.
        
        Возвращает:
        Объект из пула целей (_TARGET_POOL) по имени.

        Исключения:
        KeyError
            Если целевая задача не найдена в пуле целей (_TARGET_POOL), выбрасывается исключение с соответствующим сообщением.
        """
        # NOTE: Если резолвить здесь имена то невозможно будет найти цель если в имени целей используются переменные 
        # env = {'vars_merged': {}}
        # if parent:
        #     env = parent._prepare_invoke_environment(parent)
            
        # target = self.target.precessed_string(env['vars_merged'])
            
        # if target not in _TARGET_POOL:
        #     raise KeyError(f"not found target '{target}' for TargetRef class")
        
        # TODO: Сделать что-то получе чем прямое обращение к словарю
        return _TARGET_POOL[self.target.raw_string]._invoke(parent)


class ConditionalTarget:
    def __init__(self, condition, callable_if_true = None, callable_if_false = None):
        self.callable_if_true = callable_if_true
        self.callable_if_false = callable_if_false
        self.condition = condition

    def _invoke(self, parent):
        res = None
        if isinstance(self.condition, callable):
            res = self.condition()
        else:
            res = self.condition
        
        def _invoker(obj):
            if callable(obj):
                if parent:
                    obj(parent.vars_merged)
                else:
                    obj(parent)
            else:
                obj._invoke(parent)
        
        if res:
            if self.callable_if_true is not None:
                _invoker(self.callable_if_true)
        else:
            if self.callable_if_false is not None:
                _invoker(self.callable_if_false)
        
        return True


class TargetShellContains(Target):
    def __init__(self, 
                 target: Path, 
                 check_command: str, 
                 dependencies: list = None, 
                 recept: list = None, 
                 _not: bool = False) -> None:
        super().__init__(target, dependencies, recept)
        self.check_command: JnString = JnString(check_command)
        self._not = _not
    
    
    def _is_file(self) -> bool:
        return False
    

    def need_exec_target(self, parent = None, environment: dict = None) -> bool:
        env = None
        if environment:
            env = environment
        else:
            env = self._prepare_invoke_environment(parent)
        
        check_command = self.check_command.precessed_string(env['vars_merged'])
        result = subprocess.run(
            check_command, 
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        output_contains_target =  env['resolved_target_name'] not in result.stdout
        if self._not:
            output_contains_target = not output_contains_target
        
        if not output_contains_target:
            return (True, self.dependencies)
        
        deep_to_update = []
        for dep in self.dependencies:
            if dep.need_exec_target(parent=self):
                deep_to_update.append(dep)
        
        if not dep:
            # Если нет зависимостей которые требуют обновления то и не нужно собирать эту цель (так как она существует).
            self.exec_cond_cache = (False, [])
        else:
            self.exec_cond_cache = (True, deep_to_update)

        return self.exec_cond_cache


class TargetFileWithLine(Target):
    def __init__(self, target: Path, search_line: str, dependencies: list = [], recept: list = []) -> None:
        super().__init__(target, dependencies, recept)
        self.search_line: JnString = JnString(search_line)
        
    def need_exec_target(self, parent = None, environment: dict = None) -> bool:
        env = None
        if environment:
            env = environment
        else:
            env = self._prepare_invoke_environment(parent)
        
        search_line = self.search_line._processed_cache(env['vars_merged'])
        
        with open(env['resolved_target_name'], 'r', encoding='utf-8') as file:
            for line in file:
                if search_line in line:
                    return True
        return False


def make_targets_for_files(root_folder, pattern: str, max_depth: int = -1):
    root_folder = jn_format_with_global(root_folder, {})
    pattern = jn_format_with_global(pattern, {})
    
    target_list = []
    
    def recursive_search(current_folder, current_depth):
        if current_depth > max_depth and max_depth > 0:
            return
        
        for entry in os.listdir(current_folder):
            path = os.path.join(current_folder, entry)
            
            if os.path.isdir(path):
                recursive_search(path, current_depth + 1)
            elif os.path.isfile(path) and fnmatch.fnmatch(entry, pattern):
                # target = path
                target_list.append(Target(path))
    
    recursive_search(root_folder, 0)
    return target_list


# class GlobTarget:
#     def __init__(self, 
#                  target, 
#                  file_pattern,
#                  depth: int = -1,
#                  dependency: list["callable"] =[], 
#                  recept: list["callable"] = [],
#                  first_detect_checking: bool = True) -> None:
        
#         self.target = _get_path(target)
#         self.pattern = file_pattern
#         self.dependency = dependency
#         self.recept = recept

#         self._invoke(None)
        
    
#     def _invoke(self, parent: Target):
#         target = jn_format_with_global(self.target, parent.vars_merged)
        
#         fpath = str(self.target / self.pattern)
#         files = glob.glob(fpath)
#         if not files:
#             raise Exception(f"error target '{str(self.target)}' pattern '{fpath}' ({self.pattern}): not found files")

#         if self.suffix:
#             suffixed = []
#             for file in files:
#                 suffixed.append(
#                     Target(f"{file}{self.suffix}", dependencies=[
#                         Target(file, dependencies=self.dependency, recept=self.recept)
#                     ])
#                 )
                
#             Target(self.target, dependencies=suffixed)
#         else:
#             Target(self.target, dependencies=[Target(file if not self.suffix else f"{file}{self.suffix}", dependencies=self.dependency, recept=self.recept) for file in files])


def add_folder_to_path(folder):
    """Добавляет путь в переменную окружения PATH. 
    
    Если данный путь уже существует в переменной PATH он будет проигнорирован.

    Функция поддерживает несколько типов переменной folder. Особенности имеет лишь тип dict:
    При передачи типа dict ожидается что он будет содержать праметр с ключем 'target@name',
    в котором будет указан путь.
    
    Args:
        folder (Path | str | dict | list): Путь который необходимо добавить
    
    Raises:
        Exception: Если переданный тип не поддерживается
    """
    folders_list = []
    if isinstance(folder, str) or isinstance(folder, Path):
        folders_list = [str(folder)]
    elif isinstance(folder, list):
        folders_list = [str(f) for f in folder]
    else:
        raise Exception(f"Unsupported type on variable 'folder': {folder}")
    
    tmp_path = os.environ.get("PATH")
    for folder in folders_list:
        if folder in tmp_path:
            continue
        tmp_path = f"{folder}{os.pathsep}{tmp_path}"

    os.environ["PATH"] = tmp_path
