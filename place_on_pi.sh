#!/bin/bash -ex

SERVER="pi@raspberrypi.local"

filter='2> >(grep -v "Unsupported ioctl" 1>&2)'

build_cmd="nix-build --option system armv7l-linux --option ssh-substituter-hosts "$SERVER" "$filter""
# echo $build_cmd
# exit

build_result=$(eval "$build_cmd")
nix-copy-closure --to "$SERVER" "$build_result"
ssh "$SERVER" nix-env -i "$build_result"
