#!/bin/bash

# global
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "${CURR_DIR}")"

# vars

# error-trap
trap 'echo "[ERROR] sbin/script";exit 1' ERR
trap 'echo "[INTERRUPTED] received signal to stop";exit 1' SIGQUIT SIGTERM SIGINT

# utils
line_break() {
  seq -s= 100 | tr -d '[:digit:]';echo
}

try() {
  [[ $- = *e* ]]; SAVED_OPT_E=$?
  set +e
}

throw() {
  exit $1
}

catch() {
  export exception_code=$?
  (( $SAVED_OPT_E )) && set +e
  return $exception_code
}

#
echo "-----------------------------------------"
echo "CURR_DIR: ${CURR_DIR}"
echo "PROJECT_ROOT: ${PROJECT_ROOT}"
echo "-----------------------------------------"

