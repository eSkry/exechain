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
import requests
import os


class Download(BaseTool):
    def __init__(self, url, save_path = None) -> None:
        super().__init__()
        self.url = url
        self.save_path = _get_path(save_path)
        
    def __call__(self):
        if self.save_path is None:
            self.save_path = self.url.split('/')[-1]
        
        print(f"download [url: {str(self.url)} save_path: {str(self.save_path)}]")
        try:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                with open(str(self.save_path), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
                        
            # Проверка, что файл существует
            if not self.save_path.exists():
                raise FileNotFoundError(f"Файл {self.save_path} не был создан.")

            # Дополнительная проверка на непустоту файла (опционально)
            if os.path.getsize(str(self.save_path)) == 0:
                raise ValueError(f"Файл {self.save_path} пуст.")

        except Exception as e:
            return False
        return True


