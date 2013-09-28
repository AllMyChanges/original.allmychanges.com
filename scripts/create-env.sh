#!/bin/bash

if [ ! -e env/bin/python ]; then
    virtualenv --python=/usr/bin/python --system-site-packages --distribute env
    env/bin/pip install -e `pwd`
    env/bin/pip install -r requirements.txt
fi
