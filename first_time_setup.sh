#!/bin/bash -ex

function install() {(
    sudo apt install -y aria2 libssl-dev build-essential libncursesw5-dev libreadline-gplv2-dev\
        libssl-dev libgdbm-dev libc6-dev libsqlite3-dev tk-dev libbz2-dev git automake autoconf\
        libtool curl
)}

function download() {(
    aria2c --conf-path=aria.txt
)}

function build_python() {(
    mkdir -p Python
    tar xaf downloads/Python.tar.xz -C Python
    cd Python/*/
    ./configure --enable-shared
    make -j8
    sudo make -j8 install
)}

function build_wiringpi() {(
    mkdir -p wiringPi
    tar xaf downloads/wiringPi.tar.gz -C wiringPi
    cd wiringPi/*/
    ./build
)}

function build_protobuf() {(
    mkdir -p protobuf
    tar xaf downloads/protobuf.tar.gz -C protobuf
    cd protobuf/*/
    ./autogen.sh
    ./configure
    make -j8
    sudo make -j8 install
)}

function build_virtualenv() {(
    python3.5 -m venv virtualenv
    source ./virtualenv/bin/activate
    pip install -e ../..
)}

install
cd ./installer
download
cd _build
build_python
build_wiringpi
build_protobuf
sudo ldconfig
build_virtualenv

echo Done.
