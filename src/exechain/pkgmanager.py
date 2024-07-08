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
from pathlib import Path
import os
import sys

_INSTALLED_PACKAGES_CACHE = []


def which(name):
    search_dirs = os.environ["PATH"].split(os.pathsep)
    
    for path in search_dirs:
        test = Path(path) / name
        if test.is_file() and os.access(test, os.X_OK):
            return test

    return None


class PackageManagerBase:
    def __init__(self, no_interactive: bool = True) -> None:
        self.no_interactive = no_interactive
    
    def install(self, packages):
        pass
    
    def update(self):
        pass
    
    def run_as_root(self, command, may_use_sudo=True):
        if os.getuid() != 0:
            if may_use_sudo and which("sudo"):
                command = ["sudo"] + command
            else:
                command = ["su", "root", "-c"] + command
        
        subprocess.check_call(command, stdin=sys.stdin)



class PakmanManager(PackageManagerBase):
    def __init__(self, no_interactive: bool = True):
        super().__init__(no_interactive)
    
    def install(self, packages):
        command = ["pacman", "-S", "--needed"]
        if self.no_interactive:
            command.append("--noconfirm")
            
        command.extend(packages)
        self.run_as_root(command)


class AptManager(PackageManagerBase):
    def __init__(self, no_interactive: bool = True) -> None:
        super().__init__(no_interactive)
    
    def install(self, packages):
        command = ["apt-get", "install"]
        if self.no_interactive:
            command.append("-y")
        
        command.extend(packages)
        self.run_as_root(command)
    
    def update(self):
        command = ["apt-get", "update"]
        if self.no_interactive:
            command.append("-y")
        
        self.run_as_root(command)


class RpmManager(PackageManagerBase):
    def __init__(self, no_interactive: bool = True) -> None:
        super().__init__(no_interactive)

    def install(self, packages):
        command = []
        if which("dnf"):
            command = ["dnf",  "install"]
        else:
            command = ["yum", "install"]
        
        if self.no_interactive:
            command.append("-y")
        
        command.extend(packages)
        self.run_as_root(command)


    def update(self):
        if which("dnf"):
            command = ["dnf", "update"]
        else:
            command = ["yum", "update"]

        if self.no_interactive:
            command.append("-y")

        self.run_as_root(command)


def get_installed_packages():
    pass


def _rpm_package_installed(package_name):
    command = ["rpm", "-q", package_name]
    try:
        result = subprocess.check_output(command)
    except Exception as e:
        pass

    