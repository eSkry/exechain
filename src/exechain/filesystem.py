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


from exechain.base import _get_path, BaseTool

import shutil
from pathlib import Path
import os

class Copy(BaseTool):
    def __init__(self, src, dst) -> None:
        super().__init__()
        self.src = src
        self.dst  = dst

    def __call__(self, vars = None):
        _src = _get_path(self.src)

        if not _src.exists():
            raise FileNotFoundError(f"not found  {str(self.src)}")
        
        print(f"copy [src: {str(self.src)} dst: {str(self.dst)}]")
        if _src.is_dir():
            shutil.copytree(str(self.src), str(self.dst))
        else:
            shutil.copy(str(self.src), str(self.dst))

        return True


class Makedirs(BaseTool):
    def __init__(self, dir) -> None:
        super().__init__()
        self.dir: Path = _get_path(dir)

    def __call__(self, vars = None):
        self.dir.mkdir(parents=True, exist_ok=True)
        return True


class Touch(BaseTool):
    def __init__(self, file) -> None:
        super().__init__()
        self.file: Path = _get_path(file)

    def __call__(self, vars = None):
        self.file.touch(exist_ok=True)
        return True


class WriteFile(BaseTool):
    def __init__(self, file, content, mode="w") -> None:
        super().__init__()
        self.file: Path = _get_path(file)
        self.content: str = content
        self.mode = mode
    
    def __call__(self, vars = None):
        print(f"write [file: {str(self.file)}]")
        with open(str(self.file), self.mode) as f:
            f.write(self.content)
            
        return True


class Remove(BaseTool):
    def __init__(self, file_or_dir: Path) -> None:
        super().__init__()
        self.file_of_dir: Path = _get_path(file_or_dir)

    def __call__(self, vars = None):
        print(f"remove [file_or_dir: {str(self.file_of_dir)}]")
        if self.file_of_dir.exists():
            if self.file_of_dir.is_dir():
                shutil.rmtree(str(self.file_of_dir))
            else:
                os.remove(str(self.file_of_dir))
        return True
        
        
    def __str__(self) -> str:
        return f"remove {self.file_of_dir}"


class Chmod(BaseTool):
    def __init__(self, file_or_dir: Path, mode) -> None:
        super().__init__()
        self.target = file_or_dir
        self.mode = mode
    

    def __call__(self, vars = None):
        print(f"chmod  [file_or_dir: {str(self.target)} mode: {self.mode}]")
        self.target.chmod(self.mode)
        return True
        
    