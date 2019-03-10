#!/bin/bash

project=`basename \`pwd\``

python cc/gen.py project "${project}"

pip install -r requirements.txt
