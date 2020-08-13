#! /bin/bash

cd ..
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install .

rm -r dist
python setup.py sdist
python setup.py bdist_wheel
