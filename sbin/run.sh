#!/bin/bash

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${CURR_DIR}/common.sh

TOPICS=$1

#
python $PROJECT_ROOT/main.py --topics ${TOPICS}