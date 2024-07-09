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


from exechain.base import (
    Target, 
    TargetRef, 
    ConditionalTarget, 
    BaseTool, 
    ForEachFileTarget,
    TargetShellContains,
    get_target_by_name, 
    get_target_names,
    include
    # make_targets_for_files
)

from exechain.filesystem import (
    Makedirs, 
    Chmod, 
    Copy, 
    Remove, 
    Touch, 
    WriteFile
)

from exechain.git import (
    GitBranch, 
    GitRepository
)

from exechain.network import (
    Download
)

from exechain.shell import (
    Shell, 
    Print
)
