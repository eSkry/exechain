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


import subprocess
import os
from pathlib import Path

from exechain.internal import _get_path, which, JnString


class GitBranch:
    def __init__(self, path, branch):
        self.path: JnString = JnString(str(path))
        self.branch: JnString = JnString(branch)
        
        self.git = which('git')
        if not self.git:
            raise Exception("git is not installed")
    
    def _invoke(self, vars: dict = {}):
        path = self.path.precessed_string(vars)
        branch = self.branch.precessed_string(vars)

        command = [str(self.git), 'checkout', branch]
        cur_dir = os.getcwd()
        os.chdir(path)

        print(f"git [{command}]")
        ret = os.system(" ".join(command))
        os.chdir(cur_dir)
        return ret == 0
    

class GitRepository:
    def __init__(self, url, target_directory = None, branch = None) -> None:
        self.url: JnString = JnString(url)
        self.branch: JnString = JnString(branch)
        self.target_directory: JnString = JnString(target_directory)
        
        self.git = which('git')
        if not self.git:
            raise Exception("git is not installed")
    
    
    def _invoke(self, vars: dict = {}):
        url = self.url.precessed_string(vars)
        branch = self.branch.precessed_string(vars)
        target_directory = self.target_directory.precessed_string(vars)
        
        repo_path = target_directory
        if not target_directory:
            name = url.split('/')[-1]
            name = name.replace('.git', '')
            repo_path = Path(os.getcwd()) / name
        
        if not Path(repo_path).exists():
            command = [str(self.git), 'clone', url, str(repo_path)]
            print(f"git [command {command}]")
            ret = os.system(" ".join(command))
            
        if branch:
            GitBranch(repo_path, branch)()
        
        return True
