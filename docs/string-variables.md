# Переменные в строках

**exechain** определяет стандартный набор переменных которые доступны для подстановки в строки. переменная в тексте указывается имя переменной обрамленное в фигурные скобки. Например - `"Привет {target.name}!!!"`. (Если используется f-string строка то необходимо обрамлять двойными фигурными скобками).

## Классы переменных

Есть несколько классов переменных - **локальные** и **глобальные**. 

### Локальные переменные

Локальные переменные это переменные которые существуют в иерархии целей. Примером такой переменной является - `{target.name}`. У каждой цели она имеет ее имя.

Перечень локальных переменных:
- `target.name`: Имя текущей цели

### Глобальные переменные

