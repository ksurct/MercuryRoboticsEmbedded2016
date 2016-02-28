
all: ksurobot/protocol/proto/main_pb2.py ksurobot/protocol/proto/Main.java ksurobot/hardware/_wiring_encoders.so

ksurobot/protocol/proto/main_pb2.py: ksurobot/protocol/proto/main.proto
	protoc $< --python_out=./

ksurobot/hardware/_wiring_encoders.so: ksurobot/hardware/_wiring_encoders.cpp
	g++ $< -o $@ --shared -Wall --std=gnu++11 -fPIC

ksurobot/protocol/proto/Main.java: ksurobot/protocol/proto/main.proto
	protoc $< --java_out=`dirname $@`
