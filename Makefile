KERNAL := /home/cmp408/rpisrc/linux
PWD := $(shell pwd)
obj-m += led.o

all:
	make ARCH=arm CROSS_COMPILE=$(CROSS) -C $(KERNAL) M=$(PWD) modules
clean:
	make -C $(KERNAL) M=$(PWD) clean
