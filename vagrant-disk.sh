#!/bin/sh
set -e

main() {
  local cmd="$( which vagrant-disk )"
  set -x
  "$cmd" --traceback "$@"
}

main "$@"
