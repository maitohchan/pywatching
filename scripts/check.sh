#! /bin/bash

flack8 ../pywatching/line.py
black --check ../pywatching/line.py
black --diff ../pywatching/line.py
mypy ../pywatching/line.py
