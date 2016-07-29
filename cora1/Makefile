# Uses -m32 option to compile and link to build 32 bit version on 64 bit centos

OBJS = main.o
SRCS = main.c

INCLUDES = /adp/include
LIBS = /adp/lib

CFLAGS = -g -I$(INCLUDES) -m32

all: main 

main: $(OBJS)
	cc -m32 -L$(LIBS) -g $(OBJS) -o $@ -lreals -lrcs -lcurses -lnsl

clean:
	rm -f $(OBJS)

