all: ksurobot/protocol/proto/main_pb2.py ksurobot/hardware/_wiring_interupts.so

ksurobot/protocol/proto/main_pb2.py: ksurobot/protocol/proto/main.proto
	protoc $< --python_out=./

ksurobot/hardware/_wiring_interupts.so: ksurobot/hardware/_wiring_interupts.cpp
	g++ $< -o $@ --shared -Wall --std=gnu++11 -fPIC
