BASE_IP_ADDRESS=192.168.1.126

mkfifo fifo.500
cat fifo.500 | nc.traditional $BASE_IP_ADDRESS 5000 &
/opt/vc/bin/raspivid -o fifo.500 -t 0 -b 1000000
rm fifo.500
