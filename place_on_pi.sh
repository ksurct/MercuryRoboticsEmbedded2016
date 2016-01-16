#!/bin/bash -ex

SERVER="pi@raspberrypi.local"

build_result=$(nix-build --option system armv7l-linux)
nix-copy-closure --to "$SERVER" ./result
ssh "$SERVER" nix-env -i "$build_result"
