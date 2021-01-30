#!/bin/bash

./manage.py flush
./manage.py loaddata Presets

git add .
git commit
