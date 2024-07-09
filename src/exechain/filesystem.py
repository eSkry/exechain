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


from exechain.base import BaseTool
from exechain.internal import _get_path, safe_format, safe_format_with_global

import shutil
from pathlib import Path
import os


class Copy(BaseTool):
    def __init__(self, src, dst) -> None:
        super().__init__()
        self.src = src
        self.dst  = dst


    def _invoke(self, vars: dict = {}):
        src = safe_format_with_global(self.src, vars)
        dst = safe_format_with_global(self.dst, vars)
        
        _src = _get_path(src)

        if not _src.exists():
            raise FileNotFoundError(f"not found {src}")
        
        print(f"copy [src: {src} dst: {dst}]")
        if _src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)

        return True


class Makedirs(BaseTool):
    def __init__(self, dir) -> None:
        super().__init__()
        self.dir = dir


    def _invoke(self, vars: dict = {}):
        dir = _get_path(safe_format_with_global(self.dir, vars))
        dir.mkdir(parents=True, exist_ok=True)
        return True


class Touch(BaseTool):
    def __init__(self, file) -> None:
        super().__init__()
        self.file = file


    def _invoke(self, vars: dict = {}):
        file = _get_path(safe_format_with_global(self.file, vars))
        file.touch(exist_ok=True)
        return True


class WriteFile(BaseTool):
    def __init__(self, file, content, mode="w") -> None:
        super().__init__()
        self.file = file
        self.content = content
        self.mode = mode
    
    
    def _invoke(self, vars: dict = {}):
        file = safe_format_with_global(self.file, vars)
        content = safe_format_with_global(self.content, vars)
        mode = safe_format_with_global(self.mode, vars)
        
        print(f"write [file: {file}]")
        with open(file, mode) as f:
            f.write(self.content)
            
        return True


class Remove(BaseTool):
    def __init__(self, file_or_dir: Path) -> None:
        super().__init__()
        self.file_of_dir = file_or_dir


    def _invoke(self, vars: dict = {}):
        path = _get_path(safe_format_with_global(self.file_of_dir, vars))
        
        print(f"remove [{path}]")
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                os.remove(path)
        return True
        
    def __str__(self) -> str:
        return f"remove {self.file_of_dir}"


class Chmod(BaseTool):
    def __init__(self, path: Path, mode) -> None:
        super().__init__()
        self.target = path
        self.mode = mode
    

    def _invoke(self, vars: dict = {}):
        target = _get_path(safe_format_with_global(self.target, vars))
        mode = safe_format_with_global(self.mode, vars)
        
        print(f"chmod  [{target} mode: {mode}]")
        target.chmod(mode)
        return True
        
    