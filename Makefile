ALL_FILES = $(shell git ls-files)

robot/protocol/proto/main_pb2.py: robot/protocol/proto/main.proto
	protoc $< --python_out=./

output.tar: $(ALL_FILES)
	tar cvf output.tar $(ALL_FILES)
