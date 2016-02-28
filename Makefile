
all: ksurobot/protocol/proto/main_pb2.py ksurobot/protocol/proto/Main.java ksurobot/hardware/_wiring_interupts.so

ksurobot/protocol/proto/main_pb2.py: ksurobot/protocol/proto/main.proto
	protoc $< --python_out=./

ksurobot/hardware/_wiring_interupts.so: ksurobot/hardware/_wiring_interupts.cpp
	g++ $< -o $@ --shared -Wall --std=gnu++11 -fPIC

ksurobot/protocol/proto/Main.java: ksurobot/protocol/proto/main.proto
	protoc $< --java_out=`dirname $@`
