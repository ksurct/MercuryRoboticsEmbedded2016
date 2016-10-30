#!/bin/bash -ex



rm -f fifo.500
mkfifo fifo.500
nc.traditional -l 9001 < ./fifo.500 &
/opt/vc/bin/raspivid -o fifo.500 -t 0 -b 1000000
rm fifo.500
