all: ksurobot/protocol/proto/main_pb2.py ksurobot/protocol/proto/Main.java

ksurobot/protocol/proto/main_pb2.py: ksurobot/protocol/proto/main.proto
	protoc $< --python_out=./

ksurobot/protocol/proto/Main.java: ksurobot/protocol/proto/main.proto
	protoc $< --java_out=`dirname $@`
