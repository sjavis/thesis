ROOT_DIR = $(HOME)/software/c++/ellib
INC = $(ROOT_DIR)/include
BIN = $(ROOT_DIR)/bin
LIBS = -lellib

CXX = mpic++
CXXFLAGS = -I$(INC) -L$(BIN) $(LIBS) -Wall -DPARALLEL

all:
	$(CXX) example.cpp -o run.exe $(CXXFLAGS)
	mpirun -np 2 run.exe

debug: CXXFLAGS += -g
debug: all

clean:
	rm run.exe
