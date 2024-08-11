#!/bin/bash

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${CURR_DIR}/common.sh

TOPICS=$1
PUBLISH_STATUS=$2

#
python $PROJECT_ROOT/main.py --topics ${TOPICS} --publish_status ${PUBLISH_STATUS}