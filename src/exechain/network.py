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
from exechain.internal import _get_path, safe_format

import requests
import os


class Download(BaseTool):
    def __init__(self, url, save_path = None) -> None:
        super().__init__()
        self.url = url
        self.save_path = _get_path(save_path)
    
    
    def _invoke(self, vars: dict = {}):
        if self.save_path is None:
            self.save_path = self.url.split('/')[-1]

        url = safe_format(self.url, vars)
        path = safe_format(self.save_path, vars)
        
        print(f"download [url: {url} save_path: {path}]")
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
                        
            # Проверка, что файл существует
            if not path.exists():
                raise FileNotFoundError(f"Файл {path} не был создан.")

            # Дополнительная проверка на непустоту файла (опционально)
            if os.path.getsize(str(path)) == 0:
                raise ValueError(f"Файл {path} пуст.")

        except Exception as e:
            return False
        return True
