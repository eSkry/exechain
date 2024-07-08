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


from exechain.base import which, _get_path


class GitBranch:
    def __init__(self, path, branch):
        self.path = path
        self.branch = branch
        
        self.git = which('git')
        if not self.git:
            raise Exception("git is not installed")
    
        
    def __call__(self, vars = None):
        print(f"enter [git branch:{self.branch} in:{str(self.path)}]")

        command = [str(self.git),  'checkout', self.branch]
        cur_dir = os.getcwd()
        os.chdir(str(self.path))

        print(f"git [command {command}]")
        ret = os.system(" ".join(command))
        os.chdir(cur_dir)
        print(f"leave [git branch:{self.branch}]")
        return ret == 0
    

class GitRepository:
    def __init__(self, url, target_directory = None, branch = None) -> None:
        self.url = url
        self.branch = branch
        self.target_directory = _get_path(target_directory)
        
        self.git = which('git')
        if not self.git:
            raise Exception("git is not installed")
    
    
    def __call__(self, vars = None) -> None:
        print(f"enter [git clone url:{self.url} in:{self.target_directory}]")

        repo_path = self.target_directory
        if not self.target_directory:
            name = self.url.split('/')[-1]
            name = name.replace('.git', '')
            repo_path = Path(os.getcwd()) / name
        
        if not Path(repo_path).exists():
            command = [str(self.git), 'clone', self.url, str(repo_path)]
            print(f"git [command {command}]")
            ret = os.system(" ".join(command))
        else:
            print(f"skip [git clone {self.url}]")
            
        if self.branch:
            GitBranch(repo_path, self.branch)()
        print(f"leave [git clone {self.url}]")
        
        return True